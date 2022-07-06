from zkwordle.util import Variable, fpoly1d, inner
from zkwordle.ecc import e, G2

def verify(a, r, verification_key, proof):

  vars = {'v1': 1}

  for i in range(5):
    for j in range(5):
      vars[f'a{i}{j}'] = (a[i] >> j) & 1 
    vars[f'r{i}'] = r[i]

  l_pub = inner(vars, verification_key['l_pub'])

  if not e(proof['l'], verification_key['l']) == e(proof['ls'], G2):
    return False
  if not e(verification_key['r'], proof['r']) == e(proof['rs'], G2):
    return False
  if not e(proof['o'], verification_key['o']) == e(proof['os'], G2):
    return False
  
  if not e(proof['k'], verification_key['g']) == e(l_pub + proof['l'] + proof['o'], verification_key['bg_2']) * e(verification_key['bg_1'], proof['r']):
    return False

  if not e(l_pub + proof['l'], proof['r']) == e(proof['h'], verification_key['t']) * e(proof['o'], G2):
    return False

  return True
    
