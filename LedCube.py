"""
A 4x4x4 cube of LEDs for the visual display of the state of a state machine with 256 states: 
  4x4x4 LED-positions x [red | green] x [continuously on | blinking] = 256
  The x,y,z coordinates are in gray-code [0,1,3,2], or [00,01,11,10] in binary: wrap-around top/bottom, left/right, back/front.
  Each neighbouring state can be reached by flipping exactly one of 8 bits.
  The 8 bits are: [x0, y0, z0, x1, y1, z1, color, blink] 
  The demo shows a Hamiltonian path through all 256 states. 
  
"""
def count_bits(n):
  n = (n & 0x5555555555555555) + ((n & 0xAAAAAAAAAAAAAAAA) >> 1)
  n = (n & 0x3333333333333333) + ((n & 0xCCCCCCCCCCCCCCCC) >> 2)
  n = (n & 0x0F0F0F0F0F0F0F0F) + ((n & 0xF0F0F0F0F0F0F0F0) >> 4)
  n = (n & 0x00FF00FF00FF00FF) + ((n & 0xFF00FF00FF00FF00) >> 8)
  n = (n & 0x0000FFFF0000FFFF) + ((n & 0xFFFF0000FFFF0000) >> 16)
  n = (n & 0x00000000FFFFFFFF) + ((n & 0xFFFFFFFF00000000) >> 32) # This last & isn't strictly necessary.
  return n

advent_room_descriptions={61: "YOU'RE AT WEST END OF LONG HALL.", 107: 'YOU ARE IN A MAZE OF TWISTY LITTLE PASSAGES, ALL DIFFERENT.', 112: 'YOU ARE IN A LITTLE MAZE OF TWISTING PASSAGES, ALL DIFFERENT.', 131: 'YOU ARE IN A MAZE OF TWISTING LITTLE PASSAGES, ALL DIFFERENT.', 132: 'YOU ARE IN A LITTLE MAZE OF TWISTY PASSAGES, ALL DIFFERENT.', 133: 'YOU ARE IN A TWISTING MAZE OF LITTLE PASSAGES, ALL DIFFERENT.', 134: 'YOU ARE IN A TWISTING LITTLE MAZE OF PASSAGES, ALL DIFFERENT.', 135: 'YOU ARE IN A TWISTY LITTLE MAZE OF PASSAGES, ALL DIFFERENT.', 136: 'YOU ARE IN A TWISTY MAZE OF LITTLE PASSAGES, ALL DIFFERENT.', 137: 'YOU ARE IN A LITTLE TWISTY MAZE OF PASSAGES, ALL DIFFERENT.', 138: 'YOU ARE IN A MAZE OF LITTLE TWISTING PASSAGES, ALL DIFFERENT.', 139: 'YOU ARE IN A MAZE OF LITTLE TWISTY PASSAGES, ALL DIFFERENT.', 140: 'DEAD END',}
advent_room_descriptions={
  #    123456789012345678901
  61: "WEST END OF LONG HALL",
 107: 'MAZE TWISTY LTL PSGS',
 112: 'LTL MAZE TWSTNG PSGS', 
 131: 'MAZE TWSTNG LTL PSGS', 
 132: 'LTL MAZE TWISTY PSGS', 
 133: 'TWSTNG MAZE LTL PSGS', 
 134: 'TWSTNG LTL MAZE PSGS', 
 135: 'TWISTY LTL MAZE PSGS', 
 136: 'TWISTY MAZE LTL PSGS', 
 137: 'LTL TWISTY MAZE PSGS', 
 138: 'MAZE LTL TWSTNG PSGS', 
 139: 'MAZE LTL TWISTY PSGS', 
 140: 'VEND MACH.:PUT COINS',}
maze_room_numbers=list(advent_room_descriptions.keys())[1:-1]
#advent_room_descriptions.update({room+2000:'/'+text for room,text in advent_room_descriptions.items()})
advent_room_descriptions.update({room+2000:''+text for room,text in advent_room_descriptions.items()})

