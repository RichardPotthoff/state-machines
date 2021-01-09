from matplotlib import pyplot as plt
from math import sin,cos,pi
import os

def circle(r,eps=0.05):
  n=max(6,int(pi/(eps/r)**0.5))
  da=2*pi/n
  x=[r*cos(da*i) for i in range(n+1)]
  y=[r*sin(da*i) for i in range(n+1)]
  return(x,y,)
  
def plotEncoderDisk(r=60,dr=3,n=100,phase=-1/4,labels=True,tickmarks=True,saveas=None,bits=1,xmin=-100,xmax=100):
  def plot_ring(ax,r,dr,n,phase=0):
    da=2*pi/n
    m=int((da*r/0.6)+0.5)
    dda=da/(m*2)
    ax.plot([(r+((j+1)%4)//2*dr*(j//(4*m)))*cos((i+phase)*da+0.5*j//2*dda) for i in range(int(n)+1) for j in range(m*8)], [(r+((j+1)%4)//2*dr*(j//(4*m)))*sin((i+phase)*da+0.5*j//2*dda) for i in range(int(n)+1) for j in range(m*8)], 'k',lw=1)
    
  plt.close()
  A4=(lambda A:(2**((-A*0.5)-0.25),2**((-A*0.5)+0.25)))(4)#
  f=plt.figure(figsize=(A4[0]/0.0254,A4[1]/0.0254))
  width=(xmax-xmin)*0.001#in mm
  ax=f.add_axes((0.025,0.025,width/A4[0],width/A4[0]),aspect='equal')
  ni=n
  for i in range(bits):
    plot_ring(ax,r+dr*i,dr,ni,phase=phase)
    ni/=2
  ro=r+dr*bits
  ax.plot(*circle(ro), 'k',lw=1)
  if labels or tickmarks:
    n4=n*4
    da=2*pi/n4
    for i in range(n4):
      a=-da*(i+0.5)
      ca=cos(a)
      sa=sin(a)
      if tickmarks:
        ax.plot(*[[r1*cs for r1 in(ro+dr/2,ro+dr,)] for cs in(ca,sa,)],'k',lw=1)
        ax.plot(*[[r1*cs for r1 in(r-dr/2,r-dr,)] for cs in(ca,sa,)],'k',lw=1)
      if labels:
        ax.text((ro+1.2*dr)*ca,(ro+1.2*dr)*sa,f'{i}',rotation=a/pi*180,rotation_mode='anchor',va='center',ha='left', fontsize=6)

  ax.plot(*circle(15/2), 'k',lw=1)
  ax.plot(*circle(35.5/2), 'k',lw=1)
  ax.plot(*circle(37.5/2), 'k',lw=1)
  ax.plot((-5,5),(0,0), 'k',lw=1)
  ax.plot((0,0),(-5,5), 'k',lw=1)
  ax.set_xlim((xmin,xmax))
  ax.set_ylim((xmin,xmax))
  ax.axis('off')
  plt.show()
  if saveas:
    (filename,ext)=os.path.splitext(saveas)
    if ext=='':
      ext='.pdf'
    plt.savefig(filename+ext, papertype = 'a4', orientation = 'portrait', format = ext.lstrip('.'))
  plt.close()
  
plotEncoderDisk(r=60.5, n=64, bits=7, phase=-1/4,labels=False,tickmarks=True,saveas='EncDisk256')
plotEncoderDisk(r=60.5, n=64, bits=7, phase=-1/4,labels=True,tickmarks=True,saveas='EncDisk256_lbl')
