from zkwordle.util import Variable, fpoly1d, prime

def verify(setup_polys, verification_key, proof):
  
  polys = {
    'l': proof['l'],
    'r': proof['r'],
    'o': proof['o'],
    'h': proof['h'],
    't': verification_key['t'],
  }

  s = verification_key['s']

  for item in setup_polys:
    if item.visibility == Variable.PRIVATE:
      continue
    try:
      value = proof[item.name]
    except KeyError:
      return False
    for type, coeffs in item.polys.items():
      poly = fpoly1d(coeffs)
      poly *= value
      polys[type] += poly(s)

  if (polys['l'] * polys['r'] - polys['h'] * polys['t'] - polys['o']) % prime:
    return False

  return True
    
