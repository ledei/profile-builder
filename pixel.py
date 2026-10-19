# Tiny PNG reader/writer (Python standard library only) and a pixelate filter for the portrait.
# Handles 8-bit RGB / RGBA / grey PNGs without interlacing, which covers most exported photos.
import struct, zlib

def read_png(path):
    d = open(path, 'rb').read()
    if d[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError(f'{path} is not a PNG. Export your photo as PNG first.')
    i, idat, hdr = 8, b'', None
    while i < len(d):
        n = struct.unpack('>I', d[i:i + 4])[0]
        kind, chunk = d[i + 4:i + 8], d[i + 8:i + 8 + n]
        i += 12 + n
        if kind == b'IHDR':
            hdr = chunk
        elif kind == b'IDAT':
            idat += chunk
    w, h, depth, color, _, _, interlace = struct.unpack('>IIBBBBB', hdr)
    channels = {0: 1, 2: 3, 4: 2, 6: 4}.get(color)
    if depth != 8 or channels is None or interlace:
        raise ValueError(f'{path}: use an 8-bit RGB or RGBA PNG without interlacing.')
    stride = w * channels
    raw = zlib.decompress(idat)
    rows, prev, p = [], bytearray(stride), 0
    for _ in range(h):
        f, line = raw[p], bytearray(raw[p + 1:p + 1 + stride])
        p += 1 + stride
        for x in range(stride):
            a = line[x - channels] if x >= channels else 0
            b = prev[x]
            c = prev[x - channels] if x >= channels else 0
            if f == 1: line[x] = (line[x] + a) & 255
            elif f == 2: line[x] = (line[x] + b) & 255
            elif f == 3: line[x] = (line[x] + (a + b) // 2) & 255
            elif f == 4:
                pa, pb, pc = abs(b - c), abs(a - c), abs(a + b - 2 * c)
                line[x] = (line[x] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        rows.append(line)
        prev = line
    # always hand back RGB pixels
    def rgb(line, x):
        o = x * channels
        return (line[o],) * 3 if channels <= 2 else tuple(line[o:o + 3])
    return w, h, [[rgb(r, x) for x in range(w)] for r in rows]

def write_png(path, pixels):
    h, w = len(pixels), len(pixels[0])
    raw = b''.join(b'\x00' + bytes(v for px in row for v in px) for row in pixels)
    chunk = lambda t, c: struct.pack('>I', len(c)) + t + c + struct.pack('>I', zlib.crc32(t + c) & 0xffffffff)
    open(path, 'wb').write(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0))
                           + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b''))

def pixelate(src, dst, grid=64, size=512):
    """Crop the photo to a centred square, average it down to grid x grid, scale back up with hard edges."""
    w, h, px = read_png(src)
    side = min(w, h)
    x0, y0 = (w - side) // 2, (h - side) // 2
    cells = []
    for gy in range(grid):
        row = []
        for gx in range(grid):
            xa, xb = x0 + gx * side // grid, x0 + (gx + 1) * side // grid
            ya, yb = y0 + gy * side // grid, y0 + (gy + 1) * side // grid
            block = [px[y][x] for y in range(ya, max(yb, ya + 1)) for x in range(xa, max(xb, xa + 1))]
            row.append(tuple(sum(c[i] for c in block) // len(block) for i in range(3)))
        cells.append(row)
    scale = size // grid
    write_png(dst, [[cells[y // scale][x // scale] for x in range(grid * scale)] for y in range(grid * scale)])
