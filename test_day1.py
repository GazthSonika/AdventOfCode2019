from  day1 import A, B


test_data_A = [
    (12, 2),
    (14, 2),
    (1969, 654),
    (100756, 33583)
]


test_data_B = [
    (100756, 50346),
    (1969, 966)
]

def test_A():
    for arg, val in test_data_A:
        assert A(arg) == val


def test_B():
    for arg, val in test_data_B:
        assert B(arg) == val
