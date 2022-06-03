#!/usr/bin/env python3

from setup import fpoly1d

def prove(a, w, r):
  assert len(a) == 5
  assert len(w) == 5
  assert len(r) == 5

  vars = {}
  
  def register(name, value):
    vars[name] = value

  register('v1', 1)

  for i in range(5):
    for j in range(5):
      register(f'a{i}{j}', (a[i] >> j) & 1) 
      register(f'w{i}{j}', (w[i] >> j) & 1) 
    register(f'w{i}34', vars.get(f'w{i}3') * vars.get(f'w{i}4'))
    register(f'w{i}12', vars.get(f'w{i}1') * (vars.get(f'w{i}2') - 1 ))

    register(f'r{i}', r[i])
    register(f'r{i}2', r[i]*r[i])

    register(f'rho{i}0', (vars.get(f'r{i}') - 1) * (vars.get(f'r{i}') - 2))
    register(f'rho{i}1', vars.get(f'r{i}') * (vars.get(f'r{i}') - 2))
    register(f'rho{i}2', vars.get(f'r{i}') * (vars.get(f'r{i}') - 1))

  for i in range(5):
    for j in range(5):
      register(f'P{i}{j}12', (vars.get(f'a{i}0') + vars.get(f'w{j}0') - vars.get('v1')) * \
        (vars.get(f'a{i}1') + vars.get(f'w{j}1') - vars.get('v1'))) 

      register(f'P{i}{j}34', (vars.get(f'a{i}2') + vars.get(f'w{j}2') - vars.get('v1')) * \
        (vars.get(f'a{i}3') + vars.get(f'w{j}3') - vars.get('v1'))) 

      register(f'P{i}{j}1234', vars.get(f'P{i}{j}12') * vars.get(f'P{i}{j}34'))

      register(f'P{i}{j}', vars.get(f'P{i}{j}1234') * (vars.get(f'a{i}4') + vars.get(f'w{j}4') - vars.get('v1'))) 

      register(f'P{i}{j}2', vars.get(f'P{i}{j}') * vars.get(f'P{i}{j}'))

    for j in range(5):
      register(f'D{i}12', sum([(vars.get(f'a{i}{k}') - vars.get(f'w0{k}')) * 2**k for k in range(5)]) * \
        sum([(vars.get(f'a{i}{k}') - vars.get(f'w1{k}')) * 2**k for k in range(5)]))

      register(f'D{i}34', sum([(vars.get(f'a{i}{k}') - vars.get(f'w2{k}')) * 2**k for k in range(5)]) * \
        sum([(vars.get(f'a{i}{k}') - vars.get(f'w3{k}')) * 2**k for k in range(5)])) 

      register(f'D{i}1234', vars.get(f'D{i}12') * vars.get(f'D{i}34'))

      register(f'D{i}', vars.get(f'D{i}1234') * sum([(vars.get(f'a{i}{k}') - vars.get(f'w4{k}')) * 2**k for k in range(5)]))

      register(f'D{i}2', vars.get(f'D{i}') * vars.get(f'D{i}'))

    register(f'c{i}0', vars.get(f'rho{i}0') * sum([vars.get(f'P{i}{j}2') for j in range(5)]))
    register(f'c{i}1', vars.get(f'rho{i}1') * (vars.get(f'D{i}2') + vars.get(f'P{i}{i}2')))
    register(f'c{i}2', vars.get(f'rho{i}2') * sum([(vars.get(f'a{i}{k}') - vars.get(f'w{i}{k}')) * 2**k for k in range(5)]))

  polys = {}
  polys['l'] = fpoly1d(0)
  polys['r'] = fpoly1d(0)
  polys['o'] = fpoly1d(0)

  debug_polys = []

  import csv
  with open('setup.csv', mode='r') as file:
    csv_reader = csv.reader(file, delimiter=',')
    for line in csv_reader:
      variable, type, *coeffs = line 
      value = vars.get(variable)
      coeffs = list(map(int, coeffs))
      poly = fpoly1d(coeffs)
      debug_polys.append((fpoly1d(poly), variable, type, value))
      poly *= value
      polys[type] += poly

  count = 0
  for i in range(1, 261):
    eval = (polys['l']*polys['r'] - polys['o'])(i)
    if eval:
      print('/'*60)
      print(i, eval)
      print("Nonzero polynomials at the point:")
      for p, var, t, v in debug_polys:
        if p(i):
          print('Var:', var, 'Type:', t, 'Value:', v, 'Eval:', p(i))
      count += 1 

  print(count)

if __name__ == "__main__":
  import sys

  if len(sys.argv) < 4:
    raise Exception("not enough arguments")
  
  a = [ord(l)-97 for l in sys.argv[1]]  
  w = [ord(l)-97 for l in sys.argv[2]]
  r = [int(l) for l in sys.argv[3]]
  
  prove(a, w, r)

   

   





