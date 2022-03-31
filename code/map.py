"""
map.py: exploratory data analysis

Sandy H. S. Herho <herho@umd.edu> 
03/17/2022 
"""

# import lib
import pygmt

# download SRTM15+ data
gridMC = pygmt.datasets.load_earth_relief(resolution="15s", region=[92, 170, -20, 20])

# plot map
fig = pygmt.Figure()
fig.grdimage(grid=gridMC, projection="M15c", frame="a", cmap="geo")
fig.plot(x=109.76111, y=-7.03056, style="c0.2c", color="red")
fig.colorbar(frame=["a2000", "x+lElevation", "y+lm"])
fig.savefig('../figs/fig1.png')