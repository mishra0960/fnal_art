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


class Larcoreobj(CMakePackage):
    """Larcoreobj"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larcoreobj"
    git_base = "https://github.com/LArSoft/larcoreobj.git"
    url = "https://github.com/LArSoft/larcoreobj/archive/v01_02_03.tar.gz"
    list_url = "https://api.github.com/repos/LArSoft/larcoreobj/tags"

    version(
        "09.30.00.rc1", sha256="01c6095d4123270b5c72cb49edb87d276d6d4955bcbc45b2af209058a2556e44"
    )
    version(
        "09.30.00.rc0", sha256="136e7bcaf395103a437dea51d3fa60201ea0c95c919df271e7e82f698cd2e134"
    )
    version(
        "09.11.00.rc0", sha256="a472f20d85ebcb73125f857fd51669da28f298b9ddf538da0f7a476a7995b920"
    )
    version("09.03.01", sha256="ba687dc47bf9972f2760ccbfd4d7406f8c54a860cfd9f1459025d58c0901f8a2")
    version("09.03.00", sha256="00142588189c3371b7103a90247dfaf9e8cc5057311d48aeb3eef8d1e8b5f883")
    version(
        "09.02.01.04", sha256="348ad515af2972f8d1120bb737419faa6a1dfdbde7c2f0360ef3209a2e1dc076"
    )
    version(
        "09.02.01.03", sha256="4105948a6f66ae4f67c17dca26c45625070c55afc2e944df9fac0d65f96361b8"
    )
    version(
        "09.02.01.02", sha256="79f5d03a06653b36ece1d742297eee11ecb4f228e4e7e92dffbe58a4906cdad7"
    )
    version(
        "09.02.01.01", sha256="69ac99252ff2c522510c60ebe27ad644a9634e03d9b9ecdd25f5b78361be579f"
    )
    version(
        "mwm1",
        git="https://github.com/marcmengel/larcoreobj.git",
        branch="develop",
        get_full_repo=True,
    )
    version(
        "09.24.01.01",
        tag="v09_24_01_01",
        git="https://github.com/marcmengel/larcoreobj.git",
        get_full_repo=True,
    )

    def url_for_version(self, version):
        url = "https://github.com/LArSoft/{0}/archive/v{1}.tar.gz"
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
                    if d["name"].startswith("v") and not d["name"].endswith(")")
                ],
            )
        )

    patch("v09_03_01.patch", when="@09.03.01")

    variant(
        "cxxstd",
        default="17",
        values=("14", "17"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("canvas-root-io")
    depends_on("cetmodules", type="build")

    def cmake_args(self):
        args = ["-DCMAKE_CXX_STANDARD={0}".format(self.spec.variants["cxxstd"].value)]
        return args

    def setup_build_environment(self, spack_env):
        spack_env.set("CETBUILDTOOLS_VERSION", self.spec["cetmodules"].version)
        spack_env.set("CETBUILDTOOLS_DIR", self.spec["cetmodules"].prefix)
        spack_env.prepend_path("LD_LIBRARY_PATH", self.spec["root"].prefix.lib)
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
        # Set path to find fhicl files
        spack_env.prepend_path("FHICL_INCLUDE_PATH", os.path.join(self.build_directory, "job"))
        # Set path to find gdml files
        spack_env.prepend_path("FW_SEARCH_PATH", os.path.join(self.build_directory, "job"))
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
        # Set path to find fhicl files
        run_env.prepend_path("FHICL_INCLUDE_PATH", os.path.join(self.prefix, "job"))
        # Set path to find gdml files
        run_env.prepend_path("FW_SEARCH_PATH", os.path.join(self.prefix, "job"))
        # Cleaup.
        sanitize_environments(run_env)

    def setup_dependent_build_environment(self, spack_env, dspec):
        spack_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        spack_env.prepend_path("PATH", self.prefix.bin)
        spack_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        spack_env.append_path("FHICL_FILE_PATH", "{0}/job".format(self.prefix))
        spack_env.append_path("FW_SEARCH_PATH", "{0}/gdml".format(self.prefix))

    def setup_dependent_run_environment(self, run_env, dspec):
        run_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        run_env.prepend_path("PATH", self.prefix.bin)
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        run_env.append_path("FHICL_FILE_PATH", "{0}/job".format(self.prefix))
        run_env.append_path("FW_SEARCH_PATH", "{0}/gdml".format(self.prefix))

    def flag_handler(self, name, flags):
        if name == "cxxflags" and self.spec.compiler.name == "gcc":
            flags.append("-Wno-error=deprecated-declarations")
        return (flags, None, None)
