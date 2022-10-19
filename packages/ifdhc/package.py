# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import llnl.util.tty as tty

from spack import *


class Ifdhc(MakefilePackage):
    """Data handling client code for intensity frontier experiments"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/ifdhc"
    git_base = "https://cdcvs.fnal.gov/projects/ifdhc/ifdhc.git"

    version("develop", git=git_base, branch="develop", get_full_repo=True)
    version("2.5.16", sha256="5455f58042c7b84826fc72e77d21e9f0a5ec7efe5f40435571c52fb4c0e226fd")
    version("2.3.10", sha256="4da290f5fc3c9d4344792176e19e1d3278f87a634ebc1535bbd9a91aae2bbf9b")
    version("2.3.9", sha256="1acdff224f32c3eb5780aed13cf0f23b431623a0ebc8a74210271b75b9f2f574")
    version("2.5.2", git=git_base, tag="v2_5_2", get_full_repo=True)
    # version('2.5.4', git=git_base, tag='v2_5_4', get_full_repo=True)
    version("2.5.4", sha256="48bf6807cb8b3092677768f763c1f18940d852d685424a1ea386acf7f1606608")
    version("2.5.12", sha256="e8a8af62e5e9917e51c88b2cda889c2a195dfb7911e09c28aeaf10f54e8abf49")
    version("2.5.14", sha256="66ab9126bb3cb1f8d8dafb69568569d8856ab6770322efc7c5064252f27a8fda")

    depends_on("python")
    depends_on("swig", type="build", when="@:2.5.0")
    depends_on("zlib")
    depends_on("uuid")

    variant(
        "cxxstd",
        default="17",
        values=("default", "98", "11", "14", "17"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    patch("version.patch", level=1, when="@:2.4.5")

    parallel = False

    def patch(self):
        for hfile in (os.path.join("ifdh", "ifdh.h"), os.path.join("numsg", "numsg.h")):
            filter_file(r'^(\s*#\s*include\s+["<])../util/', r"\1", hfile)
        filter_file(r"(CFLAGS=.*) -Werror", r"\1", "util/Makefile")

    def url_for_version(self, version):
        url = "https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/{0}.v{1}.tbz2"

        return url.format(self.name, version.underscored)

    @property
    def build_targets(self):
        uuidflags = " -L %s -I %s " % (
            self.spec["uuid"].prefix.lib,
            self.spec["uuid"].prefix.include,
        )
        cxxstd = self.spec.variants["cxxstd"].value
        cxxstdflag = (
            "" if cxxstd == "default" else getattr(self.compiler, "cxx{0}_flag".format(cxxstd))
        )
        return ("SHELL=/bin/bash", "ARCH=-g -O3 -DNDEBUG %s %s" % (cxxstdflag, uuidflags), "all")

    @property
    def install_targets(self):
        return ("SHELL=/bin/bash", "DESTDIR={0}/".format(self.prefix), "install")

    @run_after("install")
    def install_cfg(self):
        cmd = "cp {0}/ifdh.cfg {1}/ifdh.cfg".format(self.stage.source_path, self.spec.prefix)
        tty.warn("installing ifdh.cfg: {0}".format(cmd))
        os.system(cmd)

    def setup_build_environment(self, spack_env):
        spack_env.set("PYTHON_INCLUDE", self.spec["python"].prefix.include)
        spack_env.set("PYTHON_LIB", self.spec["python"].prefix.lib)
        spack_env.set("IFDHC_DIR", self.spec.prefix)

    def setup_run_environment(self, run_env):
        run_env.prepend_path("PATH", self.spec.prefix.bin)
        run_env.set("IFDHC_DIR", self.spec.prefix)

    def setup_dependent_build_environment(self, spack_env, dspec):
        spack_env.prepend_path("PATH", self.spec.prefix.bin)
        # Non-standard, therefore we have to do it ourselves.
        spack_env.prepend_path("ROOT_INCLUDE_PATH", self.spec.prefix.inc)
        spack_env.set("IFDHC_DIR", self.spec.prefix)
        spack_env.set("IFDHC_INC", self.spec.prefix.inc)

    def setup_dependent_run_environment(self, run_env, dspec):
        run_env.prepend_path("PATH", self.prefix.bin)
        # Non-standard, therefore we have to do it ourselves.
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.spec.prefix.inc)
        run_env.set("IFDHC_DIR", self.spec.prefix)
