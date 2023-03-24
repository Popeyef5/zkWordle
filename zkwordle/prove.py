from zkwordle.util import inner, mod_inv
from zkwordle.helpers import fpoly1d
from zkwordle.ecc import bn128, bjj
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
  
  def register(name, value, p=bn128.curve_order):
    import time
    if p is not None:
      value = value % p
    t0 = time.monotonic()
    vars[name] = value
    polys['l'] += value * variable_polys[name]['l']
    polys['r'] += value * variable_polys[name]['r']
    polys['o'] += value * variable_polys[name]['o']
    #print(f"Registering {name} took {time.monotonic() - t0}...")

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
    register(f'R{m}{n}x', (xl(m, n, 1) * vars.get('v1') + (xl(m, n, 2) - xl(m, n, 1)) * vars.get(f'b{m}{n}0') + (xl(m, n, 3) - xl(m, n, 1)) * vars.get(f'b{m}{n}1') + (xl(m, n, 4) - xl(m, n, 3) - xl(m, n, 2) + xl(m, n, 1)) * vars.get(f'bl&{m}{n}') + (xl(m, n, 5) - xl(m, n, 1)) * vars.get(f'b{m}{n}2') + (xl(m, n, 6) - xl(m, n, 5) - xl(m, n, 2) + xl(m, n, 1)) * vars.get(f'bc&{m}{n}') + (xl(m, n, 7) - xl(m, n, 5) - xl(m, n, 3) + xl(m, n, 1)) * vars.get(f'bu&{m}{n}') + (xl(m, n, 8) - xl(m, n, 7) - xl(m, n, 6) + xl(m, n, 5) - xl(m, n, 4) + xl(m, n, 3) + xl(m, n, 2) - xl(m, n, 1)) * vars.get(f'b&{m}{n}')) * (1 * vars.get('v1') - 2 * vars.get(f'b{m}{n}3'))) 

  for q in range(63):
    m, n = q // 50, q % 50
    s, t = (q-1) // 50, (q-1) % 50
    register(f'QRx{m}{n}', vars.get(f'Q{s}{t}x', 0) * vars.get(f'R{m}{n}x'))
    register(f'QRy{m}{n}', vars.get(f'Q{s}{t}y', 1) * (yl(m, n, 1) * vars.get('v1') + (yl(m, n, 2) - yl(m, n, 1)) * vars.get(f'b{m}{n}0') + (yl(m, n, 3) - yl(m, n, 1)) * vars.get(f'b{m}{n}1') + (yl(m, n, 4) - yl(m, n, 3) - yl(m, n, 2) + yl(m, n, 1)) * vars.get(f'bl&{m}{n}') + (yl(m, n, 5) - yl(m, n, 1)) * vars.get(f'b{m}{n}2') + (yl(m, n, 6) - yl(m, n, 5) - yl(m, n, 2) + yl(m, n, 1)) * vars.get(f'bc&{m}{n}') + (yl(m, n, 7) - yl(m, n, 5) - yl(m, n, 3) + yl(m, n, 1)) * vars.get(f'bu&{m}{n}') + (yl(m, n, 8) - yl(m, n, 7) - yl(m, n, 6) + yl(m, n, 5) - yl(m, n, 4) + yl(m, n, 3) + yl(m, n, 2) - yl(m, n, 1)) * vars.get(f'b&{m}{n}')))
    register(f'QRd{m}{n}', bjj.JUBJUB_D.s * vars.get(f'QRx{m}{n}') * vars.get(f'QRy{m}{n}'))
    register(f'QRs{m}{n}', (vars.get(f'Q{s}{t}x', 0) + vars.get(f'Q{s}{t}y', 1)) * (vars.get(f'R{m}{n}x') + yl(m, n, 1) * vars.get('v1') + (yl(m, n, 2) - yl(m, n, 1)) * vars.get(f'b{m}{n}0') + (yl(m, n, 3) - yl(m, n, 1)) * vars.get(f'b{m}{n}1') + (yl(m, n, 4) - yl(m, n, 3) - yl(m, n, 2) + yl(m, n, 1)) * vars.get(f'bl&{m}{n}') + (yl(m, n, 5) - yl(m, n, 1)) * vars.get(f'b{m}{n}2') + (yl(m, n, 6) - yl(m, n, 5) - yl(m, n, 2) + yl(m, n, 1)) * vars.get(f'bc&{m}{n}') + (yl(m, n, 7) - yl(m, n, 5) - yl(m, n, 3) + yl(m, n, 1)) * vars.get(f'bu&{m}{n}') + (yl(m, n, 8) - yl(m, n, 7) - yl(m, n, 6) + yl(m, n, 5) - yl(m, n, 4) + yl(m, n, 3) + yl(m, n, 2) - yl(m, n, 1)) * vars.get(f'b&{m}{n}')))
    register(f'Q{m}{n}x', (vars.get(f'QRs{m}{n}') - vars.get(f'QRx{m}{n}') - vars.get(f'QRy{m}{n}')) * mod_inv(vars.get('v1') + vars.get(f'QRd{m}{n}'), bjj.q_j))
    register(f'Q{m}{n}y', (vars.get(f'QRy{m}{n}') - bjj.JUBJUB_A.s * vars.get(f'QRx{m}{n}')) * mod_inv(vars.get('v1') - vars.get(f'QRd{m}{n}'), bjj.q_j))
  
  register('W00x', bjj.Gx * vars.get('w44'))
  register('W00y', 1 * vars.get('v1') + (bjj.Gy - 1) * vars.get('w44'))
  for q in range(1, 25):
    i, j = q // 5, q % 5
    s, t = (q-1) // 5, (q-1) % 5
    register(f'W{s}{t}x2', vars.get(f'W{s}{t}x') * vars.get(f'W{s}{t}x'))
    register(f'W{s}{t}y2', vars.get(f'W{s}{t}y') * vars.get(f'W{s}{t}y'))
    register(f'W{s}{t}xy', vars.get(f'W{s}{t}x') * vars.get(f'W{s}{t}y'))
    register(f'V{i}{j}x', 2 * vars.get(f'W{s}{t}xy') * mod_inv(bjj.JUBJUB_A.s * vars.get(f'W{s}{t}x2') + vars.get(f'W{s}{t}y2'), bjj.q_j))
    register(f'V{i}{j}y', (vars.get(f'W{s}{t}y2') - bjj.JUBJUB_A.s * vars.get(f'W{s}{t}x2')) * mod_inv(2 * vars.get('v1') - bjj.JUBJUB_A.s * vars.get(f'W{s}{t}x2') - vars.get(f'W{s}{t}y2'), bjj.q_j))
    register(f'Vwx{i}{j}', vars.get(f'V{i}{j}x') * bjj.Gx * vars.get(f'w{4-i}{4-j}'))
    register(f'Vwy{i}{j}', vars.get(f'V{i}{j}y') * (1 + (bjj.Gy - 1) * vars.get(f'w{4-i}{4-j}')))
    register(f'Vwd{i}{j}', bjj.JUBJUB_D.s * vars.get(f'Vwx{i}{j}') * vars.get(f'Vwy{i}{j}'))
    register(f'Vws{i}{j}', (vars.get(f'V{i}{j}x') + vars.get(f'V{i}{j}y')) * (1 + (bjj.Gx + bjj.Gy - 1) * vars.get(f'w{4-i}{4-j}')))
    register(f'W{i}{j}x', (vars.get(f'Vws{i}{j}') - vars.get(f'Vwx{i}{j}') - vars.get(f'Vwy{i}{j}')) * mod_inv(vars.get('v1') + vars.get(f'Vwd{i}{j}'), bjj.q_j))
    register(f'W{i}{j}y', (vars.get(f'Vwy{i}{j}') - bjj.JUBJUB_A.s * vars.get(f'Vwx{i}{j}')) * mod_inv(vars.get('v1') - vars.get(f'Vwd{i}{j}'), bjj.q_j))

  register('QWx', vars.get('Q112x') * vars.get('W44x')) 
  register('QWy', vars.get('Q112y') * vars.get('W44y')) 
  register('QWd', bjj.JUBJUB_D.s * vars.get('QWx') * vars.get('QWy')) 
  register('QWs', (vars.get('Q112x') + vars.get('Q112y')) * (vars.get('W44x') + vars.get('W44y'))) 

  if deltas is None:
    deltas = {
      'l': secrets.randbelow(bn128.curve_order),
      'r': secrets.randbelow(bn128.curve_order),
      'o': secrets.randbelow(bn128.curve_order)
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

  h, q = p / t

  proof['h'] = inner({i: h.coeffs[-1-i] for i in range(len(h.coeffs))}, proving_key['h'])

  et = time.monotonic()
  print(f"Finished proof in {et-st}s...")
  return proof

