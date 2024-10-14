# %%
from allboard import vscode_main
from allboard.parts import thumb_cluster_right, vertical_key

STL = 1


def make():
    return vertical_key.make(
        length=20,
        width=18,
        angle=0,
        post_width=thumb_cluster_right.post_width,
        post_groove_width=thumb_cluster_right.post_groove_width,
        post_groove_height=thumb_cluster_right.post_groove_height,
        post_groove_y=thumb_cluster_right.post_groove_y,
        post_magnet_y=thumb_cluster_right.post_magnet_y,
    )


vscode_main(make)
