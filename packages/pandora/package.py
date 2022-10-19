# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob

from spack import *


class Pandora(CMakePackage):
    """PandoraPFA Multi-algorithm pattern recognition"""

    homepage = "https://github.com/PandoraPFA"

    version(
        "03.11.01",
        git="https://github.com/PandoraPFA/PandoraPFA",
        tag="v03-11-01",
        get_full_repo=True,
    )
    version(
        "03.16.00",
        git="https://github.com/PandoraPFA/PandoraPFA",
        tag="v03-16-00",
        get_full_repo=True,
    )

    variant(
        "cxxstd",
        default="17",
        values=("14", "17"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("root")
    depends_on("eigen")

    def patch(self):
        # Build larpandoracontent as part of pandora
        filter_file(
            'LArContent_version "v03_13_01"', 'LArContent_version "v03_14_05"', "CMakeLists.txt"
        )
        filter_file(
            'Eigen3_version "3.3.3"',
            'Eigen3_version "{0}"'.format(self.spec["eigen"].version),
            "CMakeLists.txt",
        )
        filter_file(
            r"            EXPORT_LIBRARY_DEPENDENCIES\((.*)\)",
            """
            CMAKE_POLICY( PUSH )
            CMAKE_POLICY( SET CMP0033 OLD )
            EXPORT_LIBRARY_DEPENDENCIES( \\1 )
            CMAKE_POLICY( POP )""",
            "cmakemodules/MacroPandoraGeneratePackageConfigFiles.cmake",
        )

    def cmake_args(self):
        args = [
            "-DCMAKE_CXX_STANDARD={0}".format(self.spec.variants["cxxstd"].value),
            "-DCMAKE_CXX_FLAGS=-Wno-implicit-fallthrough -std=c++{0}".format(
                self.spec.variants["cxxstd"].value
            ),
            "-DCMAKE_MODULE_PATH={0}/etc/cmake".format(self.spec["root"].prefix),
            "-DPANDORA_MONITORING=ON",
            "-DPANDORA_EXAMPLE_CONTENT=OFF",
            "-DPANDORA_LC_CONTENT=OFF",
            "-DPANDORA_LAR_CONTENT=OFF",
        ]
        return args

    @run_after("install")
    def install_modules(self):
        install_tree("cmakemodules", "{0}/cmakemodules".format(self.prefix))
        for f in glob.glob("{0}/*.cmake".format(self.prefix)):
            wrongp = "{0}/spack-src/cmakemodules".format(self.stage.path)
            rightp = "{0}/cmakemodules".format(self.prefix)
            filter_file(wrongp, rightp, f, backup=False)

    def setup_dependent_build_environment(self, spack_env, dspec):
        spack_env.prepend_path("CMAKE_PREFIX_PATH", "{0}/cmakemodules".format(self.prefix))

    def setup_dependent_run_environment(self, run_env, dspec):
        run_env.prepend_path("CMAKE_PREFIX_PATH", "{0}/cmakemodules".format(self.prefix))
