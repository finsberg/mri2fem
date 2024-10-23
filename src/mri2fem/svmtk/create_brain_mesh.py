from pathlib import Path
import logging
import argparse


def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "-ilp",
        "--input-lh-pial",
        type=Path,
        required=True,
        help="Input Left Hemisphere Pial STL file",
    )
    parser.add_argument(
        "-irp",
        "--input-rh-pial",
        type=Path,
        required=True,
        help="Input Right Hemisphere Pial STL file",
    )
    parser.add_argument(
        "-ilw",
        "--input-lh-white",
        type=Path,
        required=True,
        help="Input Left Hemisphere While STL file",
    )
    parser.add_argument(
        "-irw",
        "--input-rh-white",
        type=Path,
        required=True,
        help="Input Right Hemisphere While STL file",
    )
    parser.add_argument(
        "-ilv",
        "--input-lh-ventricles",
        type=Path,
        required=True,
        help="Input Right Hemisphere While STL file",
    )
    parser.add_argument("-o", "--output", type=Path, required=True, help="Output STL file")
    parser.add_argument(
        "-r",
        "--resolution",
        type=int,
        default=32,
        help="Resolution of the mesh",
    )
    parser.add_argument(
        "--remove-ventricles",
        action="store_true",
        help="Remove ventricles from the mesh",
    )


def main(
    input_lh_pial,
    input_rh_pial,
    input_lh_white,
    input_rh_white,
    input_ventricles,
    output,
    resolution=32,
    remove_ventricles=True,
):
    assert input_lh_pial.is_file(), f"Input file {input_lh_pial} not found"
    assert input_rh_pial.is_file(), f"Input file {input_rh_pial} not found"
    assert input_lh_white.is_file(), f"Input file {input_lh_white} not found"
    assert input_rh_white.is_file(), f"Input file {input_rh_white} not found"
    assert input_ventricles.is_file(), f"Input file {input_ventricles} not found"
    logger = logging.getLogger(__name__)
    logger.info(
        "Creating a mesh for the brain, with input files: %s, %s, %s, %s, %s",
        input_lh_pial,
        input_rh_pial,
        input_lh_white,
        input_rh_white,
        input_ventricles,
    )

    import SVMTK as svmtk

    logger.debug("Loading input files")
    lh_pial = svmtk.Surface(str(input_lh_pial))
    rh_pial = svmtk.Surface(str(input_rh_pial))
    lh_white = svmtk.Surface(str(input_lh_white))
    rh_white = svmtk.Surface(str(input_rh_white))
    lh_ventricles = svmtk.Surface(str(input_ventricles))

    white = lh_white
    white.union(rh_white)

    # TODO: Might consider passing in the markers and
    # resolution as arguments
    # Define identifying tags for the different regions
    tags = {"pial": 1, "white": 2, "ventricle": 3}

    # Create a map for the subdomains with tags
    # 1 for inside the first and outside the second ("10")
    # 2 for inside the first and inside the second ("11")
    logger.debug("Creating subdomain map")
    smap = svmtk.SubdomainMap()
    smap.add("1000", tags["pial"])
    smap.add("0100", tags["pial"])
    smap.add("1010", tags["white"])
    smap.add("0110", tags["white"])
    smap.add("1110", tags["white"])
    smap.add("1011", tags["ventricle"])
    smap.add("0111", tags["ventricle"])
    smap.add("1111", tags["ventricle"])

    surfaces = [lh_pial, rh_pial, white, lh_ventricles]

    # Generate mesh at given resolution
    domain = svmtk.Domain(surfaces, smap)
    domain.create_mesh(resolution)

    # Remove ventricles perhaps
    if remove_ventricles:
        domain.remove_subdomain(tags["ventricle"])

    # Save mesh
    domain.save(str(output))

    logger.info("create-brain-mesh done (output written to %s)", output)
