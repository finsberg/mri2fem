import argparse
import typing

from . import surface_to_mesh, remesh_surface, smooth_surface, repair, create_gw_mesh

__all__ = [
    "add_svmtk_parser",
    "dispatch",
    "surface_to_mesh",
    "remesh_surface",
    "smooth_surface",
    "repair",
    "create_gw_mesh",
]


def add_svmtk_parser(parser: argparse.ArgumentParser) -> None:
    subparsers = parser.add_subparsers(dest="svmtk-command")

    # Surface to mesh parser
    surface_to_mesh_parser = subparsers.add_parser(
        "surface-to-mesh", help="Convert a surface to a mesh"
    )
    surface_to_mesh.add_arguments(surface_to_mesh_parser)

    # Remesh surface parser
    remesh_surface_parser = subparsers.add_parser("remesh-surface", help="Remesh a surface")
    remesh_surface.add_arguments(remesh_surface_parser)

    # Smooth surface parser
    smooth_surface_parser = subparsers.add_parser("smooth-surface", help="Smooth a surface")
    smooth_surface.add_arguments(smooth_surface_parser)

    # Repair parser
    repair_parser = subparsers.add_parser("repair", help="Repair a surface")
    repair.add_arguments(repair_parser)

    # create-gw-mesh parser
    create_gw_mesh_parser = subparsers.add_parser(
        "create-gw-mesh", help="Create a mesh for groundwater flow"
    )
    create_gw_mesh.add_arguments(create_gw_mesh_parser)


def dispatch(command, args: dict[str, typing.Any]) -> int:
    if command == "surface-to-mesh":
        surface_to_mesh.main(**args)

    elif command == "remesh-surface":
        remesh_surface.main(**args)

    elif command == "smooth-surface":
        smooth_surface.main(**args)

    elif command == "repair":
        repair.main(**args)

    elif command == "create-gw-mesh":
        create_gw_mesh.main(**args)

    else:
        raise ValueError(f"Unknown command {command}")

    return 0
