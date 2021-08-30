#!/usr/bin/env python3
from matplotlib import pyplot as plt
from math import sin,cos,pi,log2
import os,sys,getopt,argparse

     
def circle(r,x0=0,y0=0,eps=0.05):
  n=max(6,int(pi/(eps/r)**0.5))
  da=2*pi/n
  x=[r*cos(da*i)+x0 for i in range(n+1)]
  y=[r*sin(da*i)+y0 for i in range(n+1)]
  return(x,y,)
  
def ageFromDiop(D):
  return 25*log2(21/D)**(1/1.7)

def diopFromAge(a):
  return 21*2**(-(a/25)**1.7)

def plotEncoderDisk(ax,x0=0,y0=0,r=60,dr=10,n=64,m=10,slant=0.25):
  ro=r+dr
  ri=r
  ax.plot(*circle(ro,x0,y0), 'k',lw=1)
  ax.plot(*circle(ri,x0,y0), 'k',lw=1)
  def ticks(ri,ro,n=64,m=11,slant=0.3):
    dang=2*pi/n
    ddang=dang/2/m
    for i in range(n):
      for j in range(m+1):
        angi=dang*i+ddang*(j-m/2)*(1+slant)
        ango=dang*i+ddang*(j-m/2)*(1-slant)
        p0=(ri*cos(angi),ri*sin(angi))
        p1=(ro*cos(ango),ro*sin(ango))
        yield from (p0,p1,p0,)
  p=list(zip(*((x+x0,y+y0) for x,y in ticks(ri,ro,n=n,m=m,slant=slant))))
  ax.plot(*p,'k',lw=1)  
  ax.plot(*circle(2/2,x0,y0), 'k',lw=1)
  ax.plot(*circle(15/2,x0,y0), 'k',lw=1)
  ax.plot(*circle(35.5/2,x0,y0), 'k',lw=1)
  ax.plot(*circle(37.5/2,x0,y0), 'k',lw=1)
  ax.plot((-5+x0,5+x0),(0+y0,0+y0), 'k',lw=1)
  ax.plot((0+x0,0+x0),(-5+y0,5+y0), 'k',lw=1)


def main(argv):
  r=60
  dr=10
  n=64
  m=10
  slant=0.25
  saveas=None
  try:
     opts, args = getopt.getopt(argv[1:],"had:n:m:r:s:o:",longopts=["ofile=", "saveas="])
  except getopt.GetoptError:
     print( f'{os.path.basename(argv[0])} [-h -a -n -m -r -d -s -o <outputfile>]')
     sys.exit(2)
  for opt,arg in opts:
    if opt in ("-o","--ofile","--saveas"):
      saveas=arg
    if opt in ("-n",):
      n=eval(arg)
    if opt in ("-m",):
      m=eval(arg)
    if opt in ("-r",):
      r=eval(arg)
    if opt in ("-s",):
      slant=eval(arg)
    if opt in ("-d",):
      dr=eval(arg)

  plt.close()
  pagewidth=8.5*25.4
  xmin=-pagewidth/2
  xmax=-xmin
  
  f=plt.figure(figsize=(8.5,11))
  ax=f.add_axes((0,0,1.0,1.0),aspect='equal')
  origins=[dict(x0=-31,y0=63),dict(x0=31,y0=-64)]
  for origin in origins:
    plotEncoderDisk(ax,**origin, r=r, dr=dr, n=n, m=m, slant=slant)   
  

  ax.set_xlim((xmin,xmax))
  ax.set_ylim((xmin*11/8.5,xmax*11/8.5))
  ax.axis('off')
  plt.show()
  if saveas:
    (filename,ext)=os.path.splitext(saveas)
    if ext=='':
      ext='.pdf'
    print(f'Saves as: "{filename+ext}"')
    plt.savefig(filename+ext, papertype = 'letter', orientation = 'portrait', format = ext.lstrip('.'))
  plt.close()

if __name__ == '__main__':
  main(sys.argv)


