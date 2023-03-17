from zkwordle.ecc import bjj, GroupElement
from web3 import Web3
import json

# (replicate by runing this generate(2))
# Generators
generators = [
   {
     'x': 14293604770338907046413411468626662208600242092671070123891535270955916765716,
     'y': 16931903655476233095338254632264576238984860566592271344419174450729693154521
   },
   {
     'x': 9577711637182991494004369593317413795851017562011530125394342660930391781057, 
     'y': 20153490026823100497557517417463746391764585693453798230213741259837998220915
   }
]


def generate(n, seed="wordle", curve=bjj):
  seed = str.encode(seed)
  nonce = 0
  
  generators = []

  while len(generators) < n:
    hash = Web3.keccak(seed + bytes([nonce]))
    nonce += 1
    
    hash = int.from_bytes(hash, "big")
    sign = hash & 1
    x = hash >> 1
    if not x < curve.p:
      continue
    
    y = curve.from_x(x, sign)
    if y:
      generators.append({'x': x, 'y': y})

  return generators


#https://iden3-docs.readthedocs.io/en/latest/_downloads/4b929e0f96aef77b75bb5cfc0f832151/Pedersen-Hash.pdf
def hash(input, generators=generators):
  assert input < 2**(200*len(generators))

  def enc(m):
    s0 = (m >> 0) & 1
    s1 = (m >> 1) & 1
    s2 = (m >> 2) & 1
    s3 = (m >> 3) & 1
    return (2*s3-1)*(1+s0+2*s1+4*s2)

  H = GroupElement.neutral() 
  
  k = 0

  # should it be <=?
  while 2**(4*k) < input:
    g_index = k // 50
    j = k % 50

    m = (input >> (4*k)) & 0b1111
    e = enc(m)
    f = e * 2**(5*j) 

    g = generators[g_index]
    P = GroupElement.from_ints(g['x'], g['y'])
    H = H + f * P
    
    k += 1
  
  return H


def xl(m, n, k):
  g = generators[m]
  e = GroupElement.from_ints(g['x'], g['y'])
  s = 2**(5*n) * k
  ret = s * e
  return ret.x


def yl(m, n, k):
  g = generators[m]
  e = GroupElement.from_ints(g['x'], g['y'])
  s = 2**(5*n) * k
  ret = s * e
  return ret.y

