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


class Larpandoracontent(CMakePackage):
    """Larpandoracontent"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larpandoracontent/wiki"
    url = "https://github.com/LArSoft/larpandoracontent/archive/refs/tags/v03_26_01.tar.gz"
    list_url = "https://api.github.com/repos/LArSoft/larpandoracontent/tags"

    version(
        "03.26.01.01", sha256="f7c38678f3b7631df1287ca63ee3479d62c33b6d82134e9b98b7e6de90c4ce5c"
    )
    version("03.26.01", sha256="fdd00d2b3954fe2388ed5e754ffe2f82bea6f627bf037e6d6b799555b0afef96")
    version(
        "mwm1",
        tag="mwm1",
        git="https://github.com/marcmengel/larpandoracontent.git",
        get_full_repo=True,
    )
    version(
        "03.22.11.01",
        tag="v03_22_11_01",
        git="https://github.com/LArSoft/larpandoracontent.git",
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

    # patch('v03_26_01.patch', when='@03.26.01')
    patch("v03_26_01_01.patch", when="@03.26.01.01")

    variant(
        "cxxstd",
        default="17",
        values=("14", "17"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("cetmodules", type="build")
    depends_on("eigen")
    depends_on("pandora")
    depends_on("py-torch")

    def cmake_args(self):
        args = [
            "-DCMAKE_CXX_STANDARD={0}".format(self.spec.variants["cxxstd"].value),
            "-DCMAKE_MODULE_PATH={0}/cmakemodules".format(self.spec["pandora"].prefix),
            "-DPANDORA_MONITORING=ON",
            "-DLAR_CONTENT_LIBRARY_NAME=LArPandoraContent",
            "-DPandoraSDK_DIR={0}/cmakemodules".format(self.spec["pandora"].prefix),
            "-DPandoraMonitoring_DIR={0}/cmakemodules".format(self.spec["pandora"].prefix),
            "-DCMAKE_PREFIX_PATH={0}/lib/python{1}/site-packages/torch".format(
                self.spec["py-torch"].prefix, self.spec["python"].version.up_to(2)
            ),
        ]
        return args

    def setup_build_environment(self, env):
        env.set("CETBUILDTOOLS_VERSION", "cetmodules")
