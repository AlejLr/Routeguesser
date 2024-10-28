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
    def __init__(self, geo_coord: tuple, id_num: int, select=False, neighbours={}):
        """
        Default constructor for any node that will be read from the map data.
        :param geo_coord: tuple(float, float), unique geographical coordinate (Key)
        :param id_num: int, unique ID number
        :param neighbours: dict(Point: float), all neighbours of the Point
        """
        self.geo_coord = geo_coord
        self.select = select
        self.id_num = id_num
        self.neighbours = neighbours

    def add_neighbour(self, neighbour, dist):
        n_geo_coord = neighbour.geo_coordinate
        self.neighbours[n_geo_coord] = dist
        neighbour.neighbours[self.geo_coord] = dist


class Road:
    """
    Road is a data structure.
    A Road object is a collection of geographical coordinates that will be used in the UI to present a smoother curve
    in the road, as well as to calculate the neighbour status and distance between two Point objects.
    Players are NOT allowed to modify the Road objects.
    Road objects can contain shared starting and ending coordinates.
    """
    def __init__(self, p_vector, id_num):
        """
        Default constructor that accepts the vector of coordinates, and saves the data in a more task oriented method.
        :param p_vector: list[list[double, double]]
        """
        self.p_start = tuple(p_vector[0])
        self.p_end = tuple(p_vector[-1])
        self.p_len = len(p_vector)
        self.p_dist = -1.0
        self.p_vector = p_vector
        self.p_id = id_num

    def calc_dist(self):
        dist = 0.0
        for i in range(self.p_len-2):
            dist += (self.p_vector[i]**2+self.p_vector[i+1]**2)**(1/2)
        self.p_dist = dist
        return dist
