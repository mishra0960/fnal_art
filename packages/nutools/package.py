# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

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


class Nutools(CMakePackage):
    """Nutools"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/nutools/wiki"
    git_base = "https://github.com/NuSoftHEP/nutools.git"
    url = "https://github.com/NuSoftHEP/nutools/archive/refs/tags/v3_11_05.tar.gz"
    list_url = "https://api.github.com/repos/NuSoftHEP/nutools/tags"

    version("3.12.00", sha256="6c2e70f6550c0e26c8457ec9876dd18d3f943ad00f1a1db65a3d0ab7f7449aa6")
    version("3.11.06", sha256="994f30da77259b83c549a44b9a90ccae90a28010b164f0e53aee5ca476ebf95e")
    version("3.11.05", sha256="c58c254de91c94739a23c6de454640fe096561358205ea8ed86afc28171e3e5e")
    version(
        "develop",
        git=git_base,
        commit="53595b9a9a03bd53e3264ef761e2c5c627288459",
        get_full_repo=True,
    )
    version("mwm1", tag="mwm1", git=git_base, get_full_repo=True)
    version("MVP1a", git=git_base, branch="feature/MVP1a")

    def url_for_version(self, version):
        url = "https://github.com/NuSoftHEP/{0}/archive/v{1}.tar.gz"
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

    variant(
        "cxxstd",
        default="17",
        values=("14", "17"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    patch("cetmodules2.patch", when="@develop")
    patch("v3_11_05.patch", when="@3.11.05")
    patch("v3_11_06.patch", when="@3.11.06")

    depends_on("cetmodules", type="build")
    depends_on("art-root-io")
    depends_on("perl")
    depends_on("pythia6")
    depends_on("libwda")
    depends_on("postgresql")
    depends_on("libxml2")
    depends_on("nusimdata")
    depends_on("dk2nugenie")
    depends_on("genie")
    depends_on("geant4")
    depends_on("xerces-c")
    depends_on("cry")
    depends_on("ifdh-art")
    depends_on("ifdhc")
    depends_on("ifbeam")
    depends_on("nucondb")
    depends_on("libwda")

    def cmake_args(self):
        args = [
            "-DCMAKE_CXX_STANDARD={0}".format(self.spec.variants["cxxstd"].value),
            "-DCRYHOME={0}".format(self.spec["cry"].prefix),
            "-DGENIE_INC={0}".format(self.spec["genie"].prefix),
            "-DIGNORE_ABSOLUTE_TRANSITIVE_DEPENDENCIES=1",
        ]
        return args

    def setup_build_environment(self, spack_env):
        spack_env.set("CETBUILDTOOLS_VERSION", self.spec["cetmodules"].version)
        spack_env.set("CETBUILDTOOLS_DIR", self.spec["cetmodules"].prefix)
        # Binaries.
        spack_env.prepend_path("PATH", os.path.join(self.build_directory, "bin"))
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", os.path.join(self.build_directory, "lib"))
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(
            root=False, cover="nodes", order="post", deptype=("link"), direction="children"
        ):
            spack_env.prepend_path("ROOT_INCLUDE_PATH", str(self.spec[d.name].prefix.include))
        # Perl modules.
        spack_env.prepend_path("PERL5LIB", os.path.join(self.build_directory, "perllib"))
        # Cleaup.
        sanitize_environments(spack_env)

    def setup_run_environment(self, run_env):
        # Binaries.
        run_env.prepend_path("PATH", os.path.join(self.build_directory, "bin"))
        # Ensure we can find plugin libraries.
        run_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(
            root=False, cover="nodes", order="post", deptype=("link"), direction="children"
        ):
            run_env.prepend_path("ROOT_INCLUDE_PATH", str(self.spec[d.name].prefix.include))
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        # Perl modules.
        run_env.prepend_path("PERL5LIB", os.path.join(self.prefix, "perllib"))
        # Cleaup.
        sanitize_environments(run_env)

    def setup_dependent_build_environment(self, spack_env, dependent_spec):
        # Binaries.
        spack_env.prepend_path("PATH", self.prefix.bin)
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        # Ensure Root can find headers for autoparsing.
        spack_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        # Perl modules.
        spack_env.prepend_path("PERL5LIB", os.path.join(self.prefix, "perllib"))
        # Cleanup.
        sanitize_environments(spack_env)

    def setup_dependent_run_environment(self, run_env, dependent_spec):
        # Binaries.
        run_env.prepend_path("PATH", self.prefix.bin)
        # Ensure we can find plugin libraries.
        run_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        # Ensure Root can find headers for autoparsing.
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        # Perl modules.
        run_env.prepend_path("PERL5LIB", os.path.join(self.prefix, "perllib"))
        # Cleanup.
        sanitize_environments(run_env)
