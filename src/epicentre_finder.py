import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as cx
from shapely.geometry import Point
import os
import warnings
from latlong_to_utmepsg import *
import sys

warnings.filterwarnings("ignore")

def load_data():
    CWD = os.path.dirname(os.path.abspath(__file__))

    print("Loading Dataset...")
    if ":/" not in sys.argv[1]:
        df = pd.read_csv(CWD + '\\' + str(sys.argv[1])) #arg.csv in CWD, input as (path) + name + .csv
    else:
        df = pd.read_csv(str(sys.argv[1])) #Full path

    df = df.sort_values(by=['TP']) #Sort by closest - farthest station
    df = df.reset_index(drop=True) #Resets index

    #convert from pandas df to geopandas df w/ lat/long points
    gdf = gpd.GeoDataFrame(df, crs={'init': 'epsg:4326'}, geometry=gpd.points_from_xy(df.LONG, df.LAT)) 
    gdf = gdf.to_crs(latlong_to_utmepsg(gdf)) #Set new cartesian CRS
    
    print("Done!")
    return gdf

def radii_calculations(df):
    VS,VP = df[~df['VS'].isnull()]['VS'], df[~df['VP'].isnull()]['VP'] #S and P wave speeds, in m/s

    radii = np.array([])
    for (t1, t2) in zip(list(df['TS']), list(df['TP'])): #Get TS, TP columns from csv into list of tuples (TS, TP) in seconds             
        radii = np.append(radii, round((t1 - t2) / ((1 / VS) - (1 / VP)), 2)) #turning v's into radii from first arrival times
    
    return radii
    
def find_epicentre(gdf, radii):
    lines = gdf.buffer(radii).exterior.lines.to_crs(4326) #Creating LineRings, resetting CRS to lat/long (4326)
    gdf = gdf.to_crs(4326) #CRS World mercator = 3857

    intersections_list_multi = [] #Multipoint list of intersection pairs between all intersection pairs
    for i in range(lines.size):
        for j in range(lines.size):
            if i != j:
                intersections_list_multi.append(lines[i].intersection(lines[j]))

    #removing all empty geometries
    intersections_list_multi = [multipoint for multipoint in intersections_list_multi if not multipoint.is_empty]

    intersections_list = [] #converting multipoint list to list of points
    for i in range(len(intersections_list_multi)):
        intersections_list.append(intersections_list_multi[i][0])
        intersections_list.append(intersections_list_multi[i][1])

    #GDF of intersection points, with lats and longs listed 
    intersections = gpd.GeoDataFrame(geometry=intersections_list, crs={'init': 'epsg:4326'}) 
    intersections['LONG'] = intersections['geometry'].x
    intersections['LAT'] = intersections['geometry'].y

    for i in range(2): #Trimming outliers (range(x)) x times
        intersections = intersections[np.abs(intersections.LONG-intersections.LONG.mean())<=(intersections.LONG.std())]
        intersections = intersections[np.abs(intersections.LAT-intersections.LAT.mean())<=(intersections.LAT.std())]
    
    epicentre = gpd.GeoSeries([Point(intersections.LONG.mean(), intersections.LAT.mean())])
    epicentre = epicentre.set_crs(4326)
    #epicentre = epicentre.to_crs({'init': 'epsg:26910'})

    return epicentre

def plot_epicentre(epicentre, gdf):
    print('Plotting Epicentre...')

    gdf = gdf.to_crs({'init': 'epsg:4326'}) #Setting GDF to lat/long
    ax = gdf.plot(marker="^", color='black')
    for x, y, label in zip(gdf.geometry.x, gdf.geometry.y, gdf.Station):
        ax.annotate(label, xy=(x, y), xytext=(3, 3), textcoords="offset points") #plotting names

    epicentre = epicentre.set_crs(gdf.crs, allow_override=True)
    epicentre.plot(ax=ax, color='red', marker='*')
    cx.add_basemap(ax, crs=gdf.crs)
    
    print("Done!")

    plt.savefig("epicentre.png")
    plt.show()

    print('\nThe epicentre is located at:\n' + 'LAT: ' + str(epicentre[0].y) +'\n' + 'LONG: ' + str(epicentre[0].x))
    print(str(epicentre[0].y), ",", str(epicentre[0].x))

gdf_localcrs = load_data()
radii = radii_calculations(gdf_localcrs)
epicentre = find_epicentre(gdf_localcrs, radii)
plot_epicentre(epicentre, gdf_localcrs)