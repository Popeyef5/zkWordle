import numpy as np

def mod_inv(x, p):
  x = x % p
  t = 0
  nt = 1
  r = p
  nr = x
  while nr != 0:
    q = r // nr
    t, nt = nt, t - q * nt
    r, nr = nr, r - q * nr
  if r != 1:
    raise ValueError("number has no inverse")
  return t % p


def polydivmod(u, v, p):
  m = len(u)
  n = len(v)
  s = mod_inv(v[0], p)
  q = np.array([0]*max(m-n+1, 1), dtype=object)
  r = np.copy(u)
  
  for i in range(m - n +1):
    d = s * r[i] % p
    q[i] = d
    r[i:i+n] = np.mod(r[i:i+n] - v * d, p)

  first = 0
  for i in range(len(r)-1):
    if r[i] != 0:
      break
    first += 1

  r = r[first:]

  return q, r


def dump_json(obj, filename):
  import json

  class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj.toJSON()

  with open(filename, 'w') as f:
    json.dump(obj, f, indent=6, cls=NumpyEncoder)


def load_json(filename):
  import json

  with open(filename, 'r') as f:
      ret = json.load(f)
  return ret

def inner(a, b):
  ret = None
  for key in a:
    tmp = a[key] * b[key]
    if ret is None:
      ret = tmp
    else:
      ret += tmp
  return ret


