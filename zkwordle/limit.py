import sys
import re

if not len(sys.argv) > 1:
  print("input file name")
  exit(0)

cutoff = int(sys.argv[1])
input = sys.argv[2]

if not len(sys.argv) > 3:
  output = input
else:
  output = sys.argv[3]

with open(input, 'r') as f:
  data = f.readlines()

# Edit lines
modded = 0
for i, line in enumerate(data):
  commented = False
  if line.replace(' ', '').startswith('#'):
    commented = True
  
  numbers = [int(n) for n in re.findall('\d+', line)]

  if not len(numbers) or line.startswith("#!/") or "def" in line:
    continue

  if "R1CS_LENGTH" in line and not commented:
    data[i] = f"R1CS_LENGTH = {cutoff}\n"
    continue

  if any(n > cutoff for n in numbers) and not commented:
    data[i] = "#" + line
    if not line.rstrip().endswith(",") and not data[i+1].lstrip().rstrip() == "]":
      data.insert(i+1,  " " * (len(line) - len(line.lstrip())) + "pass\n")
      modded += 1
  elif all(n <= cutoff for n in numbers) and commented:
    data[i] = line[1:]
    if data[i+1].lstrip().startswith("pass"):
      del(data[i+1])

      
  

with open(output, 'w') as f:
  f.writelines(data)
    