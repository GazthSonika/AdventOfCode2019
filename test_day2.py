from  day2 import A#, B

class mockA(A):

    def update_opcodes(self, a, b):
        pass

test_data_A = [
    ([1,9,10,3,2,3,11,0,99,30,40,50], 3500)
]

test_data_B = [
    (19690720, [86, 9])
]

# test_data_B = [
#     (100756, 50346),
#     (1969, 966)
# ]

def test_A():
    for arg, val in test_data_A:
        a = mockA(arg)
        assert a.run() == val

