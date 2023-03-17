from zkwordle.util import fpoly1d, Variable, inner, mod_inv
from zkwordle.ecc import curve_order, bjj
from zkwordle.pedersen import xl, yl
from zkwordle.points import R1CS_LENGTH
import secrets
import time


def prove(a, W, r, w, N, proving_key, variable_polys, deltas=None):
  print("Starting proof.")
  st = time.monotonic()

  assert len(a) == 5
  assert len(w) == 5
  assert len(r) == 5

  vars = {}
  
  polys = {'l': fpoly1d(0), 'r': fpoly1d(0), 'o': fpoly1d(0)}
  
  def register(name, value, p=curve_order):
    import time
    import math
    st = time.monotonic()
    if p is not None:
      value = value % p
    vars[name] = value
    polys['l'] += value * variable_polys[name]['l']
    polys['r'] += value * variable_polys[name]['r']
    polys['o'] += value * variable_polys[name]['o']
    et = time.monotonic()
    #print(f"Registered {name} with size {math.ceil(math.log2(value % curve_order)) + 1 if value % curve_order else 1} in {et-st}s.")

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

  register('Wx', W[0])
  register('Wy', W[1])

  for q in range(63):
    m, n = q // 50, q % 50
    for l in range(4):
      # TODO: Check
      register(f'b{m}{n}{l}', (N >> ((50*m+n)*4 + l)) & 1)

  for q in range(63):
    m, n = q // 50, q % 50
    register(f'bl&{m}{n}', vars.get(f'b{m}{n}0') * vars.get(f'b{m}{n}1')) 

  for q in range(63):
    m, n = q // 50, q % 50
    register(f'bc&{m}{n}', vars.get(f'b{m}{n}0') * vars.get(f'b{m}{n}2')) 

  for q in range(63):
    m, n = q // 50, q % 50
    register(f'bu&{m}{n}', vars.get(f'b{m}{n}1') * vars.get(f'b{m}{n}2')) 

  for q in range(63):
    m, n = q // 50, q % 50
    register(f'b&{m}{n}', vars.get(f'bl&{m}{n}') * vars.get(f'b{m}{n}2')) 

  for q in range(63):
    m, n = q // 50, q % 50
    register(f'ys{m}{n}', (yl(m, n, 1) * vars.get('v1') + (yl(m, n, 2) - yl(m, n, 1)) * vars.get(f'b{m}{n}0') + (yl(m, n, 3) - yl(m, n, 1)) * vars.get(f'b{m}{n}1') + (yl(m, n, 4) - yl(m, n, 3) - yl(m, n, 2) + yl(m, n, 1)) * vars.get(f'bl&{m}{n}') + (yl(m, n, 5) - yl(m, n, 1)) * vars.get(f'b{m}{n}2') + (yl(m, n, 6) - yl(m, n, 5) - yl(m, n, 2) + yl(m, n, 1)) * vars.get(f'bc&{m}{n}') + (yl(m, n, 7) - yl(m, n, 5) - yl(m, n, 3) + yl(m, n, 1)) * vars.get(f'bu&{m}{n}') + (yl(m, n, 8) - yl(m, n, 7) - yl(m, n, 6) + yl(m, n, 5) - yl(m, n, 4) + yl(m, n, 3) + yl(m, n, 2) - yl(m, n, 1)) * vars.get(f'b&{m}{n}')) * (1 * vars.get('v1') - 2 * vars.get(f'b{m}{n}3'))) 

  register('Q00x', (xl(0, 0, 1) * vars.get('v1') + (xl(0, 0, 2) - xl(0, 0, 1)) * vars.get(f'b000') + (xl(0, 0, 3) - xl(0, 0, 1)) * vars.get(f'b001') + (xl(0, 0, 4) - xl(0, 0, 3) - xl(0, 0, 2) + xl(0, 0, 1)) * vars.get(f'bl&00') + (xl(0, 0, 5) - xl(0, 0, 1)) * vars.get(f'b002') + (xl(0, 0, 6) - xl(0, 0, 5) - xl(0, 0, 2) + xl(0, 0, 1)) * vars.get(f'bc&00') + (xl(0, 0, 7) - xl(0, 0, 5) - xl(0, 0, 3) + xl(0, 0, 1)) * vars.get(f'bu&00') + (xl(0, 0, 8) - xl(0, 0, 7) - xl(0, 0, 6) + xl(0, 0, 5) - xl(0, 0, 4) + xl(0, 0, 3) + xl(0, 0, 2) - xl(0, 0, 1)) * vars.get(f'b&00')) * (1 * vars.get('v1')), bjj.p) 
  for q in range(1, 63):
    m, n = q // 50, q % 50
    s, t = (q-1) // 50, (q-1) % 50
    register(f'LQ{m}{n}', (vars.get(f'ys{m}{n}') - vars.get(f'Q{s}{t}y', vars.get(f'ys{s}{t}'))) * mod_inv(xl(m, n, 1) * vars.get('v1') + (xl(m, n, 2) - xl(m, n, 1)) * vars.get(f'b{m}{n}0') + (xl(m, n, 3) - xl(m, n, 1)) * vars.get(f'b{m}{n}1') + (xl(m, n, 4) - xl(m, n, 3) - xl(m, n, 2) + xl(m, n, 1)) * vars.get(f'bl&{m}{n}') + (xl(m, n, 5) - xl(m, n, 1)) * vars.get(f'b{m}{n}2') + (xl(m, n, 6) - xl(m, n, 5) - xl(m, n, 2) + xl(m, n, 1)) * vars.get(f'bc&{m}{n}') + (xl(m, n, 7) - xl(m, n, 5) - xl(m, n, 3) + xl(m, n, 1)) * vars.get(f'bu&{m}{n}') + (xl(m, n, 8) - xl(m, n, 7) - xl(m, n, 6) + xl(m, n, 5) - xl(m, n, 4) + xl(m, n, 3) + xl(m, n, 2) - xl(m, n, 1)) * vars.get(f'b&{m}{n}') - 1 * vars.get(f'Q{s}{t}x'), bjj.p), bjj.p) 
    register(f'Q{m}{n}x', vars.get(f'LQ{m}{n}') * vars.get(f'LQ{m}{n}') - vars.get(f'Q{s}{t}x') - (xl(m, n, 1) * vars.get('v1') + (xl(m, n, 2) - xl(m, n, 1)) * vars.get(f'b{m}{n}0') + (xl(m, n, 3) - xl(m, n, 1)) * vars.get(f'b{m}{n}1') + (xl(m, n, 4) - xl(m, n, 3) - xl(m, n, 2) + xl(m, n, 1)) * vars.get(f'bl&{m}{n}') + (xl(m, n, 5) - xl(m, n, 1)) * vars.get(f'b{m}{n}2') + (xl(m, n, 6) - xl(m, n, 5) - xl(m, n, 2) + xl(m, n, 1)) * vars.get(f'bc&{m}{n}') + (xl(m, n, 7) - xl(m, n, 5) - xl(m, n, 3) + xl(m, n, 1)) * vars.get(f'bu&{m}{n}') + (xl(m, n, 8) - xl(m, n, 7) - xl(m, n, 6) + xl(m, n, 5) - xl(m, n, 4) + xl(m, n, 3) + xl(m, n, 2) - xl(m, n, 1)) * vars.get(f'b&{m}{n}')), bjj.p) 
    register(f'Q{m}{n}y', vars.get(f'LQ{m}{n}') * (vars.get(f'Q{m}{n}x') - vars.get(f'Q{s}{t}x')) - vars.get(f'Q{s}{t}y', vars.get(f'ys{s}{t}')), bjj.p)
    
  for q in range(25):
    i, j = q // 5, q % 5
    s, t = (q-1) // 5, (q-1) % 5
    register(f'W{i}{j}x2', vars.get(f'W{s}{t}x', bjj.Gx) * vars.get(f'W{s}{t}x', bjj.Gx), curve_order)
    register(f'LD{i}{j}', (3 * vars.get(f'W{i}{j}x2') + bjj.a) * mod_inv(2 * vars.get(f'W{s}{t}y', bjj.Gy), bjj.p), curve_order)
    register(f'V{i}{j}x', vars.get(f'LD{i}{j}') * vars.get(f'LD{i}{j}') - 2 * vars.get(f'W{s}{t}x', bjj.Gx))
    register(f'V{i}{j}y', vars.get(f'LD{i}{j}') * (vars.get(f'V{i}{j}x') - vars.get(f'W{s}{t}x', bjj.Gx)) - vars.get(f'W{s}{t}y', bjj.Gy))
    register(f'LA{i}{j}', (bjj.Gy * vars.get(f'w{4-i}{4-j}') - vars.get(f'V{i}{j}y')) * mod_inv(bjj.Gx * vars.get(f'w{4-i}{4-j}') - vars.get(f'V{i}{j}x'), bjj.p))
    register(f'LAw{i}{j}', vars.get(f'w{4-i}{4-j}') * vars.get(f'LA{i}{j}'))
    if vars.get(f'w{4-i}{4-j}'):
      register(f'W{i}{j}x', vars.get(f'LAw{i}{j}') * vars.get(f'LA{i}{j}') - bjj.Gx * vars.get(f'w{4-i}{4-j}') - vars.get(f'V{i}{j}x'))
      register(f'W{i}{j}y', vars.get(f'LAw{i}{j}') * (vars.get(f'W{i}{j}x') - vars.get(f'V{i}{j}x')) - vars.get(f'V{i}{j}y'))
    else:
      register(f'W{i}{j}x', bjj.Gx * vars.get(f'w{4-i}{4-j}') + vars.get(f'V{i}{j}x') - vars.get(f'LAw{i}{j}') * vars.get(f'LA{i}{j}'))
      register(f'W{i}{j}y', vars.get(f'V{i}{j}y') - vars.get(f'LAw{i}{j}') * (vars.get(f'W{i}{j}x') - vars.get(f'V{i}{j}x')))
    register(f'Ww{i}{j}x', vars.get(f'w{4-i}{4-j}') * vars.get(f'W{i}{j}x'))
    register(f'Ww{i}{j}y', vars.get(f'w{4-i}{4-j}') * vars.get(f'W{i}{j}y'))

  # TODO: should this be divmod? Here and in all divs
  register('LW', (vars.get('W44y') - vars.get('Q112y')) * mod_inv(vars.get('W44x') - vars.get('Q112x'), curve_order))
  #register('LW', (vars.get('Wy') + vars.get('W44y')) * mod_inv(vars.get('Wx') - vars.get('W44x'), curve_order))

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
  for i in range(1, R1CS_LENGTH + 1):
    t *= fpoly1d([1, -i])

  p = (polys['l'] + deltas['l'] * t) * (polys['r'] + deltas['r'] * t) - polys['o'] - deltas['o'] * t

  #print(f"P(672): {p(672)}. P orig: {polys['l'](672)*polys['r'](672)-polys['o'](672)}")
  for i in range(1, R1CS_LENGTH + 1):
    if p(i):
      print(f"P({i}): {p(i)}")


  print(f"W00x: {vars.get('W00x')}")
  print(f"W00y: {vars.get('W00y')}")
  print(f"Gx: {bjj.Gx}")
  print(f"Gy: {bjj.Gy}")
 # print(f"Nx: {vars.get('Q112x')}")
 # print(f"Ny: {vars.get('Q112y')}")
 # print(f"Wx: {vars.get('W44x')}")
 # print(f"Wy: {vars.get('W44y')}")
 # print(f"Wx: {vars.get('W43x')}")
 # print(f"Wy: {vars.get('W43y')}")
 # print(f"w: {sum([vars.get(f'w{q//5}{q%5}') << (q) for q in range(25)])}")

  h, q = p / t

  proof['h'] = inner({i: h.coeffs[-1-i] for i in range(len(h.coeffs))}, proving_key['h'])

  et = time.monotonic()
  print(f"Finished proof in {et-st}s...")
  return proof

