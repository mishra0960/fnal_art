# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.util.spack_json as sjson
from spack import *


def sanitize_environments(*args):
    for env in args:
        for var in (
            "PATH",
            "CET_PLUGIN_PATH",
            "LD_LIBRARY_PATH",
            "DYLD_LIBRARY_PATH",
            "LIBRARY_PATH",
            "CMAKE_PREFIX_PATH",
            "ROOT_INCLUDE_PATH",
        ):
            env.prune_duplicate_paths(var)
            env.deprioritize_system_paths(var)


class IfdhArt(CMakePackage):
    """The ifdh_art package provides ART service access to the libraries
    from the ifdhc package."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/ifdh-art/wiki"
    git_base = "https://github.com/art-framework-suite/ifdh-art.git"
    url = "https://github.com/art-framework-suite/ifdh-art/archive/refs/tags/v2_12_05.tar.gz"
    list_url = "https://api.github.com/repos/art-framework-suite/ifdh-art/tags"

    version("2.13.00", sha256="d9b59c4181051d6b86ee346c562faaac7d4c5c0eeef37f159e2b1757859d4516")
    version("2.12.05", sha256="f783e6e06d6d26f58b44c68d76d6b404bfe80a57918f4d7490090495f3ef35d1")
    version("2.12.04", sha256="10999a6cbf1f55f51dcba91c9631a2dc06d04ffc6230bfe3b3421f84ccb207b1")
    version("develop", git=git_base, branch="develop", get_full_rep=True)
    version(
        "MVP1a",
        git="https://github.com/art-framework-suite/ifdh-art.git",
        branch="feature/Spack-MVP1a",
    )

    def url_for_version(self, version):
        url = "https://github.com/art-framework-suite/{0}/archive/v{1}.tar.gz"
        return url.format(self.name, version.underscored)

    def fetch_remote_versions(self, concurrency=None):
        return dict(
            map(
                lambda v: (v.dotted, self.url_for_version(v)),
                [
                    Version(d["name"][1:])
                    for d in sjson.load(
                        spack.util.web.read_from_url(
                            self.list_url, accept_content_type="application/json"
                        )[2]
                    )
                    if d["name"].startswith("v")
                ],
            )
        )

    patch("cetmodules2.patch", when="@develop")
    patch("v2_12_05.patch", when="@2.12.05")

    variant(
        "cxxstd",
        default="17",
        values=("14", "17"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("art")
    depends_on("ifdhc")
    depends_on("ifbeam")
    depends_on("nucondb")
    depends_on("libwda")
    depends_on("cetmodules", type="build")

    def cmake_args(self):
        args = ["-DCMAKE_CXX_STANDARD={0}".format(self.spec.variants["cxxstd"].value)]
        return args

    def setup_dependent_build_environment(self, spack_env, dspec):
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        spack_env.prepend_path("PATH", self.prefix.bin)

    def setup_dependent_run_environment(self, run_env, dspec):
        # Ensure we can find plugin libraries.
        run_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        run_env.prepend_path("PATH", self.prefix.bin)

    @run_after("install")
    def rename_README(self):
        import os

        if os.path.exists(join_path(self.spec.prefix, "README")):
            os.rename(
                join_path(self.spec.prefix, "README"),
                join_path(self.spec.prefix, "README_%s" % self.spec.name),
            )
