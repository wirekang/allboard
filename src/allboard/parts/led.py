"""
IR908-7C-F
PT908-7B-F
"""
# %%

from cadquery import Workplane
from allboard import vscode_main

base_length = 1.5
base_width = 4.5
base_height = 5.7
lens_diameter = 1.5
lens_z = 4.5


def make():
    lens = Workplane().sphere(lens_diameter / 2)
    base = (
        Workplane()
        .box(base_length, base_width, base_height)
        .translate((0, 0, base_height / 2))
    )

    result = base.union(lens.translate((lens_diameter / 2, 0, lens_z)))

    return result


vscode_main(make)
