# 2x1.5mm N35 round(cylinder) magnet
# https://aliexpress.com/item/1005004868835603.html

# %%
from cadquery import Workplane
from allboard import vscode_main

diameter = 2
height = 1.5


def make():
    return Workplane().cylinder(height, diameter / 2)


vscode_main(make)
