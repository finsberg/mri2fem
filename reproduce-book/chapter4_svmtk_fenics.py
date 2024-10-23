from pathlib import Path
from mri2fem import (
    freesurfer,
    utils,
    svmtk,
)

from extract_ventricles import extract_ventricles
from config import MRI2FEMDATADIR, SUBJECTS_DIR, DATADIR, setup_logging


def remesh_smooth_repair(stl: Path) -> Path:
    remesh_stl = stl.with_suffix(".remesh.stl")
    svmtk.remesh_surface.main(stl, remesh_stl, 1.0, 3)
    smooth_stl = stl.with_suffix(".smooth.stl")
    svmtk.smooth_surface.main(remesh_stl, smooth_stl, n=10, eps=1.0)
    svmtk.repair.main(smooth_stl, fill_holes=True, separate_narrow_gaps=True, adjustment=-0.25)
    return smooth_stl


def main():
    setup_logging()

    # Convert lh.pial, lh.white, rh.pial and rh.white to STL

    for name in ["lh.pial", "lh.white", "rh.pial", "rh.white"]:
        surf = MRI2FEMDATADIR / "freesurfer" / "ernie" / "surf" / name
        assert surf.exists(), f"File {surf} not found. Please download the data first"

        stl = DATADIR / "ernie" / f"{name}.stl"
        stl.parent.mkdir(exist_ok=True, parents=True)
        freesurfer.run(
            entrypoint="mris_convert",
            args=[
                "/usr/local/freesurfer/subjects/" + str(surf.relative_to(SUBJECTS_DIR)),
                "/usr/local/freesurfer/results/" + str(stl.relative_to(DATADIR)),
            ],
            SUBJECTS_DIR=str(SUBJECTS_DIR),
            RESULTS_DIR=str(DATADIR),
        )
        assert stl.exists()

    # # Remesh, smooth and repair the STL files

    lh_pial_smooth_stl = remesh_smooth_repair(DATADIR / "ernie" / "lh.pial.stl")
    lh_white_smooth_stl = remesh_smooth_repair(DATADIR / "ernie" / "lh.white.stl")
    rh_pial_smooth_stl = remesh_smooth_repair(DATADIR / "ernie" / "rh.pial.stl")
    rh_white_smooth_stl = remesh_smooth_repair(DATADIR / "ernie" / "rh.white.stl")

    # Generate gray-white mesh for left hemisphere
    ernie_gw_mesh = DATADIR / "ernie" / "ernie-gw.mesh"

    # svmtk.create_gw_mesh.main(lh_pial_smooth_stl, lh_white_smooth_stl, ernie_gw_mesh)
    svmtk.create_gw_mesh.main(
        DATADIR / "ernie" / "lh.pial.stl", DATADIR / "ernie" / "lh.white.stl", ernie_gw_mesh
    )
    assert ernie_gw_mesh.exists()

    ernia_gw_vtu = DATADIR / "ernie" / "ernie-gw.vtu"
    utils.meshio_convert(ernie_gw_mesh, ernia_gw_vtu)
    assert ernia_gw_vtu.exists()

    # # Now extract ventricles
    input = MRI2FEMDATADIR / "freesurfer" / "ernie" / "mri" / "wmparc.mgz"
    ventricles_stl = DATADIR / "ernie" / "ventricles.stl"
    extract_ventricles(ventricles_stl=ventricles_stl, input=input, postprocess=True)

    # Create brain mesh
    ernie_brain_32 = DATADIR / "ernie" / "ernie-brain-32.mesh"
    svmtk.create_brain_mesh.main(
        input_lh_pial=lh_pial_smooth_stl,
        input_lh_white=lh_white_smooth_stl,
        input_rh_pial=rh_pial_smooth_stl,
        input_rh_white=rh_white_smooth_stl,
        input_ventricles=ventricles_stl,
        output=ernie_brain_32,
        resolution=32,
    )


if __name__ == "__main__":
    raise SystemExit(main())
