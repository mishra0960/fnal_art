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


class Lardataalg(CMakePackage):
    """Lardataalg"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/lardataalg"
    git_base = "https://github.com/LArSoft/lardataalg.git"
    url = "https://github.com/LArSoft/lardataalg/archive/v01_02_03.tar.gz"
    list_url = "https://api.github.com/repos/LArSoft/lardataalg/tags"

    version(
        "09.30.00.rc1", sha256="2e2df94da944b1b6bf769e683bae718955ed24b42b15618d7b60254e5ad3a385"
    )
    version(
        "09.30.00.rc0", sha256="42f9c9009b64a3374d1586e5bfb0cfe159da7ef693ac689d6a41519aae069627"
    )
    version(
        "09.11.00.rc0", sha256="df723ec1db490fc37398a3e34ef800b191ef185e23b66f93a09adaadbe636179"
    )
    version("09.07.02", sha256="bf213045ddb589c2399baee2ecf4374f7953f25b1e3f9fca8443ae27f8eb5460")
    version("09.07.00", sha256="6dd6974a7f8898e8ba4f7319b9609bd14ec5ebd52b0b7e10ba63ff7fe4d7fb7a")
    version("09.06.02", sha256="4f2a53a37952af45e1d9e89739aa084364850853c969924b6a5d21f50dcdc1ce")
    version("09.06.01", sha256="eac9afd40a35e7c1866c3d26796c47ac8c839854d82dec7bbfedfb5153b941aa")
    version("09.06.00", sha256="c59fd141f1e2ca8a7a1b3ad714940f3e240d47960f3265fdf8092f59084d2caf")
    version("09.05.01", sha256="0510e0214de3ade148623da06e0b1019caee10715bac1b8596ece3a836b67909")
    version("09.05.00", sha256="130403d30bd58bc4c4063f11746cd9f52cee141ef38017e0cacbe9bbc9ea3eee")
    version(
        "09.04.07.01", sha256="4e472a604aa4d7700841b0c7ebea095fda9dfebff75429efaedbd8840c96ca8c"
    )
    version(
        "mwm1", tag="mwm1", git="https://github.com/marcmengel/lardataalg.git", get_full_repo=True
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

    patch("v09_07_00.patch", when="@09.07.00")
    patch("v09_07_02.patch", when="@09.07.02")

    variant(
        "cxxstd",
        default="17",
        values=("14", "17"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("lardataobj")
    depends_on("cetmodules", type="build")
    depends_on("messagefacility")

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
        spack_env.set("LARDATAALG_INC", self.prefix.include)
        spack_env.set("LARDATAALG_LIB", self.prefix.lib)
        spack_env.append_path("ROOT_INCLUDE_PATH", self.prefix.include)
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
