from zkwordle.ecc import bjj
from web3 import Web3
import json
import os

from zkwordle.util import load_json

LOAD_LOOKUP = int(os.environ.get("LOAD_LOOKUP", 1))

if LOAD_LOOKUP:
  try:
    lookup = load_json('lookup.json')
  except:
    print("Unable to preload the lookup elements for Pedersen Hash. Remember to set LOAD_LOOKUP to 0 if no file exsists.")
    exit(0)

# (replicate by runing this generate(2))
# Generators
generators = [
  {'x': 6475754429882782203003994905906857116784534756624133315443781871325085335969,
   'y': 1061669752226705182426438653967629486155153061846332681432965827148930796537
  },
  {'x': 11130047857281870482446215339847093381191806877983479531441339823419429614231, 
   'y': 4725544795630025775791314500120412189499904222516352803721979933693965526546
  }
]

def generate(n, seed="wordle", curve=bjj):
  seed = str.encode(seed)
  
  generators = bjj.hash_to_curve(seed, n)
  generators = [{'x': P.x, 'y': P.y} for P in generators]

  return generators


#https://iden3-docs.readthedocs.io/en/latest/_downloads/4b929e0f96aef77b75bb5cfc0f832151/Pedersen-Hash.pdf
def hash(input, generators=generators):
  assert input < 2**(200*len(generators))

  def enc(m):
    s0 = (m >> 0) & 1
    s1 = (m >> 1) & 1
    s2 = (m >> 2) & 1
    s3 = (m >> 3) & 1
    return (1-2*s3)*(1+s0+2*s1+4*s2)

  H = bjj.Point.ZERO
  
  for k in range(63):
    i, j = k // 50, k % 50

    m = (input >> (4*k)) & 0b1111
    e = enc(m)
    f = e * 2**(5*j) 

    g = generators[i]
    P = bjj.Point.from_ints(g['x'], g['y'])
    H = H + P * bjj.Fr(f)
    
  return H


def xl(m, n, k):
  if LOAD_LOOKUP:
    return lookup[str(m)][str(n)][str(k)]["x"]
  else:
    g = generators[m]
    e = bjj.Point.from_ints(g['x'], g['y'])
    s = 2**(5*n) * k
    ret = s * e
    return ret.x


def yl(m, n, k):
  if LOAD_LOOKUP:
    return lookup[str(m)][str(n)][str(k)]["y"]
  else:
    g = generators[m]
    e = bjj.Point.from_ints(g['x'], g['y'])
    s = 2**(5*n) * k
    ret = s * e
    return ret.y
