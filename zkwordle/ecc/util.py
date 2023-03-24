# https://en.wikipedia.org/wiki/Legendre_symbol
def legendre_symbol(a, p):
    ls = pow(a, (p - 1) // 2, p)
    if ls == p - 1:
        return -1
    return ls

# https://gist.github.com/nakov/60d62bdf4067ea72b7832ce9f71ae079
# https://en.wikipedia.org/wiki/Tonelli-Shanks_algorithm
def mod_sqrt(a, p):
  if legendre_symbol(a, p) != 1:
    return []
  elif a == 0:
    return [0, 0]
  elif p == 2:
    return [a, a]
  elif p % 4 == 3:
    x = pow(a, (p + 1) // 4, p)
    return [min(x, p-x), max(x, p-x)]

  # Partition p-1 to s * 2^e for an odd s (i.e.
  # reduce all the powers of 2 from p-1)
  #
  s = p - 1
  e = 0
  while s % 2 == 0:
    s //= 2
    e += 1

  # Find some 'n' with a legendre symbol n|p = -1.
  # Shouldn't take long.
  #
  n = 2
  while legendre_symbol(n, p) != -1:
    n += 1

  # Here be dragons!
  # Read the paper "Square roots from 1; 24, 51,
  # 10 to Dan Shanks" by Ezra Brown for more
  # information
  #

  # x is a guess of the square root that gets better
  # with each iteration.
  # b is the "fudge factor" - by how much we're off
  # with the guess. The invariant x^2 = ab (mod p)
  # is maintained throughout the loop.
  # g is used for successive powers of n to update
  # both a and b
  # r is the exponent - decreases with each update
  #
  x = pow(a, (s + 1) // 2, p)
  b = pow(a, s, p)
  g = pow(n, s, p)
  r = e

  while True:
    t = b
    m = 0
    for m in range(r):
      if t == 1:
        break
      t = pow(t, 2, p)

    if m == 0:
      return [min(x, p-x), max(x, p-x)]

    gs = pow(g, 2 ** (r - m - 1), p)
    g = (gs * gs) % p
    x = (x * gs) % p
    b = (b * g) % p
    r = m
