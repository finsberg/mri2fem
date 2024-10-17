from pathlib import Path
import logging
import argparse


def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "-ip",
        "--input-pial",
        type=Path,
        required=True,
        help="Input Pial STL file",
    )
    parser.add_argument(
        "-iw",
        "--input-white",
        type=Path,
        required=True,
        help="Input While STL file",
    )
    parser.add_argument("-o", "--output", type=Path, required=True, help="Output STL file")


def main(input_pial: Path, input_while: Path, output: Path):
    assert input_pial.is_file(), f"Input file {input_pial} not found"
    assert input_while.is_file(), f"Input file {input_while} not found"
    logger = logging.getLogger(__name__)
    logger.info(
        "Running create-gw-mesh with input_pial=%s, input_while=%s, output=%s",
        input_pial,
        input_while,
        output,
    )
    import SVMTK as svmtk

    logger.debug("Loading input files")
    pial = svmtk.Surface(str(input_pial))
    white = svmtk.Surface(str(input_while))
    surfaces = [pial, white]

    # TODO: Might consider passing in the markers and
    # resolution as arguments

    # Create a map for the subdomains with tags
    # 1 for inside the first and outside the second ("10")
    # 2 for inside the first and inside the second ("11")
    logger.debug("Creating subdomain map")
    smap = svmtk.SubdomainMap()
    smap.add("10", 1)
    smap.add("11", 2)

    # Create a tagged domain from the list of surfaces
    # and the map
    logger.debug("Creating tagged domain")
    domain = svmtk.Domain(surfaces, smap)

    # Create and save the volume mesh
    resolution = 32
    logger.debug("Creating mesh")
    domain.create_mesh(resolution)
    logger.debug("Saving the mesh")
    domain.save(str(output))

    logger.info("create-gw-mesh done (output written to %s)", output)
