import sys

def hanoi(num_disks, start, end, temp):
  print "[", num_disks, start, "->", end, ",", temp
  moves = 0
  if num_disks > 1:
    moves += hanoi(num_disks - 1, start, temp, end)
  print "move 1 from", start, "to", end
  moves += 1
  if num_disks > 1:
    moves += hanoi(num_disks - 1, temp, end, start)
  return moves

if __name__ == "__main__":
  num_moves = hanoi(int(sys.argv[1]), 'A', 'C', 'B')
  print num_moves
