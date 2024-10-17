import logging
import os
from pathlib import Path

import meshio

logger = logging.getLogger(__name__)


def meshio_convert(input: Path, output: Path) -> None:
    logger.info("Converting %s to %s", input, output)
    mesh = meshio.read(input)
    meshio.write(output, mesh)


def get_env_or_default(env_name: str, default: str) -> str:
    return os.environ.get(env_name, default)
