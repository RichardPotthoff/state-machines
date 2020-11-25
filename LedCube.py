"""
A 4x4x4 cube of LEDs for the visual display of the state of a state machine with 256 states: 
  4x4x4 LED-positions x [red | green] x [continuously on | blinking] = 256
  The x,y,z coordinates are in gray-code [0,1,3,2], or [00,01,11,10] in binary: wrap-around top/bottom, left/right, back/front.
  Each neighbouring state can be reached by flipping exactly one of 8 bits.
  The 8 bits are: [x0, y0, z0, x1, y1, z1, color, blink] 
  The demo shows a Hamiltonian path through all 256 states. 
  
"""
from collections import namedtuple
def count_bits(n):
  n = (n & 0x5555555555555555) + ((n & 0xAAAAAAAAAAAAAAAA) >> 1)
  n = (n & 0x3333333333333333) + ((n & 0xCCCCCCCCCCCCCCCC) >> 2)
  n = (n & 0x0F0F0F0F0F0F0F0F) + ((n & 0xF0F0F0F0F0F0F0F0) >> 4)
  n = (n & 0x00FF00FF00FF00FF) + ((n & 0xFF00FF00FF00FF00) >> 8)
  n = (n & 0x0000FFFF0000FFFF) + ((n & 0xFFFF0000FFFF0000) >> 16)
  n = (n & 0x00000000FFFFFFFF) + ((n & 0xFFFFFFFF00000000) >> 32) # This last & isn't strictly necessary.
  return n

pinspec=namedtuple('pinspec','name, input, output')
pinspec.__new__.__defaults__=('',0,0)

class Component(object):
  def __init__(self):
    self.activePins=set()
class Node(Component):
  pass
class IC(Component):
  pins={}
  outputpins=frozenset(key for key,value in pins.items() if value.output)
  inputpins=frozenset(key for key,value in pins.items() if value.input)
  @classmethod
  def data_from_pins(cls,pins): 
    return functools.reduce(operator.__or__,(cls.pins[p].output for p in pins&cls.outputpins),0)
  @classmethod
  def pins_from_data(cls,dat): return {d for d in cls.outputpins if cls.pins[d].output&dat}
  @classmethod
  def address_from_pins(cls,pins): 
    return functools.reduce(operator.__or__,(cls.pins[p].input for p in pins&cls.inputpins),0)
  @classmethod
  def pins_from_address(cls,adr): return {a for a in cls.inputpins if cls.pins[a].input&adr}
  @classmethod
  def _outputpins(cls):
    return frozenset(key for key,value in cls.pins.items() if value.output)
  @classmethod
  def test(cls):
    return cls
  def __init__(self):
    super().__init__()
#    self.inputpins=type(self).inputpins
  pass
class Eprom(IC):
  pins={
        1:pinspec('VPP',    0,    0,), 28:pinspec('VCC',    0,    0,),
        2:pinspec('A12',1<<12,    0,), 27:pinspec('A14',1<<14,    0,),
        3:pinspec('A07', 1<<7,    0,), 26:pinspec('A13',1<<13,    0,),
        4:pinspec('A06', 1<<6,    0,), 25:pinspec('A08', 1<<8,    0,),
        5:pinspec('A05', 1<<5,    0,), 24:pinspec('A09', 1<<9,    0,),
        6:pinspec('A04', 1<<4,    0,), 23:pinspec('A11',1<<11,    0,),
        7:pinspec('A03', 1<<3,    0,), 22:pinspec('/OE',    0,    0,),
        8:pinspec('A02', 1<<2,    0,), 21:pinspec('A10',1<<10,    0,),
        9:pinspec('A01', 1<<1,    0,), 20:pinspec('/CE',    0,    0,),
       10:pinspec('A00', 1<<0,    0,), 19:pinspec('D07',    0, 1<<7,),
       11:pinspec('D00',    0, 1<<0,), 18:pinspec('D06',    0, 1<<6,),
       12:pinspec('D01',    0, 1<<1,), 17:pinspec('D05',    0, 1<<5,),
       13:pinspec('D02',    0, 1<<2,), 16:pinspec('D04',    0, 1<<4,),
       14:pinspec('VSS',    0,    0,), 15:pinspec('D03',    0, 1<<3,),
        }
  outputpins=datapins=frozenset(key for key,value in pins.items() if value.output)
  inputpins=addresspins=frozenset(key for key,value in pins.items() if value.input)
  keypadLookupTable={
       frozenset(()):-6,
       frozenset((27,)):-1,
       frozenset((26,)):-2,
       frozenset((25,)):-3,
       frozenset((24,)):-4,
       frozenset((23,)):-5,
       frozenset((23,27)):1,
       frozenset((24,27)):2,frozenset((23,26)):3,
       frozenset((25,27)):4,frozenset((24,26)):5,frozenset((23,25)):6,
       frozenset((26,27)):7,frozenset((25,26)):8,frozenset((24,25)):9,frozenset((23,24)):0,
       frozenset((24,25,26)):11,
       frozenset((23,25,26)):12,frozenset((24,25,27)):13,
       frozenset((23,24,26)):14,frozenset((23,25,27)):15,frozenset((24,26,27)):16,
       frozenset((23,24,25)):17,frozenset((23,24,27)):18,frozenset((23,26,27)):19,frozenset((25,26,27)):10,
       frozenset((24,25,26,27)):24,
       frozenset((23,25,26,27)):23,
       frozenset((23,24,26,27)):22,
       frozenset((23,24,25,27)):21,
       frozenset((23,24,25,26)):20,
       frozenset((23,24,25,26,27)):25,
       }  
  def __init__(self):
    super().__init__()
  def setPin(self,pin):
    self.activePins.add(pin)
