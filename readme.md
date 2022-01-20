# Epicentre Finder

A seismology script created with Python 3.9.9

## Table of Contents
1. [Description](#Description)
2. [Visualization](#Visualization)
3. [Usage](#Usage)
    1. [The Script](#script)
    2. [The Data](#data)
4. [Outputs](#Outputs)
5. [Organization](#Organization)


## Description

This script estimates earthquake epicentres using the following information:
* P and S wave arrival times (handpicked)
* Seismometer locations
* Local wave speeds

The P and S wave arrival times associated with each station are used to draw rings of radius R around each station, where R is the approximate distance of the station to the epicentre. The group of points representing the densest cluster of overlapping points between these rings is then averaged, and the epicentre is plotted on a basemap.

## Visualization

A visualization of the method this script uses to find epicentres. The blue dots represent seismometers/stations, and the blue rings' radii vary depending on the P and S wave arrival times at each respective seismometer/station. Orange points are plotted at every intersection between the rings, and outliers are trimmed until only points in the densest cluster of overlaps remains, as in the second image. The averaged location of points in the densest cluster is then set as the epicentre and plotted against a basemap. 

![Initial plot](https://i.imgur.com/u6Gj408.png)
![Trimming outliers](https://i.imgur.com/HCF2qjm.png)
![Added basemap](https://i.imgur.com/9P2VTST.png)
![Final result](https://i.imgur.com/JL3vCrU.png)

## Usage

### The Script <a name="script"></a>

Install the required packages locally using requirements.txt

```
pip install -r requirements.txt
```

Navigate to the **src** directory and run

```
python epicentre_finder.py *PATH TO DATAFILE (.csv)*
```

### The Data <a name="data"></a>

A .csv file containing the following information is required:

Station | TS | TP | LAT | LONG | VS | VP
---|---|---|---|---|---|---
Station names | S-wave arrival times (s) | P-wave arrival times (s) | Latitudes of stations | Longitudes of stations | Local S-wave speed (m/s) | Local P-wave speed (m/s)

The wave speeds (VS, VP) only need to be specified in one row. The S and P wave arrival times are all relative to a common point in time, and must be selected from raw seismometer data prior to being fed into this script.



**Example**

Station | TS | TP | LAT | LONG | VS | VP
---|---|---|---|---|---|---
Frank Dawson Adams building | 12.4 | 7.82 | 45.50552978120353 | -73.57522984289152 | 2300 | 4680
IKEA Boucherville | 8.72 | 4.58 | 45.57247265317202 | -73.40117329505202 | |
Montreal-Mirabel International Airport | 21.3 | 14.5 | 45.671640840480165 | -74.03327505426336 | |

## Outputs

The script will automatically open a pyplot plot showing the epicentre's location, along with a basemap and station locations. This plot is also saved as `epicentre.png` within the **src** directory.

The script will also output the latitude/longitude of the epicentre on the terminal.

_Example output_


```
The epicentre is located at:
LAT: 35.395303206618905
LONG: 139.46674702654076
35.395303206618905 , 139.46674702654076
```

## Organization
```
|-- readme.md
|-- readmejp.md
|-- requirements.txt
|-- src
    |-- epicentre_finder.py 
    |-- latlong_to_utmepsg.py
```









