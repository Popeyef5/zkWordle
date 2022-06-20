#!usr/bin/env python3

from zkwordle.util import VariablePolynomial, fpoly1d, prime

def verify(polys_df, verifying_df, proof_df):
  
  polys_df.fillna(0, inplace=True)
  proof_df.fillna(0, inplace=True)

  proof = {var: proof_df[var][0] for var in proof_df}

  polys = {
    'l': proof['l'],
    'r': proof['r'],
    'o': proof['o'],
    'h': proof['h'],
    't': verifying_df['t'][0],
  }

  s = verifying_df['s'][0]

  for _, row in polys_df.iterrows():
    variable, type, visibility, *coeffs = row
    if visibility == VariablePolynomial.PRIVATE:
      continue
    try:
      value = proof[variable]
    except KeyError:
      return False
    coeffs = list(map(int, coeffs))
    poly = fpoly1d(coeffs)
    poly *= value
    polys[type] += poly(s)

  if (polys['l'] * polys['r'] - polys['h'] * polys['t'] - polys['o']) % prime:
    return False

  return True
    
