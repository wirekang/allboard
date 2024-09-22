# %%
import cadquery

from allboard import entrypoint


def key_center():
    return cadquery.Workplane()


entrypoint(key_center())
