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


class Larwirecell(CMakePackage):
    """Larwirecell"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larwirecell"
    git_base = "https://github.com/LArSoft/larwirecell.git"
    url = "https://github.com/LArSoft/larwirecell/archive/v01_02_03.tar.gz"
    list_url = "https://api.github.com/repos/LArSoft/larwirecell/tags"

    version(
        "09.30.00.rc1", sha256="2d2fdffbda8cb5a16f35b68bc422b6fbebe70af6ac601762f257e4fef0cbf30d"
    )
    version("09.04.05", sha256="e270deb99f0c2baf96c137d12ed61281ce005f0dfb60fd0d4ee05caf5afcadf3")
    version("09.04.03", sha256="84c7be7e6cf70f57fc53da3fcae7712cac3c748bb21be1ca9a21e9dc976b3021")
    version("09.04.02", sha256="9d53b89017a2f26f804ecffcc8fbe16f26301d2d7d2d3190d464968ff8a56297")
    version("09.04.01", sha256="d3786882f1715403b8635c9e506254fc59d7b9629df00af135411cfb4dc56236")
    version("09.04.00", sha256="e2cd7a63b8db90ac16308bf0fe018945a06993394898316ab25cf62968649746")
    version("09.03.01", sha256="d4aa46289fefe0e9c96bfda9d228ebd009b3718d6231a0a745495ba86dbfa1bb")
    version("09.03.00", sha256="2a0c6bd82d16c17a15bc976edd7972a94125c3c25d018b5c24e63b9b8e079bd0")
    version(
        "09.02.13.01", sha256="0db9cfba036367c1ac1648f865f2ce75535a2d5cbeca5341aa7d81c96077ca4f"
    )
    version("09.02.13", sha256="3bb40ffaedaceb9ebaff9ff90c71aed022455564fccc1156cb51df15a1890fa9")
    version("09.02.12", sha256="8c0ebd57bf5d99b74c67d4e4ae22369a52319ed54087c3292a8e419b1d93c873")
    version(
        "mwm1", tag="mwm1", git="https://github.com/marcmengel/larwirecell.git", get_full_repo=True
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

    variant(
        "cxxstd",
        default="17",
        values=("14", "17"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    patch("v09_04_03.patch", when="@09.04.03")
    patch("v09_04_05.patch", when="@09.04.05")

    depends_on("larevt")
    depends_on("wirecell")
    depends_on("cetmodules", type="build")

    def cmake_args(self):
        args = [
            "-DCMAKE_CXX_STANDARD={0}".format(self.spec.variants["cxxstd"].value),
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
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        spack_env.prepend_path("PATH", self.prefix.bin)
        spack_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        spack_env.append_path("FHICL_FILE_PATH", "{0}/job".format(self.prefix))
        spack_env.append_path("FW_SEARCH_PATH", "{0}/gdml".format(self.prefix))

    def setup_dependent_run_environment(self, run_env, dspec):
        # Ensure we can find plugin libraries.
        run_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        run_env.prepend_path("PATH", self.prefix.bin)
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        run_env.append_path("FHICL_FILE_PATH", "{0}/job".format(self.prefix))
        run_env.append_path("FW_SEARCH_PATH", "{0}/gdml".format(self.prefix))
