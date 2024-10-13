import argparse
import datetime
from genericpath import getmtime
import inspect
from typing import Callable
import cadquery as cq
import glob
import importlib
from os.path import dirname, basename, join

CLI = False


def vscode_main(make: Callable, **kwargs):
    if inspect.currentframe().f_back.f_globals["__name__"] != "__main__":
        return

    if CLI:
        return

    from ocp_vscode import show, set_port, set_defaults, Camera

    set_port(3939)
    set_defaults(
        reset_camera=Camera.KEEP,
    )
    print("show")
    show(make(), **kwargs)


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
    parser.add_argument("-n", "--name", required=False)
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
                if args.name and args.name not in part:
                    continue
                fname = f"{OUT}/{part}.{ext}"
                print(part.ljust(40), ext.ljust(5), end=" ")
                if not args.force:
                    try:
                        target_time = getmtime(fname)
                    except FileNotFoundError:
                        target_time = -1
                    if target_time != -1 and source_time <= target_time:
                        print("not changed")
                        continue

                start = datetime.datetime.now()

                if not obj:
                    obj = make()
                    if isinstance(obj, cq.Assembly):
                        obj = obj.toCompound()
                cq.exporters.export(obj, fname)
                print(datetime.datetime.now() - start)
    return 0
