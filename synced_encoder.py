# State Machine Synchronized Counter with a Quadrature Encoded Input
# 
# The state machine counts up to a maximum, and then waits for the synchronization signa.
# The synchronization signal is a 180° phase-shift of the quadrature encoded input.
#
# The reversal of the quadrature encoded input is achived by having the detectors normally
# phase shifted 270° from each other, and change temporarily to a 90° phase shift for the synchronization.
#
# The shift change from 270° to 90° is achived by eliminating one notch on the encoder disk at the
# sync position. Tis causes two count pulses in the reverse direction.
#
import scene
from scene import *
import sound
import os
from itertools import chain
from math import radians,pi,sin,cos,atan2

def grayToInt(gray):
  mask=gray>>1
  result=gray
  while mask!=0:
    result^=mask
    mask>>=1
  return result


def intToGray(i):
  return i^(i>>1)
  
def quadamp(dang,n,index='3'):
  n1=(0.5*dang/pi*n)%n
  if index=='3':
    if n1<1.5:
      n1/=3
  elif index=='1/3':
    if n1<0.5:
      n1*=3    
  return(sin(n1*2*pi))
  
def quadphase(rot,ang1,ang2,n,index='3'):
  return atan2(sin(quadamp(rot-ang1,n,index)),sin(quadamp(rot-ang2,n,index)))/pi*2+2
  

class StateTable(scene.ShapeNode):
  def __init__(self,x,y,w,h,data,**args):
    scene.Node.__init__(self,**args)
    self.data=data
    self.size=(w,h)
    self.position=(x,y)
    self.anchor_point=(0,0)
    self.statebox=ShapeNode(ui.Path.rect(0,0,18,10),stroke_color='#000000',fill_color='#ff8080')
    self.add_child(self.statebox)
    self.phase_=0
    self.state_=0
    self.cells=[None]*512
    for i in range(512):
      c=((i>>6&1)<<2)|(i>>7)
      r=i&((1<<6)-1)
      if c>3:r=63-r
      if c>3:c+=2
      cell=LabelNode("%4d"%(self.data[i]&0x7f),scale=0.5)
      cell.position=(c*19+self.size.w-200,self.size.h-36-11*r)
      cell.color=(0,0,0)
      if self.data[i]&0x7f>63:cell.color='#ff0000'
      if ((self.data[i] & 0x7f+128)-(i & 0x7f))%128==1 and i&0x7f != 63:cell.color='#009e0d'
      if ((self.data[i] & 0x7f)-(i & 0x7f))==0:cell.color='#000000'
      if ((self.data[i] & 0x7f+128)-(i & 0x7f))%128==127:cell.color='#ff0000'
      if (self.data[i] & 0x80):
        cell.color='#020202'
        self.add_child(ShapeNode(ui.Path.rect(0,0,17,9),position=cell.position,color='#55ff64'))
      self.cells[i]=cell
      self.add_child(cell)
    for i in range(128):
      c=((i>>6&1)<<2)
      r=i&((1<<6)-1)
      if c>3:r=63-r
      if c>3:c+=2
      cell=LabelNode("%4d:"%(i),scale=0.5)
      cell.position=(c*19+self.size.w-200-20,self.size.h-36-11*r)
      cell.color=(0,0,0)
      self.add_child(cell)
    for i in range(4):
      c=i+1
      r=-1.25
      cell=LabelNode(" {0:02b}".format(intToGray(i)),scale=0.5)
      cell.position=(c*19+self.size.w-200-20,self.size.h-36-11*r)
      cell.color=(0,0,0)
      self.add_child(cell)
    self.add_child(LabelNode("Phase",scale=0.75,position=(2.5*19+self.size.w-200-20,self.size.h-36-11*-2.5),color='#000000'))
    text=LabelNode("State",scale=0.75,position=(-1*19+self.size.w-200-20,self.size.h-36-11*32),color='#000000')
    text.rotation=pi/2
    self.add_child(text)
    p=ui.Path()
    p.move_to(0,0)
    p.line_to(0,self.size.h-58)
    p.move_to(19*6,0)
    p.line_to(19*6,self.size.h-58)
    self.cursor=ShapeNode(p)
    self.cursor.anchor_point=(0,0)
    self.cursor.position=(self.size.w-200,0)
    self.cursor.stroke_color=(0,0,0)
    self.add_child(self.cursor)
    self.stateLabel=LabelNode('',position=(0,13),anchor_point=(0,0),color='#000000',scale=1,font=('Ubuntu Mono',14))
    self.phase=0.75
    self.state=0
    self.add_child(self.stateLabel)
    self.updateState()

    
  @property
  def phase(self):
    return self.phase_
  @phase.setter
  def phase(self,phi):
    self.phase_=4*(frac(1/8+phi)%1)
    self.cursor.position=(self.size.w-200-9+18*self.phase_,30)
    self.updateState()
  @property
  def state(self):
    return self.state_
  @state.setter
  def state(self,state):
    self.state_=state
    self.updateState()
  def updateState(self):
    maxit=7
    while self.state_ != self.data[(int(self.phase_)<<7)|self.state_]&0x7f:
      self.state_=self.data[(int(self.phase)<<7)|self.state_]&0x7f
      maxit-=1
      if not maxit:
        break
    self.statebox.position=self.cells[(int(self.phase_)<<7)|self.state_].position
    self.stateLabel.text='State:{0:3d}, Phase:{1:02b}, Data:{2:08b}'.format(self.state,intToGray(int(self.phase)),intToGray(self.data_out))
  @property
  def data_out(self):
    return self.data[(int(self.phase_)<<7)|self.state_]