advent_room_descriptions.update({1000:'Select Game: "E"=maze, "N"=Casino',
3061:"YOU'RE BACK AT WEST END OF LONG HALL.",
1061:"YOU DROPPED THE BATTERIES. WEST END OF LONG HALL.",
140:"DEAD END. THERE IS A VENDING MACHINE. PUT COINS IN TO GET BATTERIES.",
2140:"DEAD END. YOU NOW HAVE FRESH BATTERIES.",
0:"None"
})

advent_room_descriptions.update({
  #    123456789012345678901
 1000:'Game:E=Maze, N=Casino',
 3061:"WEST END OF LONG HALL",
 1061:"WEST END OF LONG HALL",
  140:"VEND MACH.: PUT COINS",
 2140:"VEND MACH., BATTERIES",
    0:"None"
})

advent_map={ 29: 134 ,156:136,  20:138,  149:1000,
            153: 139,  24:137, 144:112,  17:140,
             27: 132, 154:133,  18:135,   147:1998, 
            159:1988,  30:131, 150:107,  23:61,
             }
advent_map={0b00_011_101: 134, 0b10_011_100: 136, 0b00_010_100: 138, 0b10_010_101:1000, 
            0b10_011_001: 139, 0b00_011_000: 137, 0b10_010_000: 112, 0b00_010_001: 140, 
            0b00_011_011: 132, 0b10_011_010: 133, 0b00_010_010: 135, 0b10_010_011:1998, 
            0b10_011_111:1988, 0b00_011_110: 131, 0b10_010_110: 107, 0b00_010_111:  61,
            }

advent_map.update({147^128:1999,159^128:1989})#,27^128:1132,18^128:1135})
advent_map.update({id^(128|64):room+2000 for id,room in advent_map.items()})#the "blinking" rooms
advent_edges=[(61, 'S', 107), (107, 'D', 61), (107, 'S', 131), (107, 'U', 135), (107, 'W', 138), (112, 'SE', 135), (112, 'W', 137), (112, 'D', 138), (112, 'S', 140), (131, 'W', 107), (131, 'NW', 133), (131, 'U', 136), (132, 'N', 133), (132, 'D', 139), (133, 'D', 131), (133, 'W', 132), (133, 'SW', 135), (133, 'N', 137), (134, 'D', 136), (134, 'W', 139), (135, 'N', 107), (135, 'U', 112), (135, 'S', 133), (136, 'W', 131), (136, 'D', 134), (136, 'NW', 137), (136, 'SE', 138), (137, 'W', 112), (137, 'D', 133), (137, 'N', 136), (137, 'E', 139), (138, 'D', 107), (138, 'NW', 112), (138, 'S', 136), (139, 'E', 132), (139, 'N', 134), (139, 'U', 137), (140, 'N', 112)]
advent_edges+=[(r,'_',r) for r in maze_room_numbers]

advent_edges=(advent_edges +
             [(room1+2000,action,room2+2000) for room1,action,room2 in advent_edges if not ((room1==107) and (room2==61))])#"blinking" edges

advent_edges.append((1000,'E',61))
advent_edges.append((2107,'D',2061))
advent_edges.append((140,'P',2140))
advent_edges.append((2061,'P', 61))
advent_edges.append((1061,'S', 107))


#advent_edges.append(( 132,'U',1988))
advent_edges.append(( 132,'S',1988))
#advent_edges.append(( 131,'SE',1988))
advent_edges.append(( 131,'SW',1988))
advent_edges.append(( 134,'N',1988))
advent_edges.append(( 134,'NW',1988))
advent_edges.append(( 1989,'_', 134))
advent_edges.append(( 1988,'__',134))
#advent_edges.append(( 1989,'U',131))
advent_edges.append(( 1989,'S',134))
advent_edges.append(( 1989,'NW',132))
advent_edges.append(( 1989,'N',131))
advent_edges.append(( 1989,'SW',134))
#advent_edges.append(( 1989,'SE',132))


#advent_edges.append(( 132,'W',1998))
#advent_edges.append((1998,'W',1999))
#advent_edges.append((1999,'W',1135))
#advent_edges.append(( 135,'D',1998))
#advent_edges.append((1198,'D',1999))
#advent_edges.append((1999,'D',132))
#advent_edges.append((1998,'__', 132))

