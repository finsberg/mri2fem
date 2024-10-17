from pathlib import Path
import logging
import argparse


def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        required=True,
        help="Input STL file",
    )
    parser.add_argument(
        "-f",
        "--fill-holes",
        action="store_false",
        help="Fill holes in the surface",
    )
    parser.add_argument(
        "-s",
        "--separate-narrow-gaps",
        action="store_false",
        help="Separate narrow gaps in the surface",
    )
    parser.add_argument(
        "-a",
        "--adjustment",
        type=float,
        default=-0.33,
        help="Adjustment multiplier of the edge movement",
    )


def main(input: Path, fill_holes=True, separate_narrow_gaps=True, adjustment=-0.33):
    assert input.is_file(), f"Input file {input} not found"
    logger = logging.getLogger(__name__)
    import SVMTK as svmtk

    # Load input STL file
    logger.debug("Loading input file")
    surface = svmtk.Surface(str(input))

    # Find and fill holes
    if fill_holes:
        logger.debug("Filling holes")
        surface.fill_holes()

    # Separate narrow gaps

    if separate_narrow_gaps:
        logger.debug("Separating narrow gaps")
        surface.separate_narrow_gaps(adjustment)

    logger.info("smoothen-surface done")
