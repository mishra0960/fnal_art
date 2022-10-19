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


class ArtRootIo(CMakePackage):
    """Root-based input/output for the art suite."""

    homepage = "https://art.fnal.gov/"
    git = "https://github.com/art-framework-suite/art-root-io.git"
    url = "https://github.com/art-framework-suite/art-root-io/archive/refs/tags/v3_09_01.tar.gz"

    version("develop", branch="develop", get_full_repo=True)

    variant(
        "cxxstd",
        default="17",
        values=("17", "20", "23"),
        multi=False,
        sticky=True,
        description="C++ standard",
    )

    depends_on("art")
    depends_on("boost+filesystem+date_time+program_options")
    depends_on("canvas")
    depends_on("canvas-root-io")
    depends_on("catch2", type=("build", "test"))
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("cetmodules@3.19.02:", type="build")
    depends_on("cmake@3.21:", type="build")
    depends_on("fhicl-cpp")
    depends_on("hep-concurrency")
    depends_on("messagefacility")
    depends_on("root+python")
    depends_on("sqlite@3.8.2:")

    if "SPACK_CMAKE_GENERATOR" in os.environ:
        generator = os.environ["SPACK_CMAKE_GENERATOR"]
        if generator.endswith("Ninja"):
            depends_on("ninja@1.10:", type="build")

    def cmake_args(self):
        return [
            "--trace-expand",
            "--preset",
            "default",
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
        ]

    def setup_build_environment(self, env):
        prefix = self.build_directory
        # Binaries.
        env.prepend_path("PATH", os.path.join(prefix, "bin"))
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", os.path.join(prefix, "lib"))
        # Cleanup.
        sanitize_environments(env, "PATH", "CET_PLUGIN_PATH")

    def setup_run_environment(self, env):
        prefix = self.prefix
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        # Cleanup.
        sanitize_environments(env, "CET_PLUGIN_PATH")

    def setup_dependent_build_environment(self, env, dependent_spec):
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        # Cleanup.
        sanitize_environments(env, "CET_PLUGIN_PATH")

    def setup_dependent_run_environment(self, env, dependent_spec):
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        # Cleanup.
        sanitize_environments(env, "CET_PLUGIN_PATH")
