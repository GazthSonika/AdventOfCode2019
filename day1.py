from utils import load

def A(mass):
    return mass // 3 - 2    


def B(mass):  
    fuel = 0
    tmp_fuel = A(mass)
    while tmp_fuel > 0:
        fuel += tmp_fuel
        tmp_fuel = A(tmp_fuel)
    return fuel    


def main():
    data = load('day1_a.txt')    
    print(
        "A", sum([A(int(d)) for d in data]),
        "\nB", sum([B(int(d)) for d in data])
    )        


if __name__ == "__main__":
    main()