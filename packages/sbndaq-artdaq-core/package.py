# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.util.spack_json as sjson
from spack import *


class SbndaqArtdaqCore(CMakePackage):
    """The toolkit currently provides SBNDAQ extensions to the artdaq-core
    functionality for data transfer, event building, event reconstruction."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/sbndaq/wiki"
    url = "https://github.com/SBNSoftware/sbndaq-artdaq-core/archive/v1_00_00of0.tar.gz"
    git_base = "https://github.com/SBNSoftware/sbndaq-artdaq-core.git"
    list_url = "https://api.github.com/repos/SBNSoftware/sbndaq-artdaq-core/tags"

    version(
        "develop",
        git=git_base,
        commit="e80441a707b42befe641002440421b4d2ea572d4",
        get_full_repo=True,
    )
    version("v1_00_00of0", git=git_base, tag="v1_00_00of0", get_full_repo=True)
    version("v1_00_00of2", git=git_base, tag="v1_00_00of2", get_full_repo=True)

    variant(
        "cxxstd",
        default="17",
        values=("14", "17"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    def url_for_version(self, version):
        url = "https://github.com/SBNSoftware/{0}/archive/v{1}.tar.gz"
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
    patch("v1_00_00of0.patch", when="@v1_00_00of0")
    patch("v1_00_00of2.patch", when="@v1_00_00of2")

    depends_on("messagefacility")
    depends_on("cetmodules", type="build")
    depends_on("artdaq-core")
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("boost")
    depends_on("trace")

    def setup_run_environment(self, spack_env):
        spack_env.set("MRB_QUALS", "both")

    def cmake_args(self):
        args = [
            "-DCMAKE_CXX_STANDARD={0}".format(self.spec.variants["cxxstd"].value),
            "-DCANVAS_VERSION=v3_06_00",
            "-DMESSAGEFACILITY_VERSION=v2_02_05",
            "-DBoost_SYSTEM_LIBRARY=-lboost_system-mt",
            "-DBoost_DATE_TIME_LIBRARY=-lboost_date_time",
            "-DBoost_FILESYSTEM_LIBRARY=-lboost_filesystem",
            "-DBoost_THREAD_LIBRARY=-lboost_thread",
        ]
        return args
