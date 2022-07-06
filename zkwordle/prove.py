from zkwordle.util import fpoly1d, Variable, inner
from zkwordle.ecc import curve_order
import secrets


def prove(a, w, r, proving_key, variable_polys, deltas=None):

  assert len(a) == 5
  assert len(w) == 5
  assert len(r) == 5

  vars = {}
  
  polys = {'l': fpoly1d(0), 'r': fpoly1d(0), 'o': fpoly1d(0)}
  
  def register(name, value):
    vars[name] = value
    polys['l'] += value * variable_polys[name]['l']
    polys['r'] += value * variable_polys[name]['r']
    polys['o'] += value * variable_polys[name]['o']

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

  if deltas is None:
    deltas = {
      'l': secrets.randbelow(curve_order),
      'r': secrets.randbelow(curve_order),
      'o': secrets.randbelow(curve_order)
    }

  proof = {
    'l': inner(vars, proving_key['l']) + deltas['l'] * proving_key['lt'],
    'ls': inner(vars, proving_key['ls']) + deltas['l'] * proving_key['lts'],
    'r': inner(vars, proving_key['r']) + deltas['r'] * proving_key['rt'],
    'rs': inner(vars, proving_key['rs']) + deltas['r'] * proving_key['rts'],
    'o': inner(vars, proving_key['o']) + deltas['o'] * proving_key['ot'],
    'os': inner(vars, proving_key['os']) + deltas['o'] * proving_key['ots'],
    'k': inner(vars, proving_key['k']) + deltas['l'] * proving_key['ltb'] + deltas['r'] * proving_key['rtb'] + deltas['o'] * proving_key['otb']
  }

  t = fpoly1d([1])
  for i in range(1, 356):
    t *= fpoly1d([1, -i])

  p = (polys['l'] + deltas['l'] * t) * (polys['r'] + deltas['r'] * t) - polys['o'] - deltas['o'] * t

  h, q = p / t

  proof['h'] = inner({i: h.coeffs[-1-i] for i in range(len(h.coeffs))}, proving_key['h'])

  return proof

