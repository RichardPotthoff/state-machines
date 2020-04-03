"""
A 4x4x4 cube of LEDs for the visual display of the state of a state machine with 256 states: 
  4x4x4 LED-positions x [red | green] x [continuously on | blinking] = 256
  The x,y,z coordinates are in gray-code [0,1,3,2], or [00,01,11,10] in binary: wrap-around top/bottom, left/right, back/front.
  Each neighbouring state can be reached by flipping exactly one of 8 bits.
  The 8 bits are: [x0, y0, z0, x1, y1, z1, color, blink] 
  The demo shows a Hamiltonian path through all 256 states. 
  
"""

from objc_util import *
import ctypes
import sceneKit as scn
import ui
import math

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
    self.main_view = ui.View()
    w, h = ui.get_screen_size()
    self.main_view.frame = (0,0,w,h)
    self.main_view.name = 'LED Cube'
  
    self.scene_view = scn.View(self.main_view.frame, superView=self.main_view)
    self.scene_view.autoresizingMask = scn.ViewAutoresizing.FlexibleHeight | scn.ViewAutoresizing.FlexibleRightMargin
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
#    self.off_sphere = scn.Sphere(radius=r*scale)  
    self.off_sphere = scn.Capsule(capRadius=r*scale,height=3*r*scale) 
    self.off_sphere.firstMaterial.contents=UIColor.lightGrayColor().CGColor()
#    off_sphere.firstMaterial().emission().setColor_(UIColor.greenColor().CGColor())
    self.green_sphere = scn.Capsule(capRadius=r*scale*1.1,height=3*r*scale*1.05) 
    self.green_sphere.firstMaterial.contents=(UIColor.grayColor().CGColor())
    self.green_sphere.firstMaterial.emission.contents=(UIColor.greenColor().CGColor())
    self.red_sphere = scn.Capsule(capRadius=r*scale*1.1,height=3*r*scale*1.05)  
    self.red_sphere.firstMaterial.contents=UIColor.grayColor().CGColor()
    self.red_sphere.firstMaterial.emission.contents=(UIColor.redColor().CGColor())
    self.sphere_nodes = [[[scn.Node.nodeWithGeometry(self.off_sphere) for k in range(n)]for j in range(n)]for i in range(n)]
    self.off_wire = scn.Capsule(capRadius=r*0.25*scale,height=20*(n+0.5)*scale) 
    self.off_wire.firstMaterial.contents=UIColor.lightGrayColor().CGColor()
    self.red_wire = scn.Capsule(capRadius=r*0.25*scale,height=20*(n+0.5)*scale) 
    self.red_wire.firstMaterial.contents=UIColor.lightGrayColor().CGColor()
    self.red_wire.firstMaterial.emission.contents=(0.7,0,0)#UIColor.magentaColor().CGColor())
    self.blue_wire = scn.Capsule(capRadius=r*0.25*scale,height=20*(n+0.5)*scale) 
    self.blue_wire.firstMaterial.contents=UIColor.lightGrayColor().CGColor()
    self.blue_wire.firstMaterial.emission.contents=(0,0,0.75)#(UIColor.blueColor().CGColor())
    self.wire_nodes=[[[scn.Node.nodeWithGeometry((self.off_wire,self.blue_wire,self.red_wire)[0]) for j in range(n)]for i in range(n)]for k in range(3)]
    wireoffset=r*scale
    for i in range(n):
      for j in range(n):
        x=(i-(n-1)/2)*20*scale
        y=(j-(n-1)/2)*20*scale
        self.root_node.addChildNode(self.wire_nodes[0][i][j])
        self.wire_nodes[0][i][j].setPosition((x+wireoffset,0,y))
#        self.wire_nodes[0][i][j].rotateBy(math.pi/2,(0,0,1))
        self.root_node.addChildNode(self.wire_nodes[1][i][j])
        self.wire_nodes[1][i][j].setPosition((x,y-wireoffset,0))
        self.wire_nodes[1][i][j].eulerAngles=(math.pi/2,0,0)        
        self.root_node.addChildNode(self.wire_nodes[2][i][j])
        self.wire_nodes[2][i][j].setPosition((0,x,y-wireoffset))
        self.wire_nodes[2][i][j].eulerAngles=(0,0,math.pi/2)        
        for k in range(n):
          z=(k-(n-1)/2)*20*scale
          self.root_node.addChildNode(self.sphere_nodes[i][j][k])
          self.sphere_nodes[i][j][k].setPosition((x,y,z))
          self.sphere_nodes[i][j][k].eulerAngles=(0.61547970867039,0,math.pi/4)
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
    
    self.main_view.present(style='fullscreen', hide_title_bar=False)
  
  def update(self, view, atTime):
    def update_Led(index,blink_phase,red_led,green_led,off_led,pos_wire,neg_wire,off_wire):
      index=index % 256
      gray=index^(index>>1)
      iz=(2,3,1,0)[gray>>2&2|gray>>0&1]
      ix=(2,3,1,0)[gray>>3&2|gray>>1&1]
      iy=(2,3,1,0)[gray>>4&2|gray>>2&1]
      ic=gray>>7 & 1
      ib=(gray>>6 & 1) 
      ib=ib and blink_phase
      if ib: 
        neg_wire=off_wire
      xwire,ywire,led=((neg_wire,pos_wire,red_led),(pos_wire,neg_wire,green_led))[ic]
      if ib:
        led=off_led
      self.sphere_nodes[ix][iy][iz].setGeometry(led)
      self.wire_nodes[1][ix][iy].setGeometry(xwire)
      self.wire_nodes[1][ix][3-iy].setGeometry(xwire)
      self.wire_nodes[0][ix][((1,3,0,2),(2,0,3,1))[(iy+1)%2][ix]].setGeometry(xwire)   
      self.wire_nodes[2][iy][iz].setGeometry(ywire)
      self.wire_nodes[2][iy^1][iz].setGeometry(ywire)
      self.wire_nodes[0][((3,1,2,0),(0,2,1,3))[iy//2][iz]][iz].setGeometry(ywire)
      
    n_blink=3
    tick = int(atTime*7) % (256*2*n_blink)

    update_Led(self.index,tick%2,self.off_sphere,self.off_sphere,self.off_sphere, self.off_wire,self.off_wire,self.off_wire) 
    
    self.index=tick//(2*n_blink)
#    for wn in flatten(self.wire_nodes):
#      wn.setGeometry(self.off_wire)
#    for ln in flatten(self.sphere_nodes):
#      ln.setGeometry(self.off_sphere)
    update_Led(self.index,tick%2,self.red_sphere,self.green_sphere,self.off_sphere, self.red_wire,self.blue_wire,self.off_wire)

Demo.run()
