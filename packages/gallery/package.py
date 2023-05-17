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


class Gallery(CMakePackage):
    """A library to allow reading of Root output files produced by the art
    suite.
    """

    homepage = "https://art.fnal.gov/"
    git = "https://github.com/art-framework-suite/gallery.git"
    url = "https://github.com/art-framework-suite/gallery/archive/refs/tags/v1_21_01.tar.gz"

    version("develop", branch="develop", get_full_repo=True)
    version("1.21.01", sha256="e932c2469de4abb87527defe7357ea6423e8dbc18ef9d9b5148e5e658c3ffc91")
    version("1.21.02", sha256="0eb3eff1a173d09b698e1ba174ab61d9af72937067b300f1b73d0eca73349294")


    variant(
        "cxxstd",
        default="17",
        values=("17", "20", "23"),
        multi=False,
        sticky=True,
        description="C++ standard",
    )

    depends_on("canvas")
    depends_on("canvas-root-io")
    depends_on("cetlib")
    depends_on("cetmodules", type="build")
    depends_on("cmake@3.21:", type="build")
    depends_on("range-v3", type=("build", "link", "run"))
    depends_on("root+python")

    if "SPACK_CMAKE_GENERATOR" in os.environ:
        generator = os.environ["SPACK_CMAKE_GENERATOR"]
        if generator.endswith("Ninja"):
            depends_on("ninja@1.10:", type="build")

    def url_for_version(self, version):
        url = "https://github.com/art-framework-suite/gallery/archive/refs/tags/v{0}.tar.gz"
        return url.format(version.underscored)

    def cmake_args(self):
        return [
           "--preset", "default", 
           self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
        ]

    def setup_dependent_build_environment(self, env, dependent_spec):
        prefix = self.prefix
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        # Cleaup.
        sanitize_environments(env, "CET_PLUGIN_PATH")
