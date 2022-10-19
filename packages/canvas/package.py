# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


def sanitize_environments(env, *vars):
    for var in vars:
        env.prune_duplicate_paths(var)
        env.deprioritize_system_paths(var)


class Canvas(CMakePackage):
    """The underpinnings for the art suite."""

    homepage = "https://art.fnal.gov/"
    git = "https://github.com/art-framework-suite/canvas.git"
    url = "https://github.com/art-framework-suite/canvas/archive/refs/tags/v3_09_01.tar.gz"

    version("develop", branch="develop", get_full_repo=True)

    variant(
        "cxxstd",
        default="17",
        values=("17", "20", "23"),
        multi=False,
        sticky=True,
        description="C++ standard",
    )

    depends_on("boost+date_time+test")
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("cetmodules", type="build")
    depends_on("clhep")
    depends_on("cmake@3.21:", type="build")
    depends_on("fhicl-cpp")
    depends_on("hep-concurrency", type="test")
    depends_on("messagefacility")
    depends_on("range-v3@0.12:")

    if "SPACK_CMAKE_GENERATOR" in os.environ:
        generator = os.environ["SPACK_CMAKE_GENERATOR"]
        if generator.endswith("Ninja"):
            depends_on("ninja@1.10:", type="build")

    def cmake_args(self):
        return ["--preset", "default", self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]

    def setup_build_environment(self, env):
        prefix = self.build_directory
        # Binaries.
        env.prepend_path("PATH", os.path.join(prefix, "bin"))
        # Cleanup.
        sanitize_environments(env, "PATH")
