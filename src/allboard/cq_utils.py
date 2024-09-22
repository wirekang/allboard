import cadquery


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
