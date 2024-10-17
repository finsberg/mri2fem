import logging
import argparse

from . import svmtk, download_data, freesurfer


def setup_parser():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # Root parser
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Just print the command and do not run it",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print more information",
    )

    subparsers = parser.add_subparsers(dest="command")

    # Download data parser
    download_data_parser = subparsers.add_parser("download-data", help="Download the sample data")
    download_data.add_arguments(download_data_parser)

    # SVMTK parser
    svmtk_parser = subparsers.add_parser("svmtk", help="Surface and volume meshing toolkit")
    svmtk.add_svmtk_parser(svmtk_parser)

    # Freesurfer parser
    freesurfer_parser = subparsers.add_parser("freesurfer", help="Run freesurfer")
    freesurfer.add_arguments(freesurfer_parser)

    return parser


def dispatch(parser: argparse.ArgumentParser) -> int:
    args = vars(parser.parse_args())
    logging.basicConfig(level=logging.DEBUG if args.pop("verbose") else logging.INFO)

    logger = logging.getLogger(__name__)
    dry_run = args.pop("dry_run")
    command = args.pop("command")

    if dry_run:
        logger.info("Dry run: %s", command)
        logger.info("Arguments: %s", args)
        return 0

    try:
        if command == "download-data":
            download_data.main(**args)
        elif command == "svmtk":
            svmtk.dispatch(args.pop("svmtk-command"), args)
        else:
            logger.error(f"Unknown command {command}")
            parser.print_help()
    except ValueError as e:
        logger.error(e)
        parser.print_help()

    return 0


def main() -> int:
    parser = setup_parser()

    return dispatch(parser)
