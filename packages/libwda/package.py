# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class Libwda(MakefilePackage):
    """Fermilab Web Data Access library"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/libwda"
    git_base = "https://cdcvs.fnal.gov/projects/ifdhc-libwda"
    url = "https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/libwda.v2_22_2.tbz2"

    version("2.29.1", tag="v2_29_1", git=git_base, get_full_repo=True)
    version("develop", git=git_base, branch="develop", get_full_repo=True)
    version("2.26.0", sha256="4df374bbf36030241a9714d5e08cd9b2b5e1b3374da1a97ec793cd37eba40fc2")
    version("2.22.2", tag="v2_22_2", git=git_base, get_full_repo=True)
    version("2.23.0", tag="v2_23_0", git=git_base, get_full_repo=True)
    version("2.24.0", tag="v2_24_0", git=git_base, get_full_repo=True)
    version("2.26.0", tag="v2_26_0", git=git_base, get_full_repo=True)

    parallel = False

    build_directory = "src"

    depends_on("curl")
    depends_on("zlib")
    depends_on("openssl")
    depends_on("pcre")

    patch("version.patch", level=1)

    @property
    def build_targets(self):
        tlist = [
            "LIBWDA_VERSION=v{0}".format(self.version.underscored),
        ]
        return tlist

    @property
    def install_targets(self):
        return ("PREFIX={0}".format(prefix), "install")

    def url_for_version(self, version):
        url = "https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/{0}.v{1}.tbz2"
        return url.format("-".join(("ifdhc", self.name)), version.underscored)

    @run_before("build")
    def filter_makefile(self):
        makefile = FileFilter(os.path.join("src", "Makefile"))
        makefile.filter("gcc", "$(CC)")

    def setup_build_environment(self, spack_env):
        spack_env.set("LIBWDA_DIR", self.prefix)

    def setup_run_environment(self, run_env):
        run_env.set("LIBWDA_DIR", self.prefix)

    def setup_dependent_build_environment(self, spack_env, dspec):
        spack_env.set("LIBWDA_DIR", self.prefix)

    def setup_dependent_run_environment(self, run_env, dspec):
        run_env.set("LIBWDA_DIR", self.prefix)
