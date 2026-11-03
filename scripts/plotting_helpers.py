## GEOG41160: shared plotting/validation helpers
## Written in Week 5, Part 6 ("Write It Once -- Your Own Module"), as this
## course's example of "write it once, import it everywhere": the same
## colour-bar fix it replaces was found copied and pasted across three
## weeks of last year's teaching material.
##
## Used from Week 5 onward (Weeks 7 and 8 import it again). If a script can't
## find it: this file needs to sit in the same folder as the script or
## notebook importing it (or somewhere on your PYTHONPATH).


def fix_colorbar_height(fig, ax):
    """Resize a GeoPandas .plot() colour bar to match the map's height.

    GeoPandas' .plot(legend=True) often produces a colour bar taller than
    the map itself. This repositions it to match.
    """
    cbar = fig.axes[-1]
    pos = ax.get_position()
    cbar_pos = cbar.get_position()
    cbar.set_position([cbar_pos.x0, pos.y0, cbar_pos.width, pos.height])


## Week 5, Exercise 5 asks you to add check_crs(gdf, target_crs) here
## yourself, reusing the CRS-check habit from Weeks 3-4. Deliberately
## left out of this file so that exercise has something to do.
