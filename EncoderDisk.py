from matplotlib import pyplot as plt
from math import sin,cos,pi
import os
def cyclicGrayGen(n):
  """
  print('\nn=2**k:','\n'.join([f'{i^(i>>1):08b}' for i in cyclicGrayGen(16)]),sep='\n')
  print('\nn//2==0, n//4!=0:','\n'.join([f'{i^(i>>1):08b}' for i in cyclicGrayGen(14)]),sep='\n')
  print('\nn//4==0:','\n'.join([f'{i^(i>>1):08b}' for i in cyclicGrayGen(12)]),sep='\n')
  """
  if n%2!=0:
    raise Exception(f"cyclicGrayGen(n={n}): 'n' has to be even for a cyclic gray code.")
  bl=(n-1).bit_length()
  nn=1<<bl
  if n%4==0:
      yield from range(n//4)
      yield from range(nn//2-n//4,nn//2+n//4)
      yield from range(nn-n//4,nn)
  else:
      yield from range(n//2)
      yield from range(nn-n//2,nn)
      
def circle(r,eps=0.05):
  n=max(6,int(pi/(eps/r)**0.5))
  da=2*pi/n
  x=[r*cos(da*i) for i in range(n+1)]
  y=[r*sin(da*i) for i in range(n+1)]
  return(x,y,)
  
def plotEncoderDisk(r=60,dr=3,n=100,labels=True,tickmarks=True,saveas=None,bits=1,xmin=-100,xmax=100):
  def plot_ring(ax,r,dr,n,bit=0):
    da=2*pi/n
    m=int((da*(r+dr)/0.6)+0.5)
    dda=da/(m*2)
    xy=[[rij*cos(a),rij*sin(a)] for i,g in enumerate(cyclicGrayGen(n)) for j in range(m*4) for rij,a in ((r+dr if ((g^(g>>1))>>bit)&1 and ((j+1)//2)%2 else r,-da*i-dda*(j//2+0.5)),)]
    ax.plot([x for x,y in xy],[y for x,y in xy], 'k',lw=1)
    ax.plot(*circle(r), 'k',lw=1)
  plt.close()
  max_bits=(n*4-1).bit_length()
  A4=(lambda A:(2**((-A*0.5)-0.25),2**((-A*0.5)+0.25)))(4)#
  f=plt.figure(figsize=(A4[0]/0.0254,A4[1]/0.0254))
  width=(xmax-xmin)*0.001#in mm
  ax=f.add_axes((0.025,0.025,width/A4[0],width/A4[0]),aspect='equal')
  for bit in range(bits):
    plot_ring(ax,r+dr*bit,dr,n,bit)
  ro=r+dr*bits
  ax.plot(*circle(ro), 'k',lw=1)
  if labels or tickmarks:
    da=2*pi/n
    for i in range(n):
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
  
#plotEncoderDisk(r=60.5, n=256, bits=7, labels=False,tickmarks=True,saveas='EncDisk256')
plotEncoderDisk(r=60.5, n=256, bits=7, labels=True,tickmarks=True,saveas='EncDisk256_lbl_a')
#plotEncoderDisk(r=60.5, n=254, bits=8, labels=True,tickmarks=True)