#Casino: Dice('Put'), Code entry('E'), Direct Addressing ('D')
advent_room_descriptions.update({
4000:"CASINO. ROLL THE DICE (PUT)",
4001:'YOU GOT A "1". YOU NEED A "6". TRY AGAIN.',
4002:'YOU GOT A "2". YOU NEED A "6". TRY AGAIN.',
4003:'YOU GOT A "3". THE CODE IS: "SETUP"',
4004:'YOU GOT A "4". YOU NEED A "6". TRY AGAIN.',
4005:'YOU GOT A "5". YOU NEED A "6". TRY AGAIN.',
4006:'YOU GOT A "6". YOU WIN! TAKE YOUR WINNINGS.',
4007:'CASINO VAULT. ENTER THE CODE. (ROLL THE DICE TO GET THE CODE)',
4010:'YOU HAVE TAKEN IT.',
4011:'THE DICE ARE ROLLING.',
4012:'THE DICE ARE ROLLING.',
4013:'THE DICE ARE ROLLING.',
4014:'THE DICE ARE ROLLING.',
4015:'THE DICE ARE ROLLING.',
4016:'THE DICE ARE ROLLING.',
4017:'CASINO VAULT. ENTER THE CODE.',
4027:'#1 CORRECT. ENTER THE 2ND LETTER OF THE CODE',
4026:'ENTER THE 3RD LETTER OF THE CODE.',
4025:'ENTER THE 4TH LETTER OF THE CODE.',
4024:'ENTER THE NEXT LETTER OF THE CODE.',
4023:'YOU HAVE ENTERED THE CORRECT CODE. THE VAULT IS NOW OPEN.',
4022:'YOU ARE NOW INSIDE THE VAULT. THE DOOR CLOSES BEHIND YOU.',
4037:'#1 CORRECT. ENTER THE 2ND LETTER OF THE CODE',
4036:'ENTER THE 3RD LETTER OF THE CODE.',
4035:'ENTER THE 4TH LETTER OF THE CODE.',
4034:'ENTER THE NEXT LETTER OF THE CODE.',
4033:'YOU HAVE ENTERED THE CORRECT CODE. THE VAULT IS NOW OPEN.'
})
advent_room_descriptions.update({
 #    123456789012345678901
4000:"CASINO: ROLL DICE (P)",
4001:'"1", TRY AGAIN.',
4002:'"2", TRY AGAIN.',
4003:'"3",VAULTCODE="SETUP"',
4004:'"4", TRY AGAIN.',
4005:'"5", TRY AGAIN.',
4006:'"6", YOU WIN! T=EXIT',
4007:'VAULT, ENTER CODE:',
4010:'YOU HAVE TAKEN IT.',
4011:'THE DICE ARE ROLLING.',
4012:'THE DICE ARE ROLLING.',
4013:'THE DICE ARE ROLLING.',
4014:'THE DICE ARE ROLLING.',
4015:'THE DICE ARE ROLLING.',
4016:'THE DICE ARE ROLLING.',
4017:'VAULT, ENTER CODE:',
4027:'ENTER THE 2ND LETTER:',
4026:'ENTER THE 3RD LETTER:',
4025:'ENTER THE 4TH LETTER:',
4024:'ENTER THE NEXT LETTER',
4023:'THE VAULT IS NOW OPEN',
4022:'INSIDE THE VAULT. ',
4037:'ENTER THE 2ND LETTER:',
4036:'ENTER THE 3RD LETTER:',
4035:'ENTER THE 4TH LETTER:',
4034:'ENTER THE NEXT LETTER',
4033:'THE VAULT IS NOW OPEN'
})

advent_map.update({
                5:4000, 132:4006,  12:4005, 141:4004,
               15:4003, 142:4002,   6:4001, 135:4007,
              133:4010,   4:4016, 140:4015,  13:4014,
              143:4013,  14:4012, 134:4011,   7:4017,
              129:4020,   0:4021, 136:4022,   9:4023,
              139:4024,  10:4025, 130:4026,   3:4027,
                1:4030, 128:4031,   8:4032, 137:4033,
               11:4034, 138:4035,   2:4036, 131:4037,
                 })

