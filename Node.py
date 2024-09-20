class Point:
    """
    Point is a data structure.
    A Point object is an intersection or important landmark that can be used as a next Point in the road.
    A player is ONLY allowed to move from one Point to the next.
    Each Point is its own object that self-contains the relevant information.
    The Point can be saved, retrieved, modified, or deleted.
    """
    def __init__(self, geo_coord: tuple, neighbours={}):
        """
        Default constructor for any node that will be read from the map data.
        :param geo_coord: tuple(float, float)
        :param neighbours: dict(Point: float)
        """
        self.geo_coord = geo_coord
        self.neighbours = neighbours

    def __repr__(self):
        pass

    # Create method for reading from file
    # Create method to write into file
    # Create method to update in file (combined with write?)
    # Create method to delete from file


class Node(Point):
    """
    Node is a data structure inherited from Point.
    A Node is a special Point that can be chosen by the game randomizer as a starting or ending point.
    A Node contains more information than a Point.
    """
    def __init__(self, geo_coord: tuple, neighbours={}, name="UNKNOWN", description="No description."):
        super().__init__(geo_coord, neighbours)
        self.name = name
        self.description = description

    def __repr__(self):
        pass

    # Possibly override methods
