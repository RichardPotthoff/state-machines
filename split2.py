#! /usr/local/bin/python3
import sys,getopt
def main(argv):
  start=0
  end=None
  try:
     opts, args = getopt.getopt(argv[1:],"s:e:",longopts=["start=", "end="])
  except getopt.GetoptError:
     print( f'{os.path.basename(argv[0])} [-s start -e end]')
     sys.exit(2)
  for opt,arg in opts:
    if opt in ("-e","--end"):
      end=eval(arg)
    if opt in ("-s","--start"):
      start=eval(arg)
  sys.stdin.buffer.read(start)
  sys.stdout.buffer.write(sys.stdin.buffer.read() if end==None else sys.stdin.buffer.read(end-start))
  
#  print(f"start={start:04x}, end={end:04x}")
if __name__ == '__main__':
  main(sys.argv)

