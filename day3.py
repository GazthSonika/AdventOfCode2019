from utils import load


Directions = {'D': (0, -1), 'U': (0, 1), 'L': (-1 ,0), 'R': (1, 0)}    

def create_board(comands: str, x=0, y=0):
    data = comands.split(',')    
    board = {}    
    total_steps = 0
    for d in data:
        dir_, val = d[0], int(d[1:])
        dx, dy =  Directions[dir_][0], Directions[dir_][1]
        for _ in range(val):
            x, y = x + dx, y + dy
            total_steps += 1
            board[(x, y)] = total_steps                
    return board

def A(a, b):    
    a = create_board(a)
    b = create_board(b)        
    intersections = set(a.keys()) & set(b.keys())
    distance = min(abs(x) + abs(y) for x, y in intersections)    
    return distance

def B(a, b):
    a = create_board(a)
    b = create_board(b)        
    intersections = set(a.keys()) & set(b.keys())
    distance = min(a[xy] + b[xy] for xy in intersections)
    return distance

def main():
    data = load('day3_a.txt')  
    print("A:", A(*data))    
    print("B:", B(*data))


if __name__ == "__main__":
    main()
