from PIL import Image,ImageOps
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
ps=6
s=('TWSTY LTL MZ OF PSGS.'+' '*21)[:21]
for i in range(8):
  s=''.join((chr(j) for j in range(32*i,32*(i+1))))
  data=bytes([255 if ((1<<i) & j) else 0 for i in range(8) for _ in range(ps) for c in s for j in  ascii_8x6_bitmap[ord(c)] for _ in range(ps) ])
  im=Image.fromstring('L',(len(s)*6*ps,8*ps),data)
  im.show()

