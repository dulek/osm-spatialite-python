# OpenStreetMaps + Spatialite + Python

This repository contains resources I've presented on second PyGDA meetup. The
purpose was to show how to use aformentioned technologies to start creating
Python apps that use geospatial information provided by OpenStreetMaps.

An application is simple example of pathfinder. To test it you need to install
some dependencies. In Ubuntu 14.04:

```
apt-get install spatialite-bin libspatialite5 libspatialite-dev
pip install shapely matplotlib
```

Also you need to install [Basemap library](http://matplotlib.org/basemap/users/download.html).

To run first generate Spatialite database running provided script:

```
./generate_db.sh
```

Then you can display shortest path between two points by simply calling:

```
python navi.py <origin_longitude> <origin_latitude> <destination_longitude>
<destination_latitude>
```

For example

```
python navi.py 15.107145309448242 46.532413816559455 15.195980072021484 45.805828539928356
```
