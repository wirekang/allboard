# %%
from allboard import vscode_main
from allboard.parts import vertical_key

STL = 1


def make():
    return vertical_key.make(
        length=13,
        width=11,
        angle=11,
        post_width=10,
        post_groove_width=0.75,
        post_groove_height=0.75,
        post_groove_y=2,
        post_magnet_y=5.4,
    )


vscode_main(make)
