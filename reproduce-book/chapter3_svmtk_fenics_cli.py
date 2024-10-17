from pathlib import Path
import subprocess

here = Path(__file__).absolute().parent
DATADIR = here / ".." / "data" / "chp3"


def main():
    ret = subprocess.run(
        [
            "mri2fem",
            "-v",
            "surface-to-mesh",
            "--input",
            str(DATADIR / "lh.pial.stl"),
            "--output",
            str(DATADIR / "lh.mesh"),
        ]
    )
    assert ret.returncode == 0
    ret = subprocess.run(
        [
            "mri2fem",
            "-v",
            "surface-to-mesh",
            "--input",
            str(DATADIR / "lh.pial.stl"),
            "--output",
            str(DATADIR / "lh64.mesh"),
            "--resolution",
            "64",
        ]
    )
    assert ret.returncode == 0
    ret = subprocess.run(
        [
            "meshio",
            "convert",
            str(DATADIR / "lh.mesh"),
            str(DATADIR / "lh.xdmf"),
        ]
    )
    assert ret.returncode == 0
    ret = subprocess.run(
        [
            "mri2fem",
            "-v",
            "remesh-surface",
            "--input",
            str(DATADIR / "lh.pial.stl"),
            "--output",
            str(DATADIR / "lh.pial.remesh.stl"),
            "--L",
            "1.0",
            "--n",
            "3",
        ]
    )
    assert ret.returncode == 0
    ret = subprocess.run(
        [
            "mri2fem",
            "-v",
            "smooth-surface",
            "--input",
            str(DATADIR / "lh.pial.remesh.stl"),
            "--output",
            str(DATADIR / "lh.pial.smooth.stl"),
            "--n",
            "10",
            "--eps",
            "1.0",
        ]
    )
    assert ret.returncode == 0
    ret = subprocess.run(
        [
            "mri2fem",
            "-v",
            "repair",
            "--input",
            str(DATADIR / "lh.pial.smooth.stl"),
            "--fill-holes",
            "--separate-narrow-gaps",
            "--adjustment",
            "-0.25",
        ]
    )
    assert ret.returncode == 0
    ret = subprocess.run(
        [
            "mri2fem",
            "-v",
            "surface-to-mesh",
            "--input",
            str(DATADIR / "lh.pial.smooth.stl"),
            "--output",
            str(DATADIR / "ernie.mesh"),
        ]
    )
    assert ret.returncode == 0
    ret = subprocess.run(
        [
            "meshio",
            "convert",
            str(DATADIR / "ernie.mesh"),
            str(DATADIR / "ernie.xml"),
        ]
    )
    assert ret.returncode == 0
    ret = subprocess.run(
        [
            "meshio",
            "convert",
            str(DATADIR / "ernie.xml"),
            str(DATADIR / "ernie.xdmf"),
        ]
    )
    assert ret.returncode == 0


if __name__ == "__main__":
    raise SystemExit(main())