#    print(self.activePins)
  def clearPin(self,pin):
    self.activePins.discard(pin)
#    print(self.activePins)
  def pinStatus(self,pin):
    return pin in self.activePins

class Eprom1(Eprom):
  KeypadPins=frozenset((23,24,25,26,27))
  def __init__(self):
    super().__init__()
  def run(self):
    self.activePins-=self.pins_from_data(255)
    self.activePins|=self.pins_from_data(self.data_from_address(self.address_from_pins(self.activePins)))
    
  def data_from_address(self,address):   
    mode=2*((address>>12)&1)+((address>>10)&1)
    if mode in (0,2):
      key=self.key(self.pins_from_address(address))
      data=address&255
      parity=(count_bits(data)&1)==0
      if not parity and key==-6:
          data^=1<<7 #key released -> flip msb to make parity even
      elif parity:
        olddata=data
        if mode==2:
            cyclelength=1<<(max(0,(olddata&127).bit_length()-1))
        else:
           cyclelength=128
        if key >=0 and key<=9:
          if   key==7: data^=1<<7
          elif key==0: data^=1<<6
          elif key==3: data^=1<<(3 if ((data>>3^data)&1<<0) else 0)
          elif key==8: data^=1<<(0 if ((data>>3^data)&1<<0) else 3)
          elif key==2: data^=1<<(4 if ((data>>3^data)&1<<1) else 1)
          elif key==9: data^=1<<(1 if ((data>>3^data)&1<<1) else 4)
          elif key==4: data^=1<<(5 if ((data>>3^data)&1<<2) else 2)
          elif key==6: data^=1<<(2 if ((data>>3^data)&1<<2) else 5)
          elif key==1: data=(intToGray((grayToInt(data&(cyclelength-1))+1)%cyclelength))|(data&128)
          elif key==5: data=(intToGray((grayToInt(data&(cyclelength-1))-1)%cyclelength))|(data&128)
        if mode==2:
          bitmask=(cyclelength-1)|64
          data=(data&bitmask)|(olddata&(bitmask^255))
      else:
          if key==22: data=128 #reset if '+' and '-' are pressed simultaneously
    else:
      data=0 # data will be inverted -> data^255 = 255 (empty ROM)
    return data

  def key(self,activePins=None):
    if activePins==None: 
      activePins=self.activePins
    return self.keypadLookupTable[type(self).KeypadPins&activePins]
    
from objc_util import *
#import ctypes
import sceneKit as scn
import ui
import _ui
import math
import time
import threading,queue
import functools
import operator
def countup(i=0):
  while True:
   yield i
   i+=1
id=countup()

def flatten(*arg):
  stack=list(reversed(arg))
  while stack:
    y=stack.pop()
    if hasattr(y,'__iter__'):
      stack.extend(reversed(y))
    else:
      yield y

