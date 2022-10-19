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


class Nurandom(CMakePackage):
    """Random number generator interfaces to art."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/nurandom"
    git_base = "https://github.com/NuSoftHEP/nurandom.git"
    url = "https://github.com/NuSoftHEP/nurandom/archive/refs/tags/v1_07_06.tar.gz"
    list_url = "https://api.github.com/repos/NuSoftHEP/nurandom/tags"

    version("1.08.00", sha256="f7ffa502bf2088ac1a9b974e6c57b8cc6d0ba07730174ea0f45b89810bc04411")
    version("1.07.06", sha256="85a6b595bd1b6b2873ebc726e0d4031570dc12897632cdb7d2a8fb5c16954cb5")
    version("mwm1", tag="mwm1", git=git_base, get_full_repo=True)
    version(
        "develop",
        commit="feb2c214ffec9dd2e9a1b3c7e02f2315f3ec9666",
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

    # Build-only dependencies.
    depends_on("cetmodules", type="build")
    depends_on("cetbuildtools", type="build")
    depends_on("art")
    depends_on("art-root-io")
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("clhep")

    patch("cetmodules2.patch", when="@develop")
    patch("v1_07_06.patch", when="@1.07.06")

    def cmake_args(self):
        # Set CMake args.
        args = ["-DCMAKE_CXX_STANDARD={0}".format(self.spec.variants["cxxstd"].value)]
        return args

    def setup_build_environment(self, spack_env):
        # Binaries.
        spack_env.prepend_path("PATH", os.path.join(self.build_directory, "bin"))
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", os.path.join(self.build_directory, "lib"))
        spack_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
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
