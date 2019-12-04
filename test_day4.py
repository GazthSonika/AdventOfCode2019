from  day4 import is_valid_A, is_valid_B

test_A_is_valid_data = [
    (111111, True),
    (223450, False),
    (123789, False),
]

test_B_is_valid_data = [
    (112233, True),
    (123444, False),
    (111122, True)

]

def test_A_is_valid():
    for arg, res in test_A_is_valid_data:
        assert is_valid_A(arg) == res

def test_B_is_valid():    
    for arg, res in test_B_is_valid_data:
        assert is_valid_B(arg) == res