advent_edges.append((1000,'N', 4000))
advent_edges.append((4000,'T', 4000))
advent_edges.append((4000,'P', 4010))
advent_edges.append((4010,'P', 4006))
advent_edges.append((4011,'P', 4002))
advent_edges.append((4012,'P', 4003))
advent_edges.append((4013,'P', 4004))
advent_edges.append((4014,'P', 4005))
advent_edges.append((4015,'P', 4006))
advent_edges.append((4016,'P', 4001))
advent_edges.append((4001,'P', 4011))
advent_edges.append((4002,'P', 4012))
advent_edges.append((4003,'P', 4013))
advent_edges.append((4004,'P', 4014))
advent_edges.append((4005,'P', 4015))
advent_edges.append((4006,'P', 4016))
advent_edges.append((4006,'T', 4000))
advent_edges.append((4007,'W', 4000))
advent_edges.append((4017,'W', 4000))
advent_edges.append((4000,'E', 4007))
advent_edges.append((4007,'S', 4027))
advent_edges.append((4027,'W', 4007))
advent_edges.append((4027,'E', 4026))
advent_edges.append((4026,'_', 4027))
advent_edges.append((4026,'T', 4025))
advent_edges.append((4025,'_', 4026))
advent_edges.append((4025,'U', 4024))
advent_edges.append((4024,'_', 4025))
advent_edges.append((4024,'P', 4023))
advent_edges.append((4023,'_', 4024))
advent_edges.append((4037,'W', 4007))
advent_edges.append((4036,'W', 4027))
advent_edges.append((4035,'W', 4026))
advent_edges.append((4034,'W', 4025))
advent_edges.append((4033,'W', 4024))
advent_edges.append((4023,'E', 5201))

advent_keymapping={1:'P', 2:'N', 3:'E', 4:'U', 5:'T', 6:'D', 7:'C', 8:'W', 9:'S', 0:'A',
                   10:'NW', 14:'SW', 16:'^T', 17:'SE', 18:'NE', 19:'^P',}
keynames=list(advent_keymapping.values())
advent_room_descriptions.update({5000+i+j+64:f'Room {keyname} {"(pushed)" if count_bits(i+j+64)&1 else "(released)"}' for i,keyname in enumerate(keynames) for j in (0,128)})
advent_map.update({i+j+64:5000+i+j+64 for i in range(len(keynames)) for j in (0,128)})
advent_edges+=[(room1,action,room2) for i in range(len(keynames)) for j in (0,128) for k,action in enumerate(keynames) for room1,room2 in ((5000+i+j+64,5000+k+64),) if not action in ('A','C','^T')]
advent_edges.append((4000,'D',5069))
advent_map2={i^128:room for i,room in advent_map.items()}
advent_map2.update(advent_map)
#advent_imap={j:i for i,j in advent_map.items()} 
advent_imap={j:i for i,j in advent_map2.items()} 
advent_rooms={room:{action:room2 for room1,action,room2 in advent_edges if room1==room} for room in advent_imap}
                   
                   
from collections import namedtuple
pinspec=namedtuple('pinspec','name, input, output')
pinspec.__new__.__defaults__=('',0,0)

class Component(object):
  def __init__(self):
    self.activePins=set()
#class Node(Component):
#  pass
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
  def __init__(self):
    super().__init__()
  def setPin(self,pin,value=1):
    if value:
      self.activePins.add(pin)
    else:
      self.activePins.discard(pin)
#    print(self.activePins)
  def clearPin(self,pin):
    self.setPin(pin,0)
#    self.activePins.discard(pin)
#    print(self.activePins)
  def pinStatus(self,pin):
    return pin in self.activePins