def grayToInt(gray):
  mask=gray>>1
  result=gray
  while mask!=0:
    result^=mask
    mask>>=1
  return result

def intToGray(i):
  return i^(i>>1)


class Demo:
  def __init__(self):
    self.name = 'my name is Demo'
    pass
    
  @classmethod
  def run(cls):
    cls().main()
    
  @on_main_thread
  def main(self):
# actually you need only to preserve those properties that are needed after the main_view.present call, 
# in this case the self.morpher. All the other self. prefixes are not needed for the same functionality
    self.q=queue.PriorityQueue()
    self.q1=queue.PriorityQueue()
#    ui.delay()
    self.Eprom=Eprom1()
    self.actions={'a':lambda:self.Eprom.setPin(27),'A':lambda:self.Eprom.clearPin(27),
                  'b':lambda:self.Eprom.setPin(26),'B':lambda:self.Eprom.clearPin(26),
                  'c':lambda:self.Eprom.setPin(25),'C':lambda:self.Eprom.clearPin(25),
                  'd':lambda:self.Eprom.setPin(24),'D':lambda:self.Eprom.clearPin(24),
                  'e':lambda:self.Eprom.setPin(23),'E':lambda:self.Eprom.clearPin(23),
    }
    self.main_view=ui.load_view(bindings={'button_tapped':self.button_tapped, 'rbutton_tapped':self.rbutton_tapped,'quit':self.quit,'setPin':self.setPin})
