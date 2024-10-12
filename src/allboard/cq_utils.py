import cadquery

from allboard.utils import run_multithread


def tbox(
    length, width, height, vector, centered=True, workplane=None
) -> cadquery.Workplane:
    """
    translated box
    """
    if not workplane:
        workplane = cadquery.Workplane()
    return workplane.box(length, width, height, centered).translate(vector)


def tapered_cylinder(
    bottom_diameter, top_diameter, height, workplane=None
) -> cadquery.Workplane:
    if not workplane:
        workplane = cadquery.Workplane()
    return (
        workplane.circle(bottom_diameter / 2)
        .workplane(height)
        .circle(top_diameter / 2)
        .loft(combine=False)
    )

def union_padding(
    wp: cadquery.Workplane,
    *,
    x=0,
    y=0,
    z=0,
):
    result = wp
    dx = [0]
    dy = [0]
    dz = [0]
    if x != 0:
        dx.append(-x / 2)
        dx.append(x / 2)
    if y != 0:
        dy.append(-y / 2)
        dy.append(y / 2)
    if z != 0:
        dz.append(-z / 2)
        dz.append(z / 2)

    def f(x, y, z):
        nonlocal result
        result = result.union(wp.translate((x, y, z)))

    args = []
    for x in dx:
        for y in dy:
            for z in dz:
                args.append([x, y, z])
    run_multithread(args, f)

    return result