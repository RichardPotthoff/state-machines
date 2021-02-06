from PIL import Image,ImageOps
from functools import reduce
import operator

def grayToInt(gray):
  mask=gray>>1
  result=gray
  while mask!=0:
    result^=mask
    mask>>=1
  return result

def intToGray(i):
  return i^(i>>1)


ascii_8x6_bitmap=[None]*256
i=0
with open('ASCII_8x6.txt','r',encoding='utf8') as f:
  for l in f.readlines():
    try:
      l.strip()
      l=l.split('//')[0]
      fields=l.strip(',{} ').split(',')
      ascii_8x6_bitmap[i]=[int(field,base=16) for field in fields]
      i+=1
    except:
      pass
      
#2-bit binary character bitmaps (00,01,10,11):
ascii_8x6_bitmap[240:244]=[[0, 6 if i & 2 else 48, 0, 0, 6 if i&1 else 48,0] for i in range(4)]
#7-segment digit bitmaps (0,1,2,3,4,5,6,7,8,9,A,b,C,d,E,F):
A,B,C,D,E,F,G,P=(0,1,1,1,1,0),(0,0,0,0,15,0),(0,0,0,0,120,0),(0,64,64,64,64,0),(0,120,0,0,0,0),(0,15,0,0,0,0),(0,8,8,8,8,0),(0,0,0,0,0,128)
ascii_8x6_bitmap[224:240]=[[reduce(operator.__or__,y) for y in zip(*c)] for c in ({A,B,C,D,E,F},{B,C},{A,B,D,E,G},{A,B,C,D,G},{B,C,F,G},{A,C,D,F,G},{A,C,D,E,F,G},{A,B,C},{A,B,C,D,E,F,G},{A,B,C,D,F,G},{A,B,C,E,F,G},{C,D,E,F,G},{A,D,E,F},{B,C,D,E,G},{A,D,E,F,G},{A,E,F,G},)]

def fbin(i):
  s=''
  while i:
    s=chr((i&3)+240)+s
    i>>=2
  return s   
def fhex(i):
  s=''
  while i:
    s=chr((i&15)+224)+s
    i>>=4
  return s   

ps=2
s=('TWSTY LTL MZ OF PSGS.'+' '*21)[:21]

rom=[None]*256

#128 pixel wide by 8 pixel high text: binary, hex, decimal, and decoded gray of inverted A0..A7.
#D0(top)..D6(bottom) are the text pixels(inverted), D7(underline) is the parity of A0..A7 (low=odd)

lines=[f' {fbin(256+j)[1:]}b {fhex(256+j)[1:]}h {j:3d}d {i:3d}g ' for i in range(256) for j in (i^(i>>1),)]

for i,line in enumerate(lines):
  line=line[:128//6+1]
  x=([b for c in line for b in  ascii_8x6_bitmap[ord(c)] ])
  if len(x)>128:
    x=x[:128]
  else:
    x+=[0]*(128-len(x))#pad with zeroes
  rom[intToGray(i)^255]=[(x[grayToInt(k^127)]|((i%2)*(1<<7)))^255 for k in range(128)]#set bit 7 for odd parity
  
#
ROM=[]
for line in zip(*rom):#transpose and flatten array
  ROM.extend(line)


#with open('ascii_8_6bitmap.bin','wb') as f: f.write(bytes(ROM))
#with open('ascii_8_6bitmap.bin','rb') as f:  ROM=list(bytearray(f.read()))
def getpixel(code,row,column,ROM=ROM):
  return (ROM[((column^(column>>1)^127)<<8)+code^255]>>row)&1

for j in (0,1,2,3,42,255):
  code=j^(j>>1)
  print('\n'.join([''.join(['8' if getpixel(code,row,column)==0 else ' ' for column in range(4,123)]) for row in range(8)]))
  print()
  
