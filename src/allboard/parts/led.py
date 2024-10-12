"""
IR908-7C-F
PT908-7B-F
"""
# %%

from cadquery import Workplane
from allboard import vscode_main

base_length = 4.5
base_width = 1.5
base_height = 5.7
lens_diameter = 1.5
lens_z = 4.5
pin_length = 0.5
pin_width = 0.5
pin_height = 10
pin_distance = 2.54


def make():
    lens = Workplane().sphere(lens_diameter / 2)
    base = (
        Workplane()
        .box(base_length, base_width, base_height)
        .translate((0, base_width / 2, base_height / 2))
    )

    def pin():
        return Workplane().box(pin_length, pin_width, pin_height)

    result = (
        base.union(lens.translate((0, 0, lens_z)))
        .union(pin().translate((-pin_distance / 2, base_width / 2, -pin_height / 2)))
        .union(pin().translate((pin_distance / 2, base_width / 2, -pin_height / 2)))
    )

    return result


vscode_main(make)
