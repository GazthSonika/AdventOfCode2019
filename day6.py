from utils import load
from functools import lru_cache

class Object:
    def __init__(self, name, parent=None, distance=0):
        self.name = name
        self.distance = distance
        self.parent = parent

    def __repr__(self):
        # return f"Object({self.name}) distance: {self.distance} parent: {self.parent}"
        return f"Object({self.name})"

class Mapper():

    def __init__(self, data):
        self._orbits = self._init_orbits(data)
        for it in self._orbits.values(): 
            self._set_orbit_distances(it)
                        
    @lru_cache(100000)
    def _find_orbit_distance(self, obj: Object):
        if obj.parent is None:            
            return 0
        
        return self._find_orbit_distance(obj.parent) + 1
    
    def _init_orbits(self, data):
        raw_map = [(a, b) for a, b in [it.split(')') for it in data]]
        o = {}
        for parent, child in raw_map:
            if parent not in o:
                o[parent] = Object(parent)            
            if child not in o:
                o[child] =  Object(child, o[parent])
        
        #update parents
        for name, orbit in o.items(): 
            if orbit.parent is not None: continue           
            parent_name = [key for key, val in raw_map if val == name]        
            if not parent_name: continue            
            orbit.parent = o[parent_name[0]]                
        
        return o

    def _set_orbit_distances(self, obj: Object):
        
        if obj.parent is None:
            obj.distance = 0        
            return 

        if obj.distance > 0:
            return

        obj.distance = self._find_orbit_distance(obj)
    
    @property
    def orbits(self):
        return self._orbits    


def find_path(node: Object, path=[]):    
    if node.parent == None:
        return path    
    return find_path(node.parent, path + [node])


def A(data):    
    m = Mapper(data)
    return sum(it.distance for it in m.orbits.values())

def B(data, a: str, b: str):
    m = Mapper(data)
    #lets find common node
    a_path = find_path(m.orbits[a])
    b_path = find_path(m.orbits[b])    
    cross = set(a_path) & set(b_path)
    cross = sorted(cross, key=lambda it: it.distance, reverse=True)
    closest = cross[0]    
    return m.orbits[a].distance + m.orbits[b].distance - 2 * closest.distance - 2


def main():
    data = load('day6_a.txt')
    print("A:", A(data))    
    print("B:", B(data, 'YOU', 'SAN'))    

if __name__ == "__main__":
    main()
