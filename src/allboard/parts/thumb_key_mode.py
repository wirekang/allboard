# %%
from cadquery import Workplane
from allboard import vscode_main
from allboard.parts import thumb_cluster_right, vertical_key, vertical_key_post


STL = 1


width0 = 16
width1 = 20
angle1 = 67


def make():
    length = vertical_key.post_length
    height = vertical_key.height
    post = vertical_key_post.make(
        length=length,
        width=thumb_cluster_right.post_width + width0,
        height=height,
        groove_width=thumb_cluster_right.post_groove_width,
        groove_height=thumb_cluster_right.post_groove_height,
        groove_y=thumb_cluster_right.post_groove_y,
        magnet_y=thumb_cluster_right.post_magnet_y,
    )

    p1 = (
        Workplane()
        .box(
            length,
            width1,
            height,
        )
        .translate((0, width1 / 2, 0))
        .rotate((0, 0, 0), (1, 0, 0), angle1)
        .translate((0, (thumb_cluster_right.post_width + width0) / 2, 0))
        .faces("<Y or >Y")
        .fillet(0.5)
        .translate((0, -0.7, 0))
    )
    return post.union(p1, tol=0.3)



vscode_main(make)
