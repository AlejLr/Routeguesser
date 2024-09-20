import Node as nd
import Map


def main():
    test = nd.Point((-1.339, 4.335))
    test2 = nd.Node((0.312, 3.867), name="Test")
    print(test.geo_coord, test.neighbours, test2.geo_coord, test2.name)

if __name__ == "__main__":
    main()
