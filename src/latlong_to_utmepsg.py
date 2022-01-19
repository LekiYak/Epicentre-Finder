import utm


def latlong_to_utmepsg(dataframe):
    """
    Inputs: Pandas or geopandas dataframe with columns 'LAT' and 'LONG'

    Method: Converts all lat/long pairs to UTM zones and bands, and uses the zone/band combination with the highest frequency
    as the "optimal" UTM projection, and calculates an EPSG projection based off that.

    Outputs: EPSG code (int)

    """
    coords = list(zip(list(dataframe['LAT']), list(dataframe['LONG']))) #List of coords [(LAT, LONG)]
    utm_coords = [(utm.from_latlon(coords[i][0], coords[i][1])) for i in range(len(coords))] #UTM coords [(N, E, zone, band)]
    utm_zones = [(str(utm_coords[i][2]), utm_coords[i][3]) for i in range(len(utm_coords))]

    count = {} #Counting zones to obtain "optimal" zone
    for i in utm_zones:
        count[i] = count.get(i, 0) + 1

    max_zone = max(count, key= lambda x: count[x])
    
    epsg = 32600
    if max_zone[1] < 'N':
        epsg += 100
    epsg += int(max_zone[0])

    return epsg