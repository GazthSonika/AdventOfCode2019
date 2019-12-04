from utils import load
import numpy as np
from PIL import Image
from functools import lru_cache
import sys
sys.setrecursionlimit(10**6)

def translate_comands(comands: str):
    data = comands.split(',')
    vectors = []
    for d in data:
        dir_, val = d[0], int(d[1:])        
        if dir_ == 'D':
            vectors.append((0, -val))
        elif dir_ == 'U':
            vectors.append((0, val))
        elif dir_ == 'L':
            vectors.append((-val, 0))
        elif dir_ == 'R':
            vectors.append((val, 0))    
    return vectors


def find_board_size(vectors): #bug hidden
    max_x, min_x, max_y, min_y = 0, 0, 0, 0        
    mx, my = 0, 0
    for x, y in vectors:
        mx += x
        my += y
        max_x, min_x = max(max_x, mx), min(min_x, mx)
        max_y, min_y = max(max_y, my), min(min_y, my)
            
    return abs(max_x) + abs(min_x), abs(max_y) + abs(min_y)


def draw_circut(starting_point, size, commands):    
    circut = np.zeros(size, dtype=np.int8)
    circut[starting_point[0], starting_point[1]]= 2
    old_point = point = starting_point
    for ax, ay in commands:        
        point = old_point[0] + ax, old_point[1] + ay
        for pos in np.linspace(old_point, point, max(abs(ax), abs(ay))+1):
            y, x = np.rint(pos)            
            circut[int(x), int(y)] = 1                            
        old_point = point    

    return circut


def A(a, b, draw=False):
    """
    get's full command as list
    drawing fails for big instructions
    """
    a = translate_comands(a)
    b = translate_comands(b)
    size_a = find_board_size(a)
    size_b = find_board_size(b)
    #to lazy to calculate it better but it's possible ;)
    circut_board_size = \
        (size_a[0] + size_b[0]) * 3, (size_a[1] + size_b[1]) * 3    
    starting_point = size_b[0], size_b[1]    
    from numpy import savetxt
    # draw first circut
    circut_a = draw_circut(starting_point, circut_board_size, a)
    circut_b = draw_circut(starting_point, circut_board_size, b)
    merged = circut_a + circut_b
    intersections = np.where(merged == 2)    

    if draw:
        draw_image(circut_a, circut_b, intersections,starting_point)

    distance_min = 99999999
    for y, x in zip(intersections[0], intersections[1]):
        distance = abs(x - starting_point[0]) + abs(y - starting_point[1]) 
        if distance > 0:     
            distance_min = min(distance, distance_min)

    return distance_min


#i know there are beter methods but i like this one
# @lru_cache(maxsize=30000) cuz of numpy
def walk(circut, pos, stop_at, steps=0):
    x, y = pos
    sx, sy = stop_at
    if x == sx and y == sy:
        return steps

    if steps >= 5000:
        return 10000

    
    # print(steps, y, x)
    while not(x == sx and y == sy):
        circut[y, x] = 2
        steps += 1
        if circut[y+1, x] == 1:        
            y+=1
        if circut[y-1, x] == 1:        
            y-=1
        if circut[y, x+1] == 1:        
            x+=1
        if circut[y, x-1] == 1:        
            x-=1
        if steps >= 15000:
            return 0
    return steps

    

def B(a, b, draw=False):
    """
    Got tired this one is fail slow and inefficent ;( hope to find some 
    time to write a nice few liner
    get's full command as list
    drawing fails for big instructions
    """
    a = translate_comands(a)
    b = translate_comands(b)
    size_a = find_board_size(a)
    size_b = find_board_size(b)
    #to lazy to calculate it better but it's possible ;)
    circut_board_size = \
        (size_a[0] + size_b[0]) * 3, (size_a[1] + size_b[1]) * 3    
    starting_point = size_b[0], size_b[1]    
    from numpy import savetxt
    # draw first circut
    circut_a = draw_circut(starting_point, circut_board_size, a)
    circut_b = draw_circut(starting_point, circut_board_size, b)
    merged = circut_a + circut_b
    intersections = np.where(merged == 2)    

    if draw:
        draw_image(circut_a, circut_b, intersections,starting_point)

    cords = []
    distance_min = 99999999
    for y, x in zip(intersections[0], intersections[1]):
        distance = abs(x - starting_point[0]) + abs(y - starting_point[1])        
        cords.append((x, y))
        if distance > 0 and distance < distance_min:                 
            distance_min = distance
    
    distances_a, distances_b = [], []
    for stop_at in cords:
        print(stop_at)
        distances_a.append(walk(np.copy(circut_a), starting_point, stop_at))
        distances_b.append(walk(np.copy(circut_b), starting_point, stop_at))
    
    print(distances_a, distances_b)
    distance_min = min(
        da+db for da, db in zip(distances_a, distances_b) 
        if da is not None and db is not None and da+db > 0
    )        
    return distance_min


def main():
    data = load('day3_a.txt')  
    # print(A(*data, False))    
    print(B(*data, False))


if __name__ == "__main__":
    main()


    """
    1 . translate
    2 . get all points
    3 . find all intersections, and attach distance 

    class Intersection:
        def __int__(self):
            self.pos
            self.distances[]

        def __eq__(self, in):
            self.pos == in.pos

        @property
        def distance_from_center(start=[0,0])

        @property
        def distance(self):
            sum(self.distances)

    A . get intersecttion closes to 0,0
    B . get intersection with minimal distance on both wires
    """