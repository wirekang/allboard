from threading import Thread


def run_multithread(args_list: list[list], f):
    threads = []
    for args in args_list:
        t = Thread(target=f, args=args, daemon=True)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()


def encoding2(n):
    """
    -2 to 2 single character encoding. (percision=0.1)

    - 0 = -2.0
    - 2 = -1.9
    - 3 = -1.8
    - 4 = -1.7
    - 5 = -1.6
    - 6 = -1.5
    - 7 = -1.4
    - 8 = -1.3
    - 9 = -1.2
    - a = -1.1
    - c = -1.0
    - e = -0.9
    - n = -0.8
    - r = -0.7
    - s = -0.6
    - w = -0.5
    - x = -0.4
    - z = -0.3
    - A = -0.2
    - B = -0.1
    - C = 0.0
    - D = 0.1
    - E = 0.2
    - F = 0.3
    - G = 0.4
    - H = 0.5
    - I = 0.6
    - J = 0.7
    - K = 0.8
    - L = 0.9
    - M = 1.0
    - N = 1.1
    - P = 1.2
    - Q = 1.3
    - R = 1.4
    - S = 1.5
    - T = 1.6
    - V = 1.7
    - X = 1.8
    - Y = 1.9
    - Z = 2.0
    """
    mapping = "023456789acenrswxzABCDEFGHIJKLMNPQRSTVXYZ"
    if n < -2 or n > 2:
        raise ValueError(f"_code: out of range: {n}")
    n = float(n) + 2
    n = n * 10
    return mapping[int(round(n))]
