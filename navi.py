import sys
import shapely.wkb
import sqlite3

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

db = sqlite3.connect('db.sqlite')
db.enable_load_extension(True)
db.load_extension('libspatialite')
cur = db.cursor()

fromX = sys.argv[1]
fromY = sys.argv[2]
toX = sys.argv[3]
toY = sys.argv[4]

node_query = "SELECT node_id, ST_Distance(geometry, MakePoint(%s, %s)) AS distance FROM roads_nodes ORDER BY distance LIMIT 1;" % (fromX, fromY)
cur.execute(node_query)
from_node = cur.fetchone()

from_node_id = from_node[0]
print 'Found closest from node: %s' % from_node_id

node_query = "SELECT node_id, ST_Distance(geometry, MakePoint(%s, %s)) AS distance FROM roads_nodes ORDER BY distance LIMIT 1;" % (toX, toY)
cur.execute(node_query)
to_node = cur.fetchone()

to_node_id = to_node[0]
print 'Found closest to node: %s' % to_node_id

route_query = "SELECT AsBinary(geometry) AS geom, ST_Length(geometry) AS lenght FROM roads_net WHERE NodeFrom=%s AND NodeTo=%s;" % (from_node_id, to_node_id)
cur.execute(route_query)
route = cur.fetchone()

path = shapely.wkb.loads(str(route[0]))

bounds_slovenia = (13.1781005859375, 45.321254361171476,
                   16.32568359375, 47.010225655683485)
# lower left minx miny , upper right maxx maxy
minx, miny, maxx, maxy = bounds_slovenia
w, h = maxx - minx, maxy - miny

# create a new matplotlib figure and axes instance
fig = plt.figure(figsize=(20, 20))  # Here we adjust size.
ax = fig.add_subplot(111)
m = Basemap(
    projection='merc',
    ellps='WGS84',
    llcrnrlon=minx - 0.2 * w,
    llcrnrlat=miny - 0.2 * h,
    urcrnrlon=maxx + 0.2 * w,
    urcrnrlat=maxy + 0.2 * h,
    lat_ts=0,
    resolution='i'
)
m.drawcoastlines(linewidth=1)
m.drawcountries(linewidth=1)

# set axes limits to basemap's coordinate reference system
min_x, min_y = m(minx, miny)
max_x, max_y = m(maxx, maxy)
corr_w, corr_h = max_x - min_x, max_y - min_y
ax.set_xlim(min_x - 0.2 * corr_w, max_x + 0.2 * corr_w)
ax.set_ylim(min_y - 0.2 * corr_h, max_y + 0.2 * corr_h)

x, y = path.xy
xys = []
for x, y in zip(x, y):
    xys.append(m(x, y))

x, y = map(list, zip(*xys))

ax.plot(x, y, color='#FF0000', linewidth=3, solid_capstyle='round',
        zorder=2)

plt.show()

