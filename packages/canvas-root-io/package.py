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


class CanvasRootIo(CMakePackage):
    """A Root I/O library for the art suite."""

    homepage = "https://art.fnal.gov/"
    git = "https://github.com/art-framework-suite/canvas-root-io.git"
    url = "https://github.com/art-framework-suite/canvas-root-io/archive/refs/tags/v3_09_01.tar.gz"

    version("develop", branch="develop", get_full_repo=True)
    version("1.11.01", sha256="7f8d6a465bce3b874abbac7d1f08f587db32e0035a2200402fbde2b5cef762d7")


    variant(
        "cxxstd",
        default="17",
        values=("17", "20", "23"),
        multi=False,
        sticky=True,
        description="C++ standard",
    )

    depends_on("boost+thread")
    depends_on("canvas")
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("cetmodules@3.19.02:", type="build")
    depends_on("clhep")
    depends_on("cmake@3.21:", type="build")
    depends_on("fhicl-cpp")
    depends_on("hep-concurrency")
    depends_on("messagefacility")
    depends_on("root@6.26:+python")

    def url_for_version(self,version):
        urlfmt = "https://github.com/art-framework-suite/canvas-root-io/archive/refs/tags/v{0}.tar.gz"
        return urlfmt.format(version.underscored)

    if "SPACK_CMAKE_GENERATOR" in os.environ:
        generator = os.environ["SPACK_CMAKE_GENERATOR"]
        if generator.endswith("Ninja"):
            depends_on("ninja@1.10:", type="build")

    def cmake_args(self):
        return [
           "--preset", "default", 
           "-DCMAKE_CXX_COMPILER={0}".format(self.compiler.cxx_names[0]),
           "-DCMAKE_C_COMPILER={0}".format(self.compiler.cc_names[0]),
           "-DCMAKE_Fortran_COMPILER={0}".format(self.compiler.f77_names[0]),
           self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
        ]

    def setup_build_environment(self, env):
        prefix = self.build_directory
        # Binaries.
        env.prepend_path("PATH", os.path.join(prefix, "bin"))
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", os.path.join(prefix, "lib"))
        # Set LD_LIBRARY_PATH so CheckClassVersion.py can find cppyy lib
        env.prepend_path("LD_LIBRARY_PATH", join_path(self.spec["root"].prefix.lib))
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(
            root=False, cover="nodes", order="post", deptype=("link"), direction="children"
        ):
            env.prepend_path("ROOT_INCLUDE_PATH", str(self.spec[d.name].prefix.include))
        # Cleanup.
        sanitize_environments(
            env, "PATH", "CET_PLUGIN_PATH", "LD_LIBRARY_PATH", "ROOT_INCLUDE_PATH"
        )
        # just setting with cmake doesn't seem to get through to the dictionary compiles(?)
        env.set("CXXFLAGS", "-std=c++{0}".format(self.spec.variants["cxxstd"].value))

    def setup_run_environment(self, env):
        prefix = self.prefix
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(
            root=False, cover="nodes", order="post", deptype=("link"), direction="children"
        ):
            env.prepend_path("ROOT_INCLUDE_PATH", str(self.spec[d.name].prefix.include))
        env.prepend_path("ROOT_INCLUDE_PATH", prefix.include)
        # Cleanup.
        sanitize_environments(env, "CET_PLUGIN_PATH", "ROOT_INCLUDE_PATH")

    def setup_dependent_build_environment(self, env, dependent_spec):
        prefix = self.prefix
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        # Set LD_LIBRARY_PATH so CheckClassVersion.py can find cppyy lib
        env.prepend_path("LD_LIBRARY_PATH", join_path(self.spec["root"].prefix.lib))
        # Ensure Root can find headers for autoparsing.
        for d in dependent_spec.traverse(
            root=False, cover="nodes", order="post", deptype=("link"), direction="children"
        ):
            env.prepend_path("ROOT_INCLUDE_PATH", str(dependent_spec[d.name].prefix.include))
        # Cleanup.
        sanitize_environments(env, "CET_PLUGIN_PATH", "LD_LIBRARY_PATH", "ROOT_INCLUDE_PATH")

    def setup_dependent_run_environment(self, env, dependent_spec):
        prefix = self.prefix
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        # Set LD_LIBRARY_PATH so CheckClassVersion.py can find cppyy lib
        env.prepend_path("LD_LIBRARY_PATH", join_path(self.spec["root"].prefix.lib))
        # Ensure Root can find headers for autoparsing.
        for d in dependent_spec.traverse(
            root=False, cover="nodes", order="post", deptype=("link"), direction="children"
        ):
            env.prepend_path("ROOT_INCLUDE_PATH", str(dependent_spec[d.name].prefix.include))
        # Cleanup.
        sanitize_environments(env, "CET_PLUGIN_PATH", "LD_LIBRARY_PATH", "ROOT_INCLUDE_PATH")
