# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Artg4tk(CMakePackage):
    """Artg4tk"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/artg4tk/wiki"
    url = "https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/artg4tk.v10_02_01.tbz2"
    git_base = "https://cdcvs.fnal.gov/projects/artg4tk"

    # version('10.04.00', sha256='44a1e12425ff2ebe90f7482ad2b10cbde873477815f81707677eb2ad14d3cef4')
    version("10.04.00", tag="v10_04_00", git=git_base, get_full_repo=True)
    version(
        "c06a0ed7a0a543cba5c23fc588f7dd6dcb6609e2",
        commit="c06a0ed7a0a543cba5c23fc588f7dd6dcb6609e2",
        git=git_base,
        get_full_repo=True,
    )
    version("develop", branch="develop", git=git_base, get_full_repo=True)
    version("mwm1", branch="mwm1", git=git_base, get_full_repo=True)
    version("MVP1a", branch="feature/Spack-MVP1a", git=git_base, get_full_repo=True)
    version("10.02.01", tag="v10_02_01", git=git_base, get_full_repo=True)
    version("10.02.01.01", tag="v10_02_01_01", git=git_base, get_full_repo=True)
    version("09.04.04", tag="v09_04_04", git=git_base, get_full_repo=True)
    version("09.05.00", tag="v09_05_00", git=git_base, get_full_repo=True)
    version("09.05.01", tag="v09_05_01", git=git_base, get_full_repo=True)
    version("09.05.02", tag="v09_05_02", git=git_base, get_full_repo=True)
    version("09.06.00", tag="v09_06_00", git=git_base, get_full_repo=True)
    version("09.04.04", tag="v09_04_04", git=git_base, get_full_repo=True)
    version("09.05.00", tag="v09_05_00", git=git_base, get_full_repo=True)
    version("09.05.01", tag="v09_05_01", git=git_base, get_full_repo=True)
    version("09.05.02", tag="v09_05_02", git=git_base, get_full_repo=True)
    version("09.06.00", tag="v09_06_00", git=git_base, get_full_repo=True)
    version("09.07.00", tag="v09_07_00", git=git_base, get_full_repo=True)
    version("09.07.01", tag="v09_07_01", git=git_base, get_full_repo=True)

    variant(
        "cxxstd",
        default="17",
        values=("14", "17"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    patch(
        "cetmodules2-c06a0ed7a0a543cba5c23fc588f7dd6dcb6609e2.patch",
        when="@c06a0ed7a0a543cba5c23fc588f7dd6dcb6609e2",
    )
    # patch('mwm.patch')
    depends_on("cetmodules", type="build")
    depends_on("cetbuildtools", type="build")
    depends_on("art")
    depends_on("art-root-io")
    depends_on("canvas-root-io")
    depends_on("geant4")
    depends_on("root")
    depends_on("boost")

    def cmake_args(self):
        args = ["-DCMAKE_CXX_STANDARD={0}".format(self.spec.variants["cxxstd"].value)]
        return args

    def url_for_version(self, version):
        url = "https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/{0}.v{1}.tbz2"
        return url.format(self.name, version.underscored)

    def flag_handler(self, name, flags):
        if name == "cxxflags" and self.spec.compiler.name == "gcc":
            flags.append("-Wno-error=deprecated-declarations")
            flags.append("-Wno-error=class-memaccess")
        return (flags, None, None)

    def setup_build_environment(self, spack_env):
        spack_env.set("CETBUILDTOOLS_VERSION", self.spec["cetmodules"].version)
        spack_env.set("CETBUILDTOOLS_DIR", self.spec["cetmodules"].prefix)
        spack_env.set("LD_LIBRARY_PATH", self.spec["root"].prefix.lib)
