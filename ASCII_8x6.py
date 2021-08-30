from PIL import Image,ImageOps
from functools import reduce
import operator

def count_bits(n):
  n = (n & 0x5555555555555555) + ((n & 0xAAAAAAAAAAAAAAAA) >> 1)
  n = (n & 0x3333333333333333) + ((n & 0xCCCCCCCCCCCCCCCC) >> 2)
  n = (n & 0x0F0F0F0F0F0F0F0F) + ((n & 0xF0F0F0F0F0F0F0F0) >> 4)
  n = (n & 0x00FF00FF00FF00FF) + ((n & 0xFF00FF00FF00FF00) >> 8)
  n = (n & 0x0000FFFF0000FFFF) + ((n & 0xFFFF0000FFFF0000) >> 16)
  n = (n & 0x00000000FFFFFFFF) + ((n & 0xFFFFFFFF00000000) >> 32) # This last & isn't strictly necessary.
  return n

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
lines=[['0                    ', '1                    ', 'ENTER THE 3RD LETTER:', 'ENTER THE 2ND LETTER:', 'THE DICE ARE ROLLING.', 'CASINO: ROLL DICE (P)', '"1", TRY AGAIN.      ', 'VAULT, ENTER CODE:   ', '8                    ', 'THE VAULT IS NOW OPEN', 'ENTER THE 4TH LETTER:', 'ENTER THE NEXT LETTER', '"5", TRY AGAIN.      ', 'THE DICE ARE ROLLING.', 'THE DICE ARE ROLLING.', '"3",VAULTCODE="SETUP"', 'LTL MAZE TWSTNG PSGS ', 'VEND MACH.: PUT COINS', 'TWISTY LTL MAZE PSGS ', '19                   ', 'MAZE LTL TWSTNG PSGS ', 'Game:E=Maze, N=Casino', 'MAZE TWISTY LTL PSGS ', 'WEST END OF LONG HALL', 'LTL TWISTY MAZE PSGS ', 'MAZE LTL TWISTY PSGS ', 'TWSTNG MAZE LTL PSGS ', 'LTL MAZE TWISTY PSGS ', 'TWISTY MAZE LTL PSGS ', 'TWSTNG LTL MAZE PSGS ', 'MAZE TWSTNG LTL PSGS ', '31                   ', '32                   ', '33                   ', '34                   ', '35                   ', '36                   ', '37                   ', '38                   ', '39                   ', '40                   ', '41                   ', '42                   ', '43                   ', '44                   ', '45                   ', '46                   ', '47                   ', '48                   ', '49                   ', '50                   ', '51                   ', '52                   ', '53                   ', '54                   ', '55                   ', '56                   ', '57                   ', '58                   ', '59                   ', '60                   ', '61                   ', '62                   ', '63                   ', 'Room P (pushed)      ', 'Room N (released)    ', 'Room E (released)    ', 'Room U (pushed)      ', 'Room T (released)    ', 'Room D (pushed)      ', 'Room C (pushed)      ', 'Room W (released)    ', 'Room S (released)    ', 'Room A (pushed)      ', 'Room NW (pushed)     ', 'Room SW (released)   ', 'Room ^T (pushed)     ', 'Room SE (released)   ', 'Room NE (released)   ', 'Room ^P (pushed)     ', 'LTL MAZE TWSTNG PSGS ', 'VEND MACH., BATTERIES', 'TWISTY LTL MAZE PSGS ', '83                   ', 'MAZE LTL TWSTNG PSGS ', '85                   ', 'MAZE TWISTY LTL PSGS ', 'WEST END OF LONG HALL', 'LTL TWISTY MAZE PSGS ', 'MAZE LTL TWISTY PSGS ', 'TWSTNG MAZE LTL PSGS ', 'LTL MAZE TWISTY PSGS ', 'TWISTY MAZE LTL PSGS ', 'TWSTNG LTL MAZE PSGS ', 'MAZE TWSTNG LTL PSGS ', '95                   ', '96                   ', '97                   ', '98                   ', '99                   ', '100                  ', '101                  ', '102                  ', '103                  ', '104                  ', '105                  ', '106                  ', '107                  ', '108                  ', '109                  ', '110                  ', '111                  ', '112                  ', '113                  ', '114                  ', '115                  ', '116                  ', '117                  ', '118                  ', '119                  ', '120                  ', '121                  ', '122                  ', '123                  ', '124                  ', '125                  ', '126                  ', '127                  ', '128                  ', '129                  ', 'ENTER THE 3RD LETTER:', 'ENTER THE 2ND LETTER:', '"6", YOU WIN! T=EXIT ', 'YOU HAVE TAKEN IT.   ', 'THE DICE ARE ROLLING.', 'VAULT, ENTER CODE:   ', 'INSIDE THE VAULT.    ', 'THE VAULT IS NOW OPEN', 'ENTER THE 4TH LETTER:', 'ENTER THE NEXT LETTER', 'THE DICE ARE ROLLING.', '"4", TRY AGAIN.      ', '"2", TRY AGAIN.      ', 'THE DICE ARE ROLLING.', 'LTL MAZE TWSTNG PSGS ', 'VEND MACH.: PUT COINS', 'TWISTY LTL MAZE PSGS ', '147                  ', 'MAZE LTL TWSTNG PSGS ', 'Game:E=Maze, N=Casino', 'MAZE TWISTY LTL PSGS ', 'WEST END OF LONG HALL', 'LTL TWISTY MAZE PSGS ', 'MAZE LTL TWISTY PSGS ', 'TWSTNG MAZE LTL PSGS ', 'LTL MAZE TWISTY PSGS ', 'TWISTY MAZE LTL PSGS ', 'TWSTNG LTL MAZE PSGS ', 'MAZE TWSTNG LTL PSGS ', '159                  ', '160                  ', '161                  ', '162                  ', '163                  ', '164                  ', '165                  ', '166                  ', '167                  ', '168                  ', '169                  ', '170                  ', '171                  ', '172                  ', '173                  ', '174                  ', '175                  ', '176                  ', '177                  ', '178                  ', '179                  ', '180                  ', '181                  ', '182                  ', '183                  ', '184                  ', '185                  ', '186                  ', '187                  ', '188                  ', '189                  ', '190                  ', '191                  ', 'Room P (released)    ', 'Room N (pushed)      ', 'Room E (pushed)      ', 'Room U (released)    ', 'Room T (pushed)      ', 'Room D (released)    ', 'Room C (released)    ', 'Room W (pushed)      ', 'Room S (pushed)      ', 'Room A (released)    ', 'Room NW (released)   ', 'Room SW (pushed)     ', 'Room ^T (released)   ', 'Room SE (pushed)     ', 'Room NE (pushed)     ', 'Room ^P (released)   ', 'LTL MAZE TWSTNG PSGS ', 'VEND MACH., BATTERIES', 'TWISTY LTL MAZE PSGS ', '211                  ', 'MAZE LTL TWSTNG PSGS ', '213                  ', 'MAZE TWISTY LTL PSGS ', 'WEST END OF LONG HALL', 'LTL TWISTY MAZE PSGS ', 'MAZE LTL TWISTY PSGS ', 'TWSTNG MAZE LTL PSGS ', 'LTL MAZE TWISTY PSGS ', 'TWISTY MAZE LTL PSGS ', 'TWSTNG LTL MAZE PSGS ', 'MAZE TWSTNG LTL PSGS ', '223                  ', '224                  ', '225                  ', '226                  ', '227                  ', '228                  ', '229                  ', '230                  ', '231                  ', '232                  ', '233                  ', '234                  ', '235                  ', '236                  ', '237                  ', '238                  ', '239                  ', '240                  ', '241                  ', '242                  ', '243                  ', '244                  ', '245                  ', '246                  ', '247                  ', '248                  ', '249                  ', '250                  ', '251                  ', '252                  ', '253                  ', '254                  ', '255                  '][j] for i in range(256) for j in (i^(i>>1),)]

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

for j in (23,22,156,146,18):
  code=j#^(j>>1)
  print('\n'.join([''.join(['#' if getpixel(code,row,column)==0 else ' ' for column in range(0,119)]) for row in range(8)]))
  print()
print ('average lit pixels in font:',sum([count_bits(b) for c in ascii_8x6_bitmap[32:] for b in c])/(7*(len(ascii_8x6_bitmap)-32)*6))
print ('average lit pixels in ROM:',1.0-sum([count_bits(b) for b in ROM])/(8*len(ROM)))