class Eprom1(Eprom):
  KeypadPins=frozenset((23,24,25,26,27))
  keypadLookupTable={
       frozenset(()):None,
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
  pinsForKeys={key:pins for pins,key in keypadLookupTable.items()}
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
      if not parity and key==None:
          data^=1<<7 #key released -> flip msb to make parity even
      elif parity:
        olddata=data
        if mode==2:
            cyclelength=1<<(max(0,(olddata&127).bit_length()-1))
        else:
           cyclelength=128
        if key!=None:
          if key>=0 and key<=9:
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
          bitmask=(cyclelength-1)|64|128
          data=(data&bitmask)|(olddata&(bitmask^255))
      else:
          if key==25: #reset, 3-key combination, e.g. {7,0,6}
            if mode==2:
              data=64
            else:
              data=128
    elif mode==3:
      key=self.key(self.pins_from_address(address))
      action=advent_keymapping.get(key)
      data=address&255
      parity=(count_bits(data)&1)==0
      olddata=data
      room=advent_map.get(data)
      room_actions=advent_rooms.get(room)
      if key==None:
        if not parity:
          data^=1<<7 #key released -> flip msb to make parity even
        elif room_actions:
          if '__' in room_actions:
            newdata=advent_imap.get(room_actions.get('__'))
            if newdata!=None:
              data=newdata
              if (count_bits(data)&1)==1: 
                data^=1<<7

      elif action and room_actions:
        newroom=room_actions.get(action)
        if (newroom==None):
          if not action in ('A','C','^T'):#don't do default action for Alt or Ctrl'
             newroom=room_actions.get('_')#default action
          elif action=='^T':
            newroom=room
        newdata=advent_imap.get(newroom)
        if newdata!=None:
          data=newdata
          if ((count_bits(data)&1)==0):
            data^=1<<7
      else:
          if key==25: #reset, 3-key combination, e.g. {7,0,6}
            data=149^128      
          elif key in ():#flip msb
            if (count_bits(data)&1)==0: 
              data^=1<<7 
      flipped_bits=data^olddata
      if flipped_bits.bit_length()>1:
        for i in range(8):
          if flipped_bits&(1<<i):
            data=olddata^(1<<i) # change only one bit at a time
            break
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
import scene
import ui
import _ui
import math
import time
import threading,queue
import functools
import operator
import scene
class ICNode(scene.ShapeNode):
  def __init__(self,pins=None,size=None,stroke_color='black',*args,**kwargs):
    self.pins=pins
    path=ui.Path.rect(0,0,*size,)
    path.line_width=2
    super().__init__(path=path,stroke_color=stroke_color,*args,**kwargs)
    if pins:
      n=len(pins)
      n2=n//2
      w=self.size[0]/4
      h=self.size[1]/(n2+0.5)
      self.pinnodes=[scene.SpriteNode(
          position=((i//n2)*(self.size[0]-w-4)+2,h*((n2-1-i if i<n2 else i-n2)-n2/4+0.5)+self.size[0]/2),
          size=(w,h-2),
          anchor_point=(0.0,0.0),
          color='blue', 
          parent=self)
          for i in range(n)]
      for i,pn in enumerate(self.pinnodes):
        scene.LabelNode(text=Eprom.pins[i+1][0], position=pn.size/2,font=('Helvetica', 15), color='black',anchor_point=(0.5,0.5),parent=pn)
      scene.LabelNode(text='27C256',position=(self.size[0]/2,self.size[1]*0.75),font=('Helvetica Bold', 16), color='black',anchor_point=(0.5,0.5),parent=self)
      scene.LabelNode(text='U',position=(self.size[0]/2,self.size[1]),font=('Helvetica', 22), color='black',anchor_point=(0.5,0.9),parent=self)
      self.updatePins(set())
  def updatePins(self,ActivePins):
    for i in Eprom.inputpins|Eprom.outputpins:
        self.pinnodes[i-1].color=((0.,1.,0.,1.,),(1.,0.,0.,1.,),)[i in ActivePins]

      
class keyNode(scene.ShapeNode):
    def __init__(self,radius=25,fill_color='white',stroke_color='black',title=None,stroke_width=None,id=None,*args,**kwargs):
      path=ui.Path.oval(0,0,2*radius,2*radius)
      if not stroke_width:
        stroke_width=radius*0.1
      path.line_width=stroke_width
      super().__init__(path=path,fill_color=fill_color,stroke_color=stroke_color,*args,**kwargs)
      titlelines=title.split('\n')
      for i,titleline in enumerate(titlelines):
        fontsize=radius*(0.8 if (len(title)>1) else 1)
        y=((len(titlelines)-1)/2-i)*fontsize*0.9
        if len(titlelines)>1: y-=fontsize*0.2
        if titleline[0]=='{':
          titleline=titleline.strip('{}')
          color='green'
          if len(titlelines)>1:fontsize*=0.8
        elif titleline[0]=='[':
          titleline=titleline.strip('[]')
          color='darkred'
          if len(titlelines)>1:fontsize*=0.8
        else:
          color=stroke_color
          if (len(titleline)==1) and (len(titlelines)>1):
            fontsize/=0.8
        self.label=scene.LabelNode(position=(0,y), anchor_point=(0.5,0.5), text=titleline,font=('Helvetica',fontsize) ,parent=self,color=color)
      self.id=id
    @property
    def title(self):
      return self.label.text
    @title.setter
    def title(self,title):
      self.label.text=title
      
class touchMarker(scene.ShapeNode):
    def __init__(self,radius=20,fill_color=(0,0,0,0.5),stroke_color='clear',title=None,stroke_width=None,id=None,*args,**kwargs):
      path=ui.Path.oval(0,0,2*radius,2*radius)
      if not stroke_width:
        stroke_width=radius*0.1
      path.line_width=stroke_width
      super().__init__(path=path,fill_color=fill_color,stroke_color=stroke_color,*args,**kwargs)

      
class keypadNode(scene.ShapeNode):
    def __init__(self, radius=150, fill_color='white', stroke_color='black',keytitles=None, stroke_width=3,   on_output_change=None,orientation=((1,0),(0,1)),*args, **kwargs):
      path=ui.Path.oval(0,0,2*radius,2*radius)
      if not stroke_width:
        stroke_width=radius*0.1
      path.line_width=stroke_width
      super().__init__(path=path,fill_color=fill_color,stroke_color=stroke_color,*args,**kwargs)
      if not keytitles:
        keytitles=[f'{i}' for i in range(10)]
      self.keys=[keyNode(
          position=self.size/2+(x*orientation[0][0]+y*orientation[0][1],x*orientation[1][0]+y*orientation[1][1]),
          title=keytitles[id],
          id=id,
          parent=self)
        for i in range(4) for j in range(i+1) for id,x,y in (((i*(i+1)//2+j)%10,(2-i)*60,(i/2-j)*70),)]
      self.on_output_change=on_output_change
      self.output=[0]*5
      self.keyid_to_output=[
                 (0,4),
              (0,3),(1,4),
           (0,2),(1,3),(2,4),
        (0,1),(1,2),(2,3),(3,4)]
    def update_output(self,id,inc):
      for i in self.keyid_to_output[id]:
        self.output[i]+=inc
        if (self.output[i]==0) and (inc==-1):
          if self.on_output_change:
            self.on_output_change(i,0)
        if (self.output[i]==1) and (inc==1): 
          if self.on_output_change:
            self.on_output_change(i,1)
    def touch_began(self, touch):
        for node in self.children:
          if type(node)!=keyNode:
            continue
          if (self.point_from_scene(touch.location) in node.frame):
            self.update_output(node.id,+1)
    def touch_moved(self, touch):
        for node in self.children:
          if type(node)!=keyNode:
            continue
          is_inside=self.point_from_scene(touch.location) in node.frame
          was_inside=self.point_from_scene(touch.prev_location) in node.frame
          if is_inside and not was_inside:
            self.update_output(node.id,+1)
          elif was_inside and not is_inside:
            self.update_output(node.id,-1)
    def touch_ended(self, touch):
        for node in self.children:
          if type(node)!=keyNode:
            continue
          if self.point_from_scene(touch.location) in node.frame:
            self.update_output(node.id,-1)
    def reset_touches(self):
      for i in range(len(self.output)):
        if self.output[i]!=0:
          self.output[i]=0
          self.on_output_change(i,0)
        
class MyScene(scene.Scene):
    def setup(self):
            self.did_change_size()
            self.framecount=0
            self.background_color='white'
            self.Eprom= ICNode(pins=Eprom.pins, position=(54,435), size=(145,320), anchor_point=(0,0), color='white', parent=self)     
            self.message=scene.LabelNode(scale=1.0,position=(5,5), anchor_point=(0,0),  text='messagebox '*5,font=('Courier-Bold',20),parent=self,color='black')
            self.messagetext=''
            self.touchmarkers={}
    def touch_began(self,touch): 
       self.touchmarkers[touch]=touchMarker(position=touch.location,anchor_point=(0.5,0.5),parent=self)
       for node in self.children:
            if hasattr(node, 'touch_began'):
                if touch.location in node.frame:
                    node.touch_began(touch)
#       print(f'began {touch.location},{touch.touch_id}')
    def touch_moved(self,touch):
       self.touchmarkers[touch].position=touch.location
       for node in self.children:
            if hasattr(node, 'touch_moved'):
                if touch.location in node.frame:
                    node.touch_moved(touch)

#       print(f'moved {touch.location},{touch.touch_id}')
    def touch_ended(self,touch): 
       self.touchmarkers.pop(touch).remove_from_parent()
       for node in self.children:
            if hasattr(node, 'touch_ended'):
                if touch.location in node.frame:
                    node.touch_ended(touch)
#       print(f'ended {touch.location},{touch.touch_id}')
    def update(self):
      if not self.touches:
        while self.touchmarkers:
          touchmarkers.popitem()[1].remove_from_parent()
        for node in self.children:
            if hasattr(node, 'reset_touches'):
              node.reset_touches()
      self.message.text=self.messagetext
      self.framecount+=1

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
    self.Eprom=Eprom1()
    self.sv=scene.SceneView()
    self.sv.scene=MyScene()
    self.sv.anti_alias = False
    self.sv.frame_interval = 1
    self.sv.multi_touch_enabled = True
    self.sv.shows_fps = True
    self.sv.bg_color=(1,1,1,1)
    v1width=650
    self.view1=ui.View(frame=(256+768-v1width,0,v1width,v1width))
    self.messagetext=''
    shift_y=-24
    self.rbtn1=ui.SegmentedControl(frame=(5.0,340.0+shift_y,304.0,34.0), segments=('auto','xyz','123','maze','hamming'), action= self.rbutton_tapped)
    self.switch1=ui.Switch(frame=(6.0,34.0+shift_y,51.0,31.0),action=self.setPin)
    self.switch1.targetPin=2
    self.switch2=ui.Switch(frame=(197,167+shift_y,51.0,31.0),action=self.setPin)
    self.switch2.targetPin=21
    self.sv.add_subview(self.view1)
    self.sv.add_subview(self.rbtn1)
    self.sv.add_subview(self.switch1)
    self.sv.add_subview(self.switch2)
    self.keypad1=keypadNode(scale=1.15,radius=150,position=(15,35),anchor_point=(0,0),
      keytitles=['inc','y','X','Z','dec','z','r/g','x','Y','../_'], on_output_change=self.keypad_output_changed)
    self.keypad2=keypadNode(scale=1.15,radius=150,position=(15,35),anchor_point=(0,0),
      keytitles=['1','2','3','4','5','6','7','8','9','0'],
      orientation=((0,-1),(1,0),),
      on_output_change=self.keypad_output_changed)
    self.keypad3=keypadNode(scale=1.15,radius=150,position=(15,35),anchor_point=(0,0),
      keytitles=['Put\n{NE}','N','E','[NW]\nU','Take\n{SW}','D\n{SE}','[Ctrl]','W','S','{Alt}'], on_output_change=self.keypad_output_changed)
    scene.LabelNode(position=(-30,-120), anchor_point=(0,0), text='Reset: [Ctrl Alt D]',font=('Helvetica',15),parent=self.keypad3,color='black')
    self.mode=0
    self.key=''
    self.scene_view = scn.View((0,0,self.view1.frame[2],self.view1.frame[3]), superView=self.view1)
    self.scene_view.allowsCameraControl = True
    
    self.scene_view.scene = scn.Scene()
    
    self.scene_view.delegate = self
    
    self.root_node = self.scene_view.scene.rootNode
    
    self.camera_node = scn.Node()
    self.camera_node.camera = scn.Camera()
    self.camera_node.position = (-10,1.5,2)
    self.camera_node.camera.focalLength=70
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
    self.oldindex=0
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
    
    self.sv.present(orientations= ['landscape'])
    
  def keypad_output_changed(self,i,value):
    self.q.put((0,next(id),(lambda pin,value:lambda:self.Eprom.setPin(pin,value))(27-i,value)))
  def reset_leds(self):
      for led_plane in self.led_nodes:
        for led_row in led_plane:
          for led in led_row:
            led.setGeometry(self.off_led)
      for wire_plane in self.wire_nodes:
        for wire_row in wire_plane:
          for wire in wire_row:
            wire.setGeometry(self.off_wire)
      return
      
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
        xwire,ywire,led=((self.neg_wire,self.pos_wire,self.green_led),(self.pos_wire,self.neg_wire,self.red_led))[ic]
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
      
    update_Led(self.oldindex,on=False) 
    if self.mode==4:
      for i in [0, 7, 25, 30, 42, 45, 51, 52, 75, 76, 82, 85, 97, 102, 120, 127]:
        update_Led(i^(64|128) if i & 64 else i,on=True)
      return

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
    self.oldindex=self.index
    self.sv.scene.Eprom.updatePins(self.Eprom.activePins)
    ad_index=advent_map2.get(self.index)
    ad_description=advent_room_descriptions.get(advent_map2.get(self.index))
    self.sv.scene.messagetext=f'{self.Eprom.key() if self.Eprom.key()!=None else -6:2d}\n'+ f'{count_bits(self.index)&1}{advent_keymapping.get(self.Eprom.key())  or "":2s}\n{self.index:3d}\n{self.index:08b}\n'+(f'{ad_index:3d} {ad_description.lower()}'if ad_index and ad_description else '')
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
    
  def rbutton_tapped(self,sender):
    self.mode=sender.selected_index
    self.reset_leds()
    if self.mode==0:
      self.keypad3.remove_from_parent()
      self.keypad2.remove_from_parent()
      self.keypad1.remove_from_parent()
    elif self.mode==1:
      self.keypad3.remove_from_parent()
      self.keypad2.remove_from_parent()
      self.sv.scene.add_child(self.keypad1)
    elif self.mode==2:
      self.keypad3.remove_from_parent()
      self.sv.scene.add_child(self.keypad2)
      self.keypad1.remove_from_parent()
    elif self.mode==3:
      self.switch1.value=1
      self.setPin(self.switch1)
      self.switch2.value=1
      self.setPin(self.switch2)
      def setindex(self,index): self.index=index; yield
      self.q.put((0,next(id),setindex(self,149)))
      self.keypad1.remove_from_parent()
      self.keypad2.remove_from_parent()
      self.sv.scene.add_child(self.keypad3)
    elif self.mode==4:
      self.keypad1.remove_from_parent()
      self.keypad2.remove_from_parent()
      self.keypad3.remove_from_parent()
    
    
  def setPin(self,sender):
    if sender.value:
      self.Eprom.setPin(sender.targetPin)
    else:
      self.Eprom.clearPin(sender.targetPin)
      
def  make_descriptions():
  result=[f'{index:d}' for index in range(256)]
  for index in range(256):
    ad_index=advent_map2.get(index) or advent_map2.get(index^128)
    ad_description=advent_room_descriptions.get(ad_index)
    if ad_index and ad_description:
      result[index]=ad_description
  return result

if __name__=='__main__':
  D=Demo()  
  D.main()
  
#x=[D.Eprom.data_from_address(a^255)^255 for a in range(1<<15)] #inverted data
#with open('LedCubeA.bin','wb') as f: f.write(bytes(x))
