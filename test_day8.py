from  day8 import split_layers, A

test_data = '123456789012'
size = 2, 3

def test_A():
    ret = A(test_data, size)
    assert ret == 1


def test_split_layers():    
    s = split_layers(test_data, size)
    assert s[1 ,1 ,2] == 2
    assert s[1 ,0, 0] == 7
    assert s[0, 0, 0] == 1
    assert s[0, 1, 2] == 6

