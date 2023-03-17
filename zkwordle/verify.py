from zkwordle.util import Variable, fpoly1d, inner
from zkwordle.ecc import e, G2

def verify(a, W, r, verification_key, proof):
  print("Starting verification")
  import time
  st = time.monotonic()
  vars = {'v1': 1}

  for i in range(5):
    for j in range(5):
      vars[f'a{i}{j}'] = (a[i] >> j) & 1 
    vars[f'r{i}'] = r[i]

  vars['Wx'] = W[0]
  vars['Wy'] = W[1]

  l_pub = inner(vars, verification_key['l_pub'])

  if not e(proof['l'], verification_key['l']) == e(proof['ls'], G2):
    print(f"Verification failed in {time.monotonic()-st}s. LprivxLpub")
    return False
  if not e(verification_key['r'], proof['r']) == e(proof['rs'], G2):
    print(f"Verification failed in {time.monotonic()-st}s. RprivxRpub")
    return False
  if not e(proof['o'], verification_key['o']) == e(proof['os'], G2):
    print(f"Verification failed in {time.monotonic()-st}s. OprivxOpub")
    return False
  
  if not e(proof['k'], verification_key['g']) == e(l_pub + proof['l'] + proof['o'], verification_key['bg_2']) * e(verification_key['bg_1'], proof['r']):
    print(f"Verification failed in {time.monotonic()-st}s. Weird part")
    return False

  if not e(l_pub + proof['l'], proof['r']) == e(proof['h'], verification_key['t']) * e(proof['o'], G2):
    print(f"Verification failed in {time.monotonic()-st}s. Invalid proof")
    return False

  # print("l_pub:", verification_key['l_pub'])
  # print("proof['l']:", proof['l'])
  # print("proof['r']:", proof['r'])
  # print("proof['h']:", proof['h'])
  # print("verification_key['t']:", verification_key['t'])
  # print("proof['o']:", proof['o'])

  et = time.monotonic()
  print(f"Finished verification in {et-st}s.")
  return True
    
