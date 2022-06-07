#!/usr/bin/env python3

from zkwordle.util import fpoly1d

def prove(a, w, r, df=None, csv=''):
  import pandas as pd

  assert len(a) == 5
  assert len(w) == 5
  assert len(r) == 5

  if df is None:
    if csv:
      df = pd.read_csv(csv, index_col=0)
    else:
      return False

  df.fillna(0, inplace=True)
   
  vars = {}
  
  def register(name, value):
    vars[name] = value

  register('v1', 1)

  for i in range(5):
    for j in range(5):
      register(f'a{i}{j}', (a[i] >> j) & 1) 
      register(f'w{i}{j}', (w[i] >> j) & 1) 
    register(f'w{i}34', vars.get(f'w{i}3') * vars.get(f'w{i}4'))
    register(f'w{i}12', vars.get(f'w{i}1') * (vars.get(f'w{i}2') - vars.get('v1')))

    register(f'r{i}', r[i])
    register(f'r{i}2', r[i]*r[i])

    register(f'rho{i}0', (vars.get(f'r{i}') - 1) * (vars.get(f'r{i}') - 2))
    register(f'rho{i}1', vars.get(f'r{i}') * (vars.get(f'r{i}') - 2))
    register(f'rho{i}2', vars.get(f'r{i}') * (vars.get(f'r{i}') - 1))

  for i in range(5):
    for j in range(5):
      register(f'P{i}{j}01', (vars.get(f'a{i}0') + vars.get(f'w{j}0') - vars.get('v1')) * \
        (vars.get(f'a{i}1') + vars.get(f'w{j}1') - vars.get('v1'))) 

      register(f'P{i}{j}23', (vars.get(f'a{i}2') + vars.get(f'w{j}2') - vars.get('v1')) * \
        (vars.get(f'a{i}3') + vars.get(f'w{j}3') - vars.get('v1'))) 

      register(f'P{i}{j}0123', vars.get(f'P{i}{j}01') * vars.get(f'P{i}{j}23'))

      register(f'P{i}{j}', vars.get(f'P{i}{j}0123') * (vars.get(f'a{i}4') + vars.get(f'w{j}4') - vars.get('v1'))) 

      register(f'P{i}{j}2', vars.get(f'P{i}{j}') * vars.get(f'P{i}{j}'))

    for j in range(i):
      register(f'S{i}{j}01', (vars.get(f'a{i}0') + vars.get(f'a{j}0') - vars.get('v1')) * \
        (vars.get(f'a{i}1') + vars.get(f'a{j}1') - vars.get('v1'))) 

      register(f'S{i}{j}23', (vars.get(f'a{i}2') + vars.get(f'a{j}2') - vars.get('v1')) * \
        (vars.get(f'a{i}3') + vars.get(f'a{j}3') - vars.get('v1'))) 

      register(f'S{i}{j}0123', vars.get(f'S{i}{j}01') * vars.get(f'S{i}{j}23'))

      register(f'S{i}{j}', vars.get(f'S{i}{j}0123') * (vars.get(f'a{i}4') + vars.get(f'a{j}4') - vars.get('v1'))) 

      register(f'S{i}{j}2', vars.get(f'S{i}{j}') * vars.get(f'S{i}{j}'))

  for i in range(5):
    for j in range(5):
      register(f'Dp{i}{j}', vars.get(f'P{i}{j}2') * (vars.get('v1') - vars.get(f'P{j}{j}2')))

    for j in range(i):
      register(f'Dm{i}{j}', vars.get(f'S{i}{j}2') * (vars.get('v1') - vars.get(f'P{j}{j}2')))

    register(f'T{i}12', (sum([vars.get(f'Dp{i}{j}') for j in range(5)]) - sum([vars.get(f'Dm{i}{j}') for j in range(i)]) - 1 * vars.get('v1')) * \
      (sum([vars.get(f'Dp{i}{j}') for j in range(5)]) - sum([vars.get(f'Dm{i}{j}') for j in range(i)]) - 2 * vars.get('v1'))) 
    register(f'T{i}34', (sum([vars.get(f'Dp{i}{j}') for j in range(5)]) - sum([vars.get(f'Dm{i}{j}') for j in range(i)]) - 3 * vars.get('v1')) * \
      (sum([vars.get(f'Dp{i}{j}') for j in range(5)]) - sum([vars.get(f'Dm{i}{j}') for j in range(i)]) - 4 * vars.get('v1'))) 
    register(f'T{i}08', (sum([vars.get(f'Dp{i}{j}') for j in range(5)]) - sum([vars.get(f'Dm{i}{j}') for j in range(i)])) * \
      (sum([vars.get(f'Dp{i}{j}') for j in range(5)]) - sum([vars.get(f'Dm{i}{j}') for j in range(i)]) + 1 * vars.get('v1'))) 
    register(f'T{i}76', (sum([vars.get(f'Dp{i}{j}') for j in range(5)]) - sum([vars.get(f'Dm{i}{j}') for j in range(i)]) + 2 * vars.get('v1')) * \
      (sum([vars.get(f'Dp{i}{j}') for j in range(5)]) - sum([vars.get(f'Dm{i}{j}') for j in range(i)]) + 3 * vars.get('v1'))) 
    register(f'T{i}0876', vars.get(f'T{i}08') * vars.get(f'T{i}76'))
    register(f'Tp{i}', vars.get(f'T{i}12') * vars.get(f'T{i}34'))
    register(f'Tm{i}', vars.get(f'T{i}0876') * (sum([vars.get(f'Dp{i}{j}') for j in range(5)]) - sum([vars.get(f'Dm{i}{j}') for j in range(i)]) + 4 * vars.get('v1')))

    register(f'c{i}0', vars.get(f'rho{i}0') * vars.get(f'Tm{i}'))
    register(f'c{i}1', vars.get(f'rho{i}1') * (vars.get(f'Tp{i}') + vars.get(f'P{i}{i}2')))
    register(f'c{i}2', vars.get(f'rho{i}2') * (vars.get('v1') - vars.get(f'P{i}{i}2')))

  polys = {}
  polys['l'] = fpoly1d(0)
  polys['r'] = fpoly1d(0)
  polys['o'] = fpoly1d(0)

  debug_polys = []
     
  for _, row in df.iterrows():
    variable, type, *coeffs = row 
    value = vars.get(variable)
    coeffs = list(map(int, coeffs))
    poly = fpoly1d(coeffs)
    debug_polys.append((fpoly1d(poly), variable, type, value))
    poly *= value
    polys[type] += poly

  poly = polys['l'] * polys['r'] - polys['o']

  t = fpoly1d([1, -1])
  for i in range(2, 356):
    t *= fpoly1d([1, -i])

  h, q = poly / t

  if q != fpoly1d(0):
    print('/'*100)
    print(f"Discrepancies found using a:{''.join([chr(l+97) for l in a])}, w:{''.join([chr(l+97) for l in w])} and r:{r}. Conflictive points:")
    count = 0
    for i in range(1, 356):
      eval = poly(i)
      if eval:
        print('/'*100)
        print(i, eval)
        print("Nonzero polynomials at the point:")
        for dp, var, t, v in debug_polys:
          if dp(i):
            print('Var:', var, 'Type:', t, 'Value:', v, 'Coeff:', dp(i))
        count += 1 
    print('Errors:', count)
    return False

  return True

