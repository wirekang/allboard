# %%
from allboard import vscode_main
from allboard.parts import cluster, vertical_key


STL = 1


def make():
    return vertical_key.make(
        length=13,
        width=8,
        angle=0,
        post_width=cluster.post_width,
        post_groove_width=cluster.post_groove_width,
        post_groove_height=cluster.post_groove_height,
        post_groove_y=cluster.post_groove_y,
        post_magnet_y=cluster.post_magnet_y,
    )


vscode_main(make)