#    self.main_view = ui.View()
#    w, h = ui.get_screen_size()
#   self.main_view.frame = (0,0,w,h)
#    self.main_view.name = 'LED Cube'
    self.view1=self.main_view['view1']
    self.view2=self.main_view['view2']
    self.rbtn1=self.main_view['rbtn1']
    self.view3=self.main_view['view3']
    self.view5=self.main_view['view5']
    self.view2.hidden=True
    self.view3.hidden=True
    w=self.view5.width//4
    h=self.view5.height//14
    for i in range(28):
      self.view5.add_subview(ui.Label(
        frame=((i//14)*(self.view5.width-w), h*(i if i<14 else 27-i)+6,w,h-2),
        background_color='blue', 
        name=f'pin{i+1:02d}',
        text=self.Eprom.pins[i+1][0],
        alignment=ui.ALIGN_CENTER))
    self.view5.add_subview(ui.Label(frame=(w,h,w*2,h),text='27C256',alignment=ui.ALIGN_CENTER))
    self.view5.add_subview(ui.Label(frame=(w,0,w*2,h*0.6),text='U',alignment=ui.ALIGN_CENTER))
    for sv in self.view2.subviews: #copy, rotate, and rename numeric keys
      nb=ui.load_view_str(ui.dump_view(sv))
      nb.x=self.view3.width-sv.height-sv.y
      nb.y=sv.x
      nb.title={'1':'+','2':'y','3':'X','4':'Z','5':'-','6':'z',
    '7':'r/g','8':'x','9':'Y','0':'../_'}[sv.title]
      self.view3.add_subview(nb)
    
    self.mode=0
    self.key=''
#    self.scene_view = scn.View(self.main_view.frame, superView=self.main_view)
    self.scene_view = scn.View((0,0,self.view1.frame[2],self.view1.frame[3]), superView=self.view1)
#    self.scene_view.autoresizingMask = scn.ViewAutoresizing.FlexibleHeight | scn.ViewAutoresizing.FlexibleRightMargin
    self.scene_view.allowsCameraControl = True
    
    self.scene_view.scene = scn.Scene()
    
    self.scene_view.delegate = self
    
    self.root_node = self.scene_view.scene.rootNode
    
    self.camera_node = scn.Node()
    self.camera_node.camera = scn.Camera()
    self.camera_node.position = (-10,1.5,2)
    self.camera_node.camera.focalLength=60
    self.root_node.addChildNode(self.camera_node)    
    self.origin_node = scn.Node()
    self.root_node.addChildNode(self.origin_node)    
    self.floor_node=scn.Node(geometry=scn.Floor())
    self.floor_node.position=(0,-1.25,0)
#    self.root_node.addChildNode(self.floor_node)    
    n=4
    scale=0.1/n
    r=3
#    self.off_led = scn.Sphere(radius=r*scale)  
    self.off_led = scn.Capsule(capRadius=r*scale,height=3*r*scale) 
    self.off_led.firstMaterial.contents=UIColor.lightGrayColor().CGColor()
#    off_led.firstMaterial().emission().setColor_(UIColor.greenColor().CGColor())
    self.green_led = scn.Capsule(capRadius=r*scale*1.1,height=3*r*scale*1.05) 
    self.green_led.firstMaterial.contents=(UIColor.grayColor().CGColor())
    self.green_led.firstMaterial.emission.contents=(UIColor.greenColor().CGColor())
    self.red_led = scn.Capsule(capRadius=r*scale*1.1,height=3*r*scale*1.05)  
    self.red_led.firstMaterial.contents=UIColor.grayColor().CGColor()
    self.red_led.firstMaterial.emission.contents=(UIColor.redColor().CGColor())
    self.led_nodes = [[[scn.Node.nodeWithGeometry(self.off_led) for k in range(n)]for j in range(n)]for i in range(n)]
    self.off_wire = scn.Capsule(capRadius=r*0.25*scale,height=20*(n+0.5)*scale) 
    self.off_wire.firstMaterial.contents=UIColor.lightGrayColor().CGColor()
    self.pos_wire = scn.Capsule(capRadius=r*0.25*scale,height=20*(n+0.5)*scale) 
    self.pos_wire.firstMaterial.contents=UIColor.lightGrayColor().CGColor()
    self.pos_wire.firstMaterial.emission.contents=(0.7,0,0)#UIColor.magentaColor().CGColor())
    self.neg_wire = scn.Capsule(capRadius=r*0.25*scale,height=20*(n+0.5)*scale) 
    self.neg_wire.firstMaterial.contents=UIColor.lightGrayColor().CGColor()
    self.neg_wire.firstMaterial.emission.contents=(0,0,0.75)#(UIColor.blueColor().CGColor())
    self.wire_nodes=[[[scn.Node.nodeWithGeometry((self.off_wire,self.neg_wire,self.pos_wire)[0]) for j in range(n)]for i in range(n)]for k in range(3)]
    wireoffset=r*scale
    for i in range(n):
      for j in range(n):
        x=(i-(n-1)/2)*20*scale
        y=(j-(n-1)/2)*20*scale
        self.root_node.addChildNode(self.wire_nodes[0][i][j])
        self.wire_nodes[0][i][j].setPosition((x+wireoffset,0,y))
        self.root_node.addChildNode(self.wire_nodes[1][i][j])
        self.wire_nodes[1][i][j].setPosition((x,y-wireoffset,0))
        self.wire_nodes[1][i][j].eulerAngles=(math.pi/2,0,0)        
        self.root_node.addChildNode(self.wire_nodes[2][i][j])
        self.wire_nodes[2][i][j].setPosition((0,x,y-wireoffset))
        self.wire_nodes[2][i][j].eulerAngles=(0,0,math.pi/2)        
        for k in range(n):
          z=(k-(n-1)/2)*20*scale
          self.root_node.addChildNode(self.led_nodes[i][j][k])
          self.led_nodes[i][j][k].setPosition((x,y,z))
          self.led_nodes[i][j][k].eulerAngles=(0.61547970867039,0,math.pi/4)
    self.index=0
    constraint = scn.LookAtConstraint(self.root_node)#(self.sphere_nodes[2][2][2])    
    constraint.gimbalLockEnabled = True
    self.camera_node.constraints = constraint
    
    self.light_node = scn.Node()
    self.light_node.position = (100, 0, -10)
    self.light = scn.Light()
    self.light.type = scn.LightTypeDirectional
    self.light.castsShadow = False
    self.light.color = 'white'
    self.light_node.light = self.light
    self.root_node.addChildNode(self.light_node)
    
    self.action = scn.Action.repeatActionForever(scn.Action.rotateBy(0, math.pi*2, 0, 10))
    self.origin_node.runAction(self.action)  
    
    self.main_view.present(style='fullscreen', hide_title_bar=True)
    
  def quit(self,sender):
    self.main_view.close()
    
  def update(self, view, atTime):
    n_blink=3
    tick = int(atTime*7) % (256*2*n_blink)
    def update_Led(index, on=True,):
      blink_phase=tick%2
      gray=index
      iz=(2,3,1,0)[gray>>2&2|gray>>0&1]
      ix=(2,3,1,0)[gray>>3&2|gray>>1&1]
      iy=(2,3,1,0)[gray>>4&2|gray>>2&1]
      ic=gray>>7 & 1
      ib=(gray>>6 & 1) 
      ib=ib and blink_phase
      if on:
        xwire,ywire,led=((self.neg_wire,self.pos_wire,self.red_led),(self.pos_wire,self.neg_wire,self.green_led))[ic]
        if ib:
          led=self.off_led
          xwire=self.off_wire
      else:
        xwire,ywire,led=(self.off_wire,self.off_wire,self.off_led)
      self.led_nodes[ix][iy][iz].setGeometry(led)
      self.wire_nodes[1][ix][iy].setGeometry(xwire)
      self.wire_nodes[1][ix][3-iy].setGeometry(xwire)
      self.wire_nodes[0][ix][((1,3,0,2),(2,0,3,1))[(iy+1)%2][ix]].setGeometry(xwire)   
      self.wire_nodes[2][iy][iz].setGeometry(ywire)
      self.wire_nodes[2][iy^1][iz].setGeometry(ywire)
      self.wire_nodes[0][((3,1,2,0),(0,2,1,3))[iy//2][iz]][iz].setGeometry(ywire)
      return #update_Led()
    update_Led(self.index,on=False) 
    self.Eprom.activePins-=self.Eprom.pins_from_address(255)
    self.Eprom.activePins|=self.Eprom.pins_from_address(self.index)
    if self.mode==0:
      index=(tick//(2*n_blink))%256
      self.index=index^(index>>1)
      self.Eprom.activePins-=self.Eprom.pins_from_data(255)
      self.Eprom.activePins|=self.Eprom.pins_from_data(self.index)
    elif self.mode>=1:
      self.Eprom.run()
      self.index=self.Eprom.data_from_pins(self.Eprom.activePins)
    update_Led(self.index) 
    def update_view5():
      for i in type(self.Eprom).inputpins|type(self.Eprom).outputpins:
        cl=((0.,1.,0.,1.,),(1.,0.,0.,1.,),)[i in self.Eprom.activePins]
        sv=self.view5[f'pin{i:02d}']
        sv.background_color=cl #program hangs at exit with this line
    ui.in_background(update_view5)()#running it in the background works
    # self.view5.subviews[i-1].background_color=((0,1,0,1,),(1,0,0,1,),)[i in self.Eprom.activePins]
    try:
      t,i,item=self.q.get_nowait()
      if t>atTime:
        self.q.put((t,i,item,))
      else:
        try:
          dt=next(item,None)
          if dt:
            self.q.put((atTime+dt,i,item,))
        except:
          item()
      self.q.task_done()
    except:
      pass
      
  def transmit(self,key):
    text={'1':'eaAE','2':'daAD','3':'ebBE','4':'caAC','5':'dbBD','6':'ecCE',
    '7':'baAB','8':'cbBC','9':'dcCD','0':'edDE',
    '+':'eaAE','y':'daAD','X':'ebBE','Z':'caAC','-':'dbBD','z':'ecCE',
    'r/g':'baAB','x':'cbBC','Y':'dcCD','../_':'edDE'}[key]
    for k,c in enumerate(text):
      i=ord(c)-64
      self.actions[c]()
      yield 0.3 if k==1 else 0.1
      
  def rbutton_tapped(self,sender):
    self.mode=sender.selected_index
    if self.mode==0:
      self.view2.hidden=True
      self.view3.hidden=True
    elif self.mode==1:
      self.view2.hidden=True
      self.view3.hidden=False
    elif self.mode==2:
      self.view2.hidden=False
      self.view3.hidden=True

  def button_tapped(self,sender):
    self.key=sender.title
    self.q.put((0,next(id),self.transmit(self.key)))
  def setPin(self,sender):
    if sender.value:
      self.Eprom.setPin(sender.targetPin)
    else:
      self.Eprom.clearPin(sender.targetPin)
if __name__=='__main__':
  D=Demo()  
  D.main()
  
#x=[D.Eprom.data_from_address(a^255)^255 for a in range(1<<15)] #inverted data
#with open('LedCube.bin','wb') as f: f.write(bytes(x))
