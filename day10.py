from utils import load
from PIL import Image, ImageDraw
import math

def draw_map(cords, satelite_position, counts={}, size=(1000, 1000), scale=27):    
    im = Image.new("RGB", size)
    draw = ImageDraw.Draw(im)
    for c, visible in cords.items():
        color = 'red' if visible else (130,0,0)        
        if c == satelite_position:
            color = 'green'
        
        draw.ellipse((c[0]*scale, c[1]*scale, c[0]*scale+scale, c[1]*scale+scale), color)
        if c in counts:
            draw.text((c[0]*scale +6, c[1]*scale + 6), str(counts[c]), fill=(255,255,255,128))
    return im


def read_cords_from_map(m: str, object_sign='#'):
    cords = dict()
    for y, line in enumerate(m.split('\n')):
        for x, char in enumerate(line):
            if char == object_sign:
                cords[(x, y)] = True # true visible
    return cords


def __find_minimal_pair(dx, dy):                 
    gcd = math.gcd(dx, dy)
    return dx / gcd, dy / gcd

def get_max_cords(cords):
    max_x, max_y = 0, 0
    for c in cords:                        
        max_x, max_y = max(max_x, c[0]), max(max_y, c[1])
    return max_x, max_y

def visibility(cords, me: tuple):
    """
    me: position of main object 'satelite'
    """
    cords = cords.copy()
    max_x, max_y = get_max_cords(cords)    
    mx, my = me
    
    for c, visible in cords.items():
        if me == c or not visible :            
            continue        
        cx, cy = c
        dx, dy = __find_minimal_pair(cx - mx, cy - my)
        while cx >= 0 and cx <= max_x and cy >= 0 and cy <= max_y:                        
            cx += int(dx)
            cy += int(dy)
            if (cx, cy) in cords.keys():                
                cords[(cx, cy)] = False                                
    return cords

def get_counts(cords):
    counts = dict()
    for c in cords:
        counts[c] = sum(1 for v in visibility(cords, c).values() if v) - 1
    return counts

def shoot_laster(cords, target): # mutable will mofity cords
    # if cords.get(target, None):
    #     print(len(cords), target, target in cords, cords.get(target, None))
    if target in cords and cords[target]:
        print("Destroying ", target)
        del cords[target]
        return True
    return False

def get_laser_shot_cords(me, pos):    

    mx, my = me 
    px, py = pos
    if mx - px != 0:
        a = (my - py) / (mx - px)
    else:
        a = 999999999999

    b = py - a * px   
    dx, dy = abs(mx - px), abs(my - py)
    cords = []
    
    if dx >= dy:                
        direction = 1 if px-mx >= 0 else -1
        for x in range(mx, px + direction, direction):            
            cords.append((x, round(a * x + b)))
    else:        
        direction = 1 if py-my >= 0 else -1
        for y in range(my, py + direction, direction):
            cords.append((round((y - b) / a), y))
    
    return cords


def visualise_B(map_, me=(0, 0), looking_for=200):
    import pygame

    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    done = False
    size = 20
    cords = read_cords_from_map(map_) 
    cords = visibility(cords, me)
    print(cords)
    print(me)
    destroyed = 0
    while not done:                

        screen.fill((0, 0, 0))
        mouse = pygame.mouse.get_pos() 
        mouse_rel = mouse[0] // size, mouse[1] // size
        path = get_laser_shot_cords(me, mouse_rel)
        to_shoot = set(path) & set(c for c in cords if cords[c] and c != me)
        pygame.display.set_caption(f"Already destroyed {destroyed} " + str(to_shoot))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONUP:
                for it in to_shoot:
                    destroyed += 1
                    del cords[it]
                cords = visibility(cords, me)
        distance = 0
        
        
        for x in range(800 // size):
            for y in range(800 // size):                
                color = (0, 32, 64)     
                if (x, y) in cords:
                    color = (180, 0 ,0)           
                    if cords[(x,y)] == False:
                        color = (30, 0 ,0)           
                
                if mouse_rel == (x, y):
                    color = (255,255,255)
                if (x, y) in path:
                    color = (max(0, 127-distance),max(0, 127-distance),max(0, 127-distance))
                    distance -= 5
                    

                    if (x, y) in cords:
                        color = (250,0, 0)
                        if cords[(x,y)] == False:
                            color = (10, 0 ,0)
                if (x, y) == me:
                    color = (128, 0, 255)

                pygame.draw.rect(screen, color, pygame.Rect(x*size, y*size, size-1, size-1))

        pygame.display.flip()


def B(map_, me=(0, 0), looking_for=200):
    
    cords = read_cords_from_map(map_)    
    mx, my = me
    max_x, max_y = get_max_cords(cords)
            
    start_stop = (mx, 0)
    change_positions = [(max_x, 0), (max_x, max_y), (0 ,max_y), (0, 0)]    
    
    vectors = [(0, 1), (-1, 0), (0, -1), (1, 0)]
    destroyed = 0
    while True:        
        cords = visibility(cords, me)
        counts = get_counts(cords)        
        
        pos = list(start_stop)
        vn = 3
        while True:            

            if tuple(pos) in change_positions:
                vn = change_positions.index(tuple(pos))                
            
            pos[0], pos[1] = vectors[vn][0] + pos[0], vectors[vn][1] + pos[1]
            if tuple(pos) == start_stop:
                print("Breaking inner")
                break
            path = get_laser_shot_cords(me, pos)
            to_shoot = list(set(path) & set(c for c in cords if cords[c] and c != me))
            to_shoot = sorted(to_shoot, key=lambda it: math.sqrt((it[0] - mx)**2) + (it[1] - my) ** 2, reverse=True)
            for it in to_shoot:
                destroyed += 1

                if destroyed == looking_for:
                    print("I guess i was lucky or maybe it really works well but another points that might be 200", to_shoot)
                    return it
                del cords[it]
                cords = visibility(cords, me)


def A_draw(map_, me=(2,2)):
    """
    Bonus function to draw it :) 
    """
    cords = read_cords_from_map(map_)
    counts = get_counts(cords)
    c = visibility(cords, me)
    draw_map(c, me, counts).show()


def A(map_):
    cords = read_cords_from_map(map_)
    counts = get_counts(cords)
    scounts = sorted(counts.items(), key=lambda it: it[1], reverse=True)[0]
    return scounts    

def main():    
    m = load('day10_a.txt', None)
    
    cords, a = A(m)   
    
    print("A:", a, cords)    
    # visualise_B(m, cords)
    b = B(m, cords)
    print("B:", b, '=>', b[0]*100+b[1])

if __name__ == "__main__":
    main()
