from  day6 import A, B

test_A_data = [
    (["COM)B","B)C","C)D","D)E","E)F","B)G","G)H","D)I","E)J","J)K","K)L"], 42)
]

test_B_data = [
    ([
        "COM)B",
        "B)C",
        "C)D",
        "D)E",
        "E)F",
        "B)G",
        "G)H",
        "D)I",
        "E)J",
        "J)K",
        "K)L",
        "I)YOU",
        "K)SAN"
    ], ('YOU', 'SAN', 4))
]


def test_A():
    for arg, res in test_A_data:
        assert A(arg) == res

def test_B():
    for arg, res in test_B_data:
        a, b, dist = res
        assert B(arg, a, b) == dist
