import cadquery


def tbox(
    length, width, height, vector, centered=False, workplane=None
) -> cadquery.Workplane:
    """
    translated box
    """
    if not workplane:
        workplane = cadquery.Workplane()
    return workplane.box(length, width, height, centered).translate(vector)
