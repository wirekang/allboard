# %%

from cadquery import Workplane
from allboard import entrypoint


def make():
    return Workplane()


entrypoint(make())
