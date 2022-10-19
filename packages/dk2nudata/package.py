# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dk2nudata(CMakePackage):
    """This package consolidates the disparate formats of neutrino beam simulation "flux" files."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/dk2nu"
    url = "https://cdcvs.fnal.gov/subversion/dk2nu/tags/v01_07_02"

    version("01.10.00", revision="154", svn="https://cdcvs.fnal.gov/subversion/dk2nu/trunk")
    version("01.09.02", revision="153", svn="https://cdcvs.fnal.gov/subversion/dk2nu/trunk")
    version("01.09.01", revision="152", svn="https://cdcvs.fnal.gov/subversion/dk2nu/trunk")
    version("01.09.00", revision="148", svn="https://cdcvs.fnal.gov/subversion/dk2nu/trunk")
    version("01.08.00", revision="146", svn="https://cdcvs.fnal.gov/subversion/dk2nu/trunk")
    version("01.07.02", revision="140", svn="https://cdcvs.fnal.gov/subversion/dk2nu/trunk")

    # Variant is still important even though it's not passed to compiler
    # flags (use of ROOT, etc.).
    variant(
        "cxxstd",
        default="11",
        values=("11", "14", "17"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("cmake", type="build")
    depends_on("root")
    depends_on("tbb")
    depends_on("libxml2")
    depends_on("log4cpp")
    depends_on("tbb")

    parallel = False

    root_cmakelists_dir = "dk2nu"

    def cmake_args(self):
        args = ["-DWITH_GENIE=OFF", "-DTBB_LIBRARY=%s/libtbb.so" % self.spec["tbb"].prefix.lib]
        return args

    def setup_dependent_build_environment(self, spack_env, dspec):
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        spack_env.set("DK2NUDATA_LIB", self.prefix.lib)
        spack_env.set("DK2NUDATA_INC", self.prefix.include)

    def setup_dependent_run_environment(self, run_env, dspec):
        # Ensure we can find plugin libraries.
        run_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
