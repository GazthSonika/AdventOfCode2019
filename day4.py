def is_valid_A(number):
    sn = [int(n) for n in str(number)]
    return sn == sorted(sn) and any(a == b for a, b in zip(sn[1:], sn))


def is_valid_B(number):
    sn = [-1] + [int(n) for n in str(number)] + [10]    
    z = zip(sn[3:], sn[2:], sn[1:], sn)
    return sn == sorted(sn) and any(
        a != b and b == c and c != d for a, b, c, d in z
    ) 


def A(a, b):
    return sum(1 for x in range(a, b) if is_valid_A(x))

def B(a, b):
    return sum(1 for x in range(a, b) if is_valid_B(x))


def main():
    data = (245182, 790572) 
    print("A:", A(*data))
    print("B:", B(*data))


if __name__ == "__main__":
    main()
