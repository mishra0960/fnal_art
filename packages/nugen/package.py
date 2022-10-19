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


class Nugen(CMakePackage):
    """Generator interfaces to art for GENIE and GiBUU."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/nugen"
    git_base = "https://github.com/NuSoftHEP/nugen.git"
    url = "https://github.com/NuSoftHEP/nugen/archive/refs/tags/v1_14_05.tar.gz"
    list_url = "https://api.github.com/repos/NuSoftHEP/nugen/tags"

    version("1.15.00", sha256="098c9128b4d938e5a781c0b3535f7bc5f09e33c3b8280f2bc9927634fcdfc2c7")
    version("1.14.06", sha256="99642b9b3f05cf8cc886222303d43d4a4442583ce7a5c7a872871aacdc45df53")
    version("1.14.05", sha256="e2cb16b5855e54a442cdfba42a40ca87e4d17d8156cbb2678205e0e5565a7b6c")
    version("mwm1", tag="mwm1", git="https://cdcvs.fnal.gov/projects/nugen", get_full_repo=True)
    version(
        "develop",
        commit="dca7eaa2257476033b074e71b78b2f6b23b647be",
        git=git_base,
        get_full_repo=True,
    )

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
    patch("v1_14_06.patch", when="@1.14.06")
    patch("v1_14_05.patch", when="@1.14.05")

    # Build-only dependencies.
    depends_on("cmake@3.12:", type="build")
    depends_on("cetmodules", type="build")
    depends_on("catch2@2.3.0:", type="build")

    # Build and link dependencies.
    depends_on("clhep")
    depends_on("boost")
    depends_on("canvas")
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("fhicl-cpp")
    depends_on("hep-concurrency")
    depends_on("messagefacility")
    depends_on("tbb")
    depends_on("root+python")
    depends_on("perl")
    depends_on("art-root-io")
    depends_on("perl")
    depends_on("pythia6")
    depends_on("libwda")
    depends_on("postgresql")
    depends_on("libxml2")
    depends_on("nusimdata")
    depends_on("dk2nudata")
    depends_on("dk2nugenie")
    depends_on("genie")
    depends_on("xerces-c")
    depends_on("cry")
    depends_on("ifdh-art")
    depends_on("ifdhc")
    depends_on("ifbeam")
    depends_on("nucondb")
    depends_on("libwda")
    depends_on("log4cpp")

    if "SPACKDEV_GENERATOR" in os.environ:
        generator = os.environ["SPACKDEV_GENERATOR"]
        if generator.endswith("Ninja"):
            depends_on("ninja", type="build")

    def cmake_args(self):
        # Set CMake args.
        args = [
            "-DCMAKE_CXX_STANDARD={0}".format(self.spec.variants["cxxstd"].value),
            "IGNORE_ABSOLUTE_TRANSITIVE_DEPENDENCIES=1",
            "-DGENIE_INC={0}".format(self.spec["genie"].prefix.include),
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
