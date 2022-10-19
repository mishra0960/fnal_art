# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install google-benchmark
#
# You can edit this file again by typing:
#
#     spack edit google-benchmark
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class GoogleBenchmark(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://github.com/google/benchmark/"
    url = "https://github.com/google/benchmark/archive/v1.5.0.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version("1.5.2", sha256="dccbdab796baa1043f04982147e67bb6e118fe610da2c65f88912d73987e700c")
    version("1.5.1", sha256="23082937d1663a53b90cb5b61df4bcc312f6dee7018da78ba00dd6bd669dfef2")

    depends_on("googletest")

    def cmake_args(self):
        # FIXME: Add arguments other than
        # FIXME: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
        # FIXME: If not needed delete this function
        args = [CMakePackage.define("BENCHMARK_ENABLE_TESTING", "OFF")]
        return args