class dial(scene.Node):
  def __init__(self,x,y,r1,r2,n,**args):
    scene.Node.__init__(self,**args)
    self.all_flags = []
    self.angle_=0.0
    self.r1=r1
    self.r2=r2
    self.position=(x,y)
    self.n=n

    p=ui.Path()
    p.move_to(r1,0)
    ang1=2*2*pi/self.n
    p.add_arc(0,0,r1,0,-ang1/2,False)
    p.add_arc(0,0,r2,-ang1/2,ang1/2,True)
    p.add_arc(0,0,r1,ang1/2,0,False)
    p.close()   
    rcorr=(cos(ang1/2)*r1+r2)/2
    rcorr=0.0
    for ang in [(4*i+3)*(2*pi/n) for i in (*range(self.n//4),-0.5)]:
      flag=ShapeNode(p)
      flag.fill_color=(0,0,0)
      flag.stroke_color=(0,0,0)
      flag.alpha=0.8
      flag.position=(cos(ang)*rcorr,sin(ang)*rcorr)
      flag.anchor_point=(0.0,0.5)
      flag.rotation=ang
      self.add_child(flag)
      self.all_flags.append(flag)
    circ=scene.ShapeNode(ui.Path.oval(0,0,2*r1,2*r1))
    circ.fill_color=(1,1,1)
    circ.stroke_color=(0,0,0)
    self.add_child(circ)
    for i in range(self.n):
      ang=-i*2*pi/self.n
      text=LabelNode("%3d – "%(i-4),color=(0,0,0),scale=1.0)
      text.rotation=ang
      text.position=(cos(ang)*(self.r1-text.size.w/2),sin(ang)*(self.r1-text.size.w/2))
      self.add_child(text)
    text=LabelNode("+",color=(0,0,0),scale=1.0)
    self.add_child(text)
    
def frac(x):
  return x-int(x)
  
class dial_lock (Scene):
  def __init__(self,data,initial_state=0,**args):
    Scene.__init__(self,**args)
    self.data=data
    self.initial_state=initial_state
  def setup(self):
    self.background_color=(1,1,1)
    n=64+8
    r=0.49*min(self.size.w, self.size.h)
    rled=r*0.025
    Rled=+0.95*r
    xc=self.size.h/2
    yc=self.size.h/2
    self.phi1=1.5*2*pi/n
    self.phi2=self.phi1-3*2*pi/n
    for pos in ((xc+Rled*cos(phi),yc+Rled*sin(phi)) for phi in (self.phi1,self.phi2)):
      circ=scene.ShapeNode(ui.Path.oval(0,0,2*rled,2*rled),fill_color='#00ffde',stroke_color='#000000',position=pos)
      self.add_child(circ)
    self.statusLed=scene.ShapeNode(ui.Path.oval(0,0,2*rled,2*rled),color='#ff0000',position=(self.size.h-20,20))
    self.add_child(self.statusLed)
    self.dial=dial(self.size.h/2,self.size.h/2,0.9*r,r,n,scale=1.0)
    self.add_child(self.dial)
    text=LabelNode("——",color=(0,0,0))
    text.position=(self.size.h/2+0.9*r,self.size.h/2)
    self.add_child(text)
    self.dial.angle=pi/16
    self.stateTable=StateTable(self.size.h,0,self.size.w-self.size.h,self.size.h,self.data)
    self.stateTable.state=self.initial_state
    self.add_child(self.stateTable)
    
  def touch_began(self, touch):
    self.last_angle=atan2(touch.location.y-self.dial.position.y,touch.location.x-self.dial.position.x)
    pass

  def touch_moved(self, touch):
    angle=atan2(touch.location.y-self.dial.position.y,touch.location.x-self.dial.position.x)
    self.dial.rotation+=angle-self.last_angle
    amp1,amp2=(quadamp(phi-self.dial.rotation+2*2*pi/self.dial.n,self.dial.n//4) for phi in(self.phi1,self.phi2))
#    self.stateTable.phase=(-self.dial.rotation+2*pi)/(2*pi/(self.dial.n/4))+0.75
    self.stateTable.phase=(atan2(amp1,amp2)/(2*pi)+3/8)%1
    self.statusLed.color='#00ff16' if self.stateTable.data_out&0x80 else '#ff0000'
    self.last_angle=angle
    pass

  def touch_ended(self, touch):
    pass
addressInversionMask=(1<<9)-1 
dataInversionMask=(1<<8)-1
def dcounter():
  def ff(i,j):
    ig=intToGray(i)
    jg=intToGray(j)
    dj=ig^jg
    mask=1
    for _ in range(dj.bit_length()):
      if dj&mask:
        return grayToInt(ig^mask)
      mask<<=1

  actions=[([i+1,i,i,127-i][(i+j) % 4])%128 if (i+1)%128<=64 else ff(i,125)  for j in range(4) for i in range(128)]
  actions[126::128]=125,126,126,127
  actions[125::128]=125,126,125,125
  return dial_lock(actions,initial_state=0)
  
p=dcounter()
run(p, scene.LANDSCAPE,show_fps=True)
def test():
  from matplotlib import pyplot as plt
  import numpy as np
  n=64
  index='3'
  ang=np.linspace(0,2*pi,1000)
  phi1=0
  if index=='3':
    phi2=3/4*2*pi/(n//4)
  else:
    phi2=1/4*2*pi/(n//4)
  amp1=np.array([quadamp(x-phi1,n//4,index) for x in ang])
  plt.plot(ang,amp1-1)
  plt.plot(ang,(amp1>0)*0.5-3)
  amp2=np.array([quadamp(x-phi2,n//4,index) for x in ang])
  plt.plot(ang,amp2-1)
  plt.plot(ang,(amp2>0)*0.5-4)
  phase=np.array([quadphase(x,phi1,phi2,n//4,index) for x in ang])
  plt.plot(ang,phase)
  plt.show()
