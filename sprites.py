INK,CLAY,BUTTER,SAGE,WOOD,TEAL,MOSS='#2E2A1F','#A3472F','#F2D27A','#B9CC98','#7A5634','#9FC7C4','#4F6B3A'
S={
'bmx':(["...........hhh..","....sss....f....",".....ffffffff...",".oooo.f..f.oooo.","o....o.ff.o.f..o","o..ffffc..o.f..o","o....o....o....o",".oooo......oooo."],
  {'h':INK,'s':INK,'f':CLAY,'c':INK,'o':INK}),
'code':([".kkkkkkkkkkkk.",".kddddddddddk.",".kdgggdyyyddk.",".kdddrrrdgddk.",".kdyyyydggddk.",".kddddddddddk.",".kkkkkkkkkkkk.","kkkkkkkkkkkkkk"],
  {'k':WOOD,'d':INK,'g':SAGE,'y':BUTTER,'r':'#E9B8A4'}),
'game':(["..kkkkkkkkkk..",".kckcccccrck..".replace('..','k.',1)[:0] or ".kckccccccrck.","kckkkccccrcrck","kcckccccccrcck","kccck....kccck",".kkk......kkk."],
  {'k':INK,'c':TEAL,'r':CLAY}),
'f1':(["kkkk..................",".kk......yy...........",".kkbbbbbyybb..........","..oo.bbbbbbbbbb.oo....",".oooobbbbbbbbbboooobbk",".oggo.bbbbbbbb.oggo...","..oo............oo...."],
  {'k':INK,'b':CLAY,'y':BUTTER,'o':INK,'g':'#D9C9A0'}),
}
def rects(name,x0=0,y0=0,c=1):
    rows,cols=S[name]; out=[]
    for y,row in enumerate(rows):
        x=0
        while x<len(row):
            ch=row[x]
            if ch=='.': x+=1; continue
            e=x
            while e<len(row) and row[e]==ch: e+=1
            out.append(f'<rect x="{x0+x*c}" y="{y0+y*c}" width="{(e-x)*c}" height="{c}" fill="{cols[ch]}"></rect>')
            x=e
    return ''.join(out)
def size(name):
    rows,_=S[name]; return max(map(len,rows)),len(rows)
def svg(name,scale,label=None):
    w,h=size(name)
    a='role="img" aria-label="%s"'%label if label else 'aria-hidden="true"'
    return f'<svg width="{w*scale}" height="{h*scale}" viewBox="0 0 {w} {h}" shape-rendering="crispEdges" {a} style="flex: none">{rects(name)}</svg>'
if __name__=='__main__':
    import sys
    for n in S: print(n, size(n), [len(r) for r in S[n][0]])
