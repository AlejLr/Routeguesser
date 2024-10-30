"""
TODO:
> Privatize and protect data.
> Add setters and getters.
> Add basic magic methods.
> Connect to Map class.
> Complete functionality.
> Comment code.
> Test in main.
"""


class Point:
    """
    Point is a data structure.
    A Point object is an intersection or important landmark that can be used as a next Point in the road.
    A player is ONLY allowed to move from one Point to the next.
    Each Point is its own object that self-contains the relevant information.
    """
    # Default constructor.
    def __init__(self, geo_coord: tuple, select=False, neighbours={}):
        self.geo_coord = geo_coord
        self.select = select
        self.neighbours = neighbours

    # JSON constructor.
    def __init__(self, json_obj):
        self.geo_coord = (0, 0)
        self.select = False
        self.neighbours = {}

    # Adds a connection between two objects.
    def add_neighbour(self, neighbour, road_obj):
        n_geo_coord = neighbour.geo_coord
        self.neighbours[n_geo_coord] = (road_obj.p_dist, road_obj.p_id)
        neighbour.neighbours[self.geo_coord] = (road_obj.p_dist, road_obj.p_id)

    # Turns object into JSON friendly format.
    def turn_json(self):
        j = {'geo_coord': self.geo_coord, 'select': self.select}
        n = {}
        for key, value in self.neighbours.items():
            n[str(key)] = [*value]
        j['neighbours'] = n
        return j

    def __repr__(self):
        return f"Point(geo_coord: {self.geo_coord})"


class Road:
    """
    Road is a data structure.
    A Road object is a collection of geographical coordinates that will be used in the UI to present a smoother curve
    in the road, as well as to calculate the neighbour status and distance between two Point objects.
    Players are NOT allowed to modify the Road objects.
    Road objects can contain shared starting and ending coordinates.
    """
    # Default constructor.
    def __init__(self, p_vector, id_num):
        # Attributes to reduce basic function calls
        self.p_start = tuple(p_vector[0])
        self.p_end = tuple(p_vector[-1])
        self.p_len = len(p_vector)

        # Inherent value attributes
        self.p_vector = p_vector
        self.p_dist = self.calc_dist()
        self.p_id = id_num

    def __repr__(self):
        return f"Road(between: {self.p_start} and {self.p_end}, length: {self.p_dist})"

    # Calculates the length of the road calculating distance between each point along the road.
    def calc_dist(self):
        dist = 0.0
        for i in range(self.p_len-2):
            v1 = self.p_vector[i]
            v2 = self.p_vector[i+1]
            dist += Road.pyth(*v1, *v2)
        return dist

    def turn_json(self):
        j = {'p_start': self.p_start,
             'p_end': self.p_end,
             'p_len': self.p_len,
             'p_id': self.p_id,
             'p_dist': self.p_dist,
             'p_vector': self.p_vector}
        return j

    @staticmethod
    def pyth(x1, y1, x2, y2):
        return (abs(x2-x1)**2 + abs(y2-y1)**2)**(1/2)
