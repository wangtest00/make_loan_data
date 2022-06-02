
def compute_code(m):
    m = m[-4:]
    x1 = str(int(m[0]) + 5)
    x2 = str(int(m[1]) + 5)
    x3 = str(int(m[2]) + 5)
    x4 = str(int(m[3]) + 5)
    x = x4[-1:] + x3[-1:] + x2[-1:] + x1[-1:]
    return x