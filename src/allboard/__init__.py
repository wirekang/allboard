import argparse
from genericpath import getmtime
import inspect
import time
from typing import Any
import cadquery as cq
import glob
import importlib
from os.path import dirname, basename, join

CLI = False


def vscode_main(*args, **kwargs):
    if CLI:
        return

    from ocp_vscode import show, set_port, set_defaults, Camera

    set_port(3939)
    set_defaults(reset_camera=Camera.KEEP)
    show(*args, **kwargs)


def export():
    global CLI
    CLI = True
    print("export\n")
    TYPES = [
        ("STL", "stl"),
        ("DXF", "dxf"),
    ]
    OUT = "out"

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--force", action="store_true")
    args = parser.parse_args()

    files = glob.glob(join(dirname(__file__), "parts", "*.py"))

    for file in files:
        part = basename(file)[:-3]
        if part.startswith("_"):
            continue
        module = importlib.import_module(f"allboard.parts.{part}")
        make = getattr(module, "make", None)
        if make is None:
            continue

        source_time = getmtime(file)
        obj = None

        for attr, ext in TYPES:
            if hasattr(module, attr) and getattr(module, attr):
                fname = f"{OUT}/{part}.{ext}"
                print(part.ljust(50), ext.ljust(5), end=" ")
                if not args.force:
                    try:
                        target_time = getmtime(fname)
                    except FileNotFoundError:
                        target_time = -1
                    if target_time != -1 and source_time <= target_time:
                        print("not changed")
                        continue

                start = time.time_ns()

                if not obj:
                    obj = make()
                    if isinstance(obj, cq.Assembly):
                        obj = obj.toCompound()
                cq.exporters.export(obj, fname)
                print(int((time.time_ns() - start) / 1000000))
    return 0
