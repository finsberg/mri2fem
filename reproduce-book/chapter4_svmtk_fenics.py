import logging

from mri2fem import svmtk, utils

from config import DATADIR


def main():
    logging.basicConfig(level=logging.DEBUG)

    svmtk.create_gw_mesh.main(
        DATADIR / "lh.pial.stl", DATADIR / "lh.white.stl", DATADIR / "ernie-gw.mesh"
    )
    utils.meshio_convert(DATADIR / "ernie-gw.mesh", DATADIR / "ernie-gw.vtu")
    # Next extract ventricles and convert the rh files with freesurfer


if __name__ == "__main__":
    raise SystemExit(main())
