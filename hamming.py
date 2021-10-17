def bitcount(n):
  n = (n & 0x5555555555555555) + ((n & 0xAAAAAAAAAAAAAAAA) >> 1)
  n = (n & 0x3333333333333333) + ((n & 0xCCCCCCCCCCCCCCCC) >> 2)
  n = (n & 0x0F0F0F0F0F0F0F0F) + ((n & 0xF0F0F0F0F0F0F0F0) >> 4)
  n = (n & 0x00FF00FF00FF00FF) + ((n & 0xFF00FF00FF00FF00) >> 8)
  n = (n & 0x0000FFFF0000FFFF) + ((n & 0xFFFF0000FFFF0000) >> 16)
  n = (n & 0x00000000FFFFFFFF) + ((n & 0xFFFFFFFF00000000) >> 32) # This last & isn't strictly necessary.
  return n
  
def insert_bit(i,j):
  im=i&((1<<(j))-1)
  return ((i^im)<<1)|im
  
def hamming(i):
  bl=i.bit_length()#number of significant data bits
  np=0 #number of parity bits
  result=0
  while True:
    pb=(1<<np)-1# bit position of the next parity bit
    if bl<pb: #break if there are no more bits to encode
      break
    i=insert_bit(i,pb)#make room for the parity bits, and push data bits into the correct position
    np+=1
    bl+=1
  p=hamming_check(i) #calculate the parity bits
  for j in range(np): #fill the parity bits in
    pb=(1<<j)-1
    i|=(p&1)<<pb
    p>>=1
  return i
    
def hamming_check(i):
  m=i.bit_length()
  p=0
  for j in range(1,m+1):
    if i&1: p^=j #calculate all parity bits in parallel according to the hamming scheme
    i>>=1
  return p

def hamming_data(i):
  np=i.bit_length().bit_length()
  result=0
  for j in range(1,np):
    bl=1<<j
    mask=((1<<bl)-2)<<(bl-1)
    result|=(i&mask)>>(j+1)
  return result
  
  
def hamming_distance(i,j):
  return bitcount(i^j)
  
def dehamming(i):
  error_pos=hamming_check(i)
  if error_pos!=0:
    i^=1<<(error_pos-1)
  return hamming_data(i)

