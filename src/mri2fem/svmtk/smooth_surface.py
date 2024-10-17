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
    parser.add_argument("-o", "--output", type=Path, required=True, help="Output STL file")
    parser.add_argument("-n", type=int, default=3, help="Number of iterations")
    parser.add_argument("-l", "--edge-length", type=float, default=1.0, help="Taget Edge length")
    parser.add_argument(
        "-p",
        "--no-preserve-volume",
        action="store_false",
        help="Do not preserve volume",
    )


def main(input: Path, output: Path, n=1, eps=1.0, preserve_volume=True):
    assert input.is_file(), f"Input file {input} not found"
    logger = logging.getLogger(__name__)
    logger.info(
        "Running smoothen-surface with input=%s, output=%s, n=%s, eps=%s, preserve_volume=%s",
        input,
        output,
        n,
        eps,
        preserve_volume,
    )
    import SVMTK as svmtk

    # Load input STL file
    logger.debug("Loading input file")
    surface = svmtk.Surface(str(input))

    # Smooth using Taubin smoothing
    # if volume should be preserved,
    # otherwise use Laplacian smoothing

    if preserve_volume:
        logger.debug("Smoothing using Taubin smoothing")
        surface.smooth_taubin(n)
    else:
        logger.debug("Smoothing using Laplacian smoothing")
        surface.smooth_laplacian(eps, n)

    # Save smoothened STL surface
    logger.debug("Saving the smoothened surface")
    surface.save(str(output))

    logger.info("smoothen-surface done (output written to %s)", output)
