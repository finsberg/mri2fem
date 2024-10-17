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
    parser.add_argument("-l", "--edge-length", type=float, default=1.0, help="Taget Edge length")
    parser.add_argument("-n", "--niter", type=int, default=3, help="Number of iterations")
    parser.add_argument(
        "-p",
        "--do-not-move-boundary-edges",
        action="store_true",
        help="Protect boundary edges from moving",
    )


def main(input: Path, output, edge_length, niter, do_not_move_boundary_edges=False):
    assert input.is_file(), f"Input file {input} not found"
    logger = logging.getLogger(__name__)
    logger.info(
        "Running remesh-surface with input=%s, output=%s, "
        "edge_length=%s, niter=%s, do_not_move_boundary_edges=%s",
        input,
        output,
        edge_length,
        niter,
        do_not_move_boundary_edges,
    )
    import SVMTK as svmtk

    # Load input STL file
    logger.debug("Loading input file")
    surface = svmtk.Surface(str(input))

    # Remesh surface
    logger.debug("Remeshing the surface")
    surface.isotropic_remeshing(edge_length, niter, do_not_move_boundary_edges)

    # Save remeshed STL surface
    logger.debug("Saving the remeshed surface")
    surface.save(str(output))

    logger.info("remesh-surface done (output written to %s)", output)
