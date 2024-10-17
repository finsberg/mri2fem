import argparse
from pathlib import Path

import logging


def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        required=True,
        help="Input surface file",
    )
    parser.add_argument("-o", "--output", type=Path, required=True, help="Output mesh file")
    parser.add_argument("-r", "--resolution", type=int, default=16)


def main(input: Path, output: Path, resolution: int = 16, **kwargs) -> None:
    assert input.is_file(), f"Input file {input} not found"
    logger = logging.getLogger(__name__)
    logger.info(
        "Running surface-to-mesh with input=%s, output=%s, resolution=%s", input, output, resolution
    )

    import SVMTK as svmtk

    # Load input file
    logger.debug("Loading input file")
    surface = svmtk.Surface(str(input))

    # Generate the volume mesh
    logger.debug("Generating the volume mesh")
    domain = svmtk.Domain(surface)
    domain.create_mesh(resolution)

    # Write the mesh to the output file
    logger.debug("Writing the mesh to the output file")
    domain.save(str(output))

    logger.info("surface-to-mesh done (output written to %s)", output)
