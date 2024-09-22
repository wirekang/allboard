# %%
from allboard import entrypoint
import cadquery as cq

STL = 1
DXF = 1


def example():
    return cq.Workplane().box(1, 2, 2)


entrypoint(example())
