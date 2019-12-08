from utils import load
import numpy as np

LAYER_SIZE = 6, 25

def split_layers(data, size: tuple):
    return np.array(list(data)).reshape(-1, *size).astype(np.int8)

def find_color(layers, pos, layer): 
    el = layers[layer, pos[1], pos[0]]
    if el == 2: 
        return find_color(layers, pos, layer+1)
    return el
    

def A(data, size):
    flayers = [l.flatten() for l in split_layers(data, size)] 
    zc = sorted(flayers, key=lambda it: np.count_nonzero(it == 0))[0]   
    return np.count_nonzero(zc == 1) * np.count_nonzero(zc == 2)    


def B(data, size):    
    layers = split_layers(data, size)    
    bufor = ''    
    for y in range(LAYER_SIZE[0]):
        for x in range(LAYER_SIZE[1]):        
            bufor += '#' if find_color(layers, (x, y), 0) == 1 else ' '
        bufor += '\n'
    return bufor


def main():
    data = load('day8_a.txt')[0]        
    print("A:", A(data, LAYER_SIZE))    
    print("B:")
    print(B(data, LAYER_SIZE))

if __name__ == "__main__":
    main()
