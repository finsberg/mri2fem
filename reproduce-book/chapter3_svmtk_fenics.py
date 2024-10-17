from mri2fem import (
    freesurfer,
    utils,
    svmtk,
    fenics,
)

from config import MRI2FEMDATADIR, SUBJECTS_DIR, DATADIR, setup_logging


def main():
    setup_logging()

    lh_pial = MRI2FEMDATADIR / "freesurfer" / "ernie" / "surf" / "lh.pial"
    assert lh_pial.exists(), f"File {lh_pial} not found. Please download the data first"

    lh_pial_stl = DATADIR / "ernie" / "lh.pial.stl"
    lh_pial_stl.parent.mkdir(exist_ok=True, parents=True)
    freesurfer.run(
        entrypoint="mris_convert",
        args=[
            "/usr/local/freesurfer/subjects/" + str(lh_pial.relative_to(SUBJECTS_DIR)),
            "/usr/local/freesurfer/results/" + str(lh_pial_stl.relative_to(DATADIR)),
        ],
        SUBJECTS_DIR=str(SUBJECTS_DIR),
        RESULTS_DIR=str(DATADIR),
    )

    lh_mesh = DATADIR / "ernie" / "lh.mesh"

    svmtk.surface_to_mesh.main(lh_pial_stl, lh_mesh)
    assert lh_mesh.exists()

    lh_mesh64 = DATADIR / "ernie" / "lh64.mesh"
    svmtk.surface_to_mesh.main(lh_pial_stl, lh_mesh64, resolution=64)
    assert lh_mesh64.exists()

    lh_xdmf = DATADIR / "ernie" / "lh.xdmf"
    utils.meshio_convert(lh_mesh, lh_xdmf)
    assert lh_xdmf.exists()

    lh_pial_remesh_stl = DATADIR / "ernie" / "lh.pial.remesh.stl"
    svmtk.remesh_surface.main(lh_pial_stl, lh_pial_remesh_stl, 1.0, 3)
    assert lh_pial_remesh_stl.exists()

    lh_pial_smooth_stl = DATADIR / "ernie" / "lh.pial.smooth.stl"
    svmtk.smooth_surface.main(lh_pial_remesh_stl, lh_pial_smooth_stl, n=10, eps=1.0)
    assert lh_pial_smooth_stl.exists()

    svmtk.repair.main(
        lh_pial_smooth_stl, fill_holes=True, separate_narrow_gaps=True, adjustment=-0.25
    )

    ernie_mesh = DATADIR / "ernie" / "ernie.mesh"
    svmtk.surface_to_mesh.main(lh_pial_smooth_stl, ernie_mesh)
    assert ernie_mesh.exists()

    ernie_xml = DATADIR / "ernie" / "ernie.xml"
    utils.meshio_convert(ernie_mesh, ernie_xml)
    assert ernie_xml.exists()

    ernie_xdmf = DATADIR / "ernie" / "ernie.xdmf"
    utils.meshio_convert(ernie_xml, ernie_xdmf)
    assert ernie_xdmf.exists()

    results_dir = DATADIR / "ernie" / "results_dolfin"
    results_dir.mkdir(exist_ok=True)
    fenics.diffusion_chp3.main(ernie_xdmf, results_dir)


if __name__ == "__main__":
    raise SystemExit(main())
