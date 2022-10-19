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


class Nuevdb(CMakePackage):
    """Nuevdb"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/nuevdb/wiki"
    git_base = "https://github.com/NuSoftHEP/nuevdb.git"
    url = "https://github.com/NuSoftHEP/nuevdb/archive/refs/tags/v1_05_05.tar.gz"
    list_url = "https://api.github.com/repos/NuSoftHEP/nuevdb/tags"

    version("1.06.00", sha256="5a9dc5dd235ed4a16f26ebf09070d806f132bb22c6750a019c6ca7a3797d5d51")
    version("1.05.06", sha256="76050a5dea93202b39ce81e09a4b66411ad845340bef935fe50d6d54e1a90126")
    version("1.05.05", sha256="e5bbd1c523f8befcb63b4a6a529e6eed592519ddefd31a2504ffd25e312e1115")
    version("mwm1", tag="mwm1", git=git_base, get_full_repo=True)
    version("develop", branch="develop", git=git_base, get_full_repo=True)

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
    patch("v1_05_05.patch", when="@1.05.05")
    patch("v1_05_06.patch", when="@1.05.06")

    depends_on("cetmodules", type="build")
    depends_on("art-root-io")
    depends_on("perl")
    depends_on("pythia6")
    depends_on("libwda")
    depends_on("postgresql")
    depends_on("libxml2")
    depends_on("nusimdata")
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
            "-DIGNORE_ABSOLUTE_TRANSITIVE_DEPENDENCIES=1",
        ]
        return args

    def setup_build_environment(self, spack_env):
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

    def setup_dependent_build_environment(self, spack_env, dspec):
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        spack_env.prepend_path("PATH", self.prefix.bin)
        spack_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        spack_env.append_path("FHICL_FILE_PATH", "{0}/job".format(self.prefix))
        spack_env.append_path("FW_SEARCH_PATH", "{0}/gdml".format(self.prefix))
        sanitize_environments(spack_env)

    def setup_dependent_run_environment(self, run_env, dspec):
        # Ensure we can find plugin libraries.
        run_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        run_env.prepend_path("PATH", self.prefix.bin)
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        run_env.append_path("FHICL_FILE_PATH", "{0}/job".format(self.prefix))
        run_env.append_path("FW_SEARCH_PATH", "{0}/gdml".format(self.prefix))
        sanitize_environments(run_env)
