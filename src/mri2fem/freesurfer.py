from pathlib import Path
import argparse
import shutil
import subprocess
import logging

from . import utils

# Download the license and put it in the .freesurfer folder in your home directory
# mkdir -p "$HOME"/.freesurfer
# cp license.txt "$HOME"/.freesurfer/license.txt

logger = logging.getLogger(__name__)


def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "-e",
        "--entrypoint",
        type=str,
        default="/bin/bash",
        help="Entrypoint to run in the container",
    )
    parser.add_argument(
        "-i",
        "--image-name",
        type=str,
        default=utils.get_env_or_default("FREESURFER_IMAGE", "freesurfer:latest"),
        help="Name of the freesurfer docker image",
    )


def check_license(LICESENS_DIR: Path) -> bool:
    license_file = LICESENS_DIR / "license.txt"
    if not license_file.exists():
        msg = (
            f"License file {license_file} not found. Please download "
            "the license file and put it in the .freesurfer folder in your home directory"
        )
        logger.info(msg)
        return False
    return True


def check_docker(image_name: str) -> bool:
    docker = shutil.which("docker")
    if docker is None:
        logger.info("Docker not found")
        return False
    ret = subprocess.run([docker, "images", "-q", image_name], capture_output=True)
    if ret.returncode != 0 or ret.stdout == b"":
        logger.warning(f"Docker image {image_name} not found")
        return False
    return True


def main(): ...


def run(
    args: list[str],
    RESULTS_DIR=Path.cwd(),
    SUBJECTS_DIR=Path.cwd(),
    entrypoint: str = "/bin/bash",
    LICESENS_DIR=Path.home() / ".freesurfer",
    image_name="freesurfer2:latest",
):
    # Check first if the entrypoint exist as a command
    if shutil.which(entrypoint) is not None:
        # We are in an environment where the entrypoint is available
        # so just run the command directly
        logger.info(" ".join([entrypoint] + args))
        subprocess.run([entrypoint] + args)
        return

    if not (check_docker(image_name) and check_license(LICESENS_DIR)):
        return

    docker_cmd = [
        "docker",
        "run",
        "--rm",
        "-v",
        f"{SUBJECTS_DIR}:/usr/local/freesurfer/subjects",
        "-v",
        f"{RESULTS_DIR}:/usr/local/freesurfer/results",
        "-v",
        f"{LICESENS_DIR}:/usr/local/freesurfer/license",
        "-e",
        "FS_LICENSE=/usr/local/freesurfer/license/license.txt",
        "-e",
        "SUBJECTS_DIR=/usr/local/freesurfer/subjects",
        "-e",
        "RESULTS_DIR=/usr/local/freesurfer/results",
        "--entrypoint",
        entrypoint,
        "-t",
        image_name,
    ]
    full_cmd = docker_cmd + args
    logger.info(" ".join(full_cmd))

    subprocess.run(full_cmd)
