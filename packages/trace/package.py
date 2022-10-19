# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
import sys

from spack import *

libdir = "%s/var/spack/repos/fnal_art/lib" % os.environ["SPACK_ROOT"]
if libdir not in sys.path:
    sys.path.append(libdir)


def patcher(x):
    cetmodules_20_migrator(".", "artg4tk", "9.07.01")


class Trace(CMakePackage):
    """TRACE is yet another logging (time stamp) tool, but it allows
    fast and/or slow logging - dynamically (you choose)."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/trace/wiki"
    git_base = "https://cdcvs.fnal.gov/projects/trace-git/"

    parallel = False

    depends_on("cetmodules", type="build")
    depends_on("cetpkgsupport", type="build")

    patch("trace-3.15.05.patch", when="@3.15.05")
    patch("trace-3.16.00.patch", when="@3.16.00")
    patch("trace-3.15.07.patch", when="@3.15.07")

    version("3.17.01", sha256="396c56edceba545db4ab2a40080b56236a816ab39ce06fd057ca2794dc276e66")

    def url_for_version(self, version):
        url = "https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/{0}.v{1}.tbz2"
        return url.format(self.name + "-git", version.underscored)

    def cmake_args(self):
        args = [
            "-Dproduct=trace",
            "-Dtrace_include_dir={0}".format(self.spec.prefix.include),
        ]
        return args

    @run_after("install")
    def rename_README(self):
        import os

        if os.path.exists(join_path(self.spec.prefix, "README")):
            os.rename(
                join_path(self.spec.prefix, "README"),
                join_path(self.spec.prefix, "README_%s" % self.spec.name),
            )

    def setup_dependent_build_environment(self, spack_env, dspec):
        spack_env.set("TRACE_INC", self.spec.prefix.include)
