# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import llnl.util.tty as tty

from spack.package import *
from spack.util.environment import NameValueModifier


class PrependEnv(NameValueModifier):
    def execute(self, env):
        tty.debug("PrependEnv: {0}+{1}".format(self.name, str(self.value)), level=3)
        prepend_env_value = env.get(self.value, None)
        if prepend_env_value:
            environment_value = env.get(self.name, None)
            directories = (
                prepend_env_value.split(self.separator) + environment_value.split(self.separator)
                if environment_value
                else []
            )
            env[self.name] = self.separator.join(directories)


def sanitize_environments(env, *vars):
    for var in vars:
        env.prune_duplicate_paths(var)
        env.deprioritize_system_paths(var)


class Critic(CMakePackage):
    """Compatibility tests for the art and gallery applications of the art
    suite.
    """

    homepage = "https://art.fnal.gov/"
    git = "https://github.com/art-framework-suite/critic.git"
    url = "https://github.com/art-framework-suite/critic/archive/refs/tags/v3_09_01.tar.gz"

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
    depends_on("art-root-io")
    depends_on("canvas")
    depends_on("cetlib")
    depends_on("cetmodules", type="build")
    depends_on("clhep@2.4.1.0:")
    depends_on("cmake@3.21:", type="build")
    depends_on("fhicl-cpp")
    depends_on("gallery")
    depends_on("hep-concurrency")
    depends_on("messagefacility")
    depends_on("root+python")

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
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", os.path.join(prefix, "lib"))
        # ... and in the interpreter.
        env.env_modifications.append(PrependEnv("LD_LIBRARY_PATH", "CET_PLUGIN_PATH"))
        # Cleanup.
        sanitize_environments(env, "PATH", "CET_PLUGIN_PATH", "LD_LIBRARY_PATH")
