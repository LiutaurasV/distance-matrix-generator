import csv
from geopy.geocoders import Nominatim
from geopy.distance import distance

def getCoordinates(cities):
    """Takes a list of city names as strings and returns
    A list of coordinate tuples (latitude, longitude) for those cities."""
    
    geolocator = Nominatim(user_agent='distance_matrix_generator')
    coordinates = []
    for city in cities:
        location = geolocator.geocode(city)
        coordinates.append((location.latitude, location.longitude))
    return coordinates

def calcDistances(coordinates):
    """Takes a list of coordinate tuples (lat, long) and returns a distance
        matrix of given coordinates."""

    #The distance between A and B is only calculated once. The value
    #for distance between B and A is generated later in the fill matrix
    #function by copying A - B distance to save time.
    matrix = []
    for i in range(len(coordinates)):
        i_distances = ['' for _ in range(i)]
        for j in range(i, len(coordinates)):
            i_distances.append(distance(coordinates[i], coordinates[j]).km)
        matrix.append(i_distances)

    return matrix

def fillMatrix(matrix):
    """Fills the lower left half of the matrix with values by mirroring the
        upper right half of the matrix"""
    
    for i in range(1, len(matrix)):
        for j in range(i):
            matrix[i][j] = matrix [j][i]
 
    return matrix

if __name__ == '__main__':

    #Reading the city names from the csv file
    with open ('cities.csv', 'r', encoding='UTF-8') as f:
        reader = csv.reader(f, delimiter=';')
        cities = next(reader)

    coordinates = getCoordinates(cities)
    matrix = calcDistances(coordinates)
    matrix = fillMatrix(matrix)

    with open('distance_matrix.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f, delimiter = ';')

        #Adding an empty 'cell' before city names for the matrix header to
        #be displayed correctly
        writer.writerow(['']+cities)
        
        for i in range(len(matrix)):
            writer.writerow([cities[i]] + matrix[i])
