# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Libpqxx(CMakePackage):
    """libpqxx, the C++ API to the PostgreSQL database management system."""

    homepage = "http://pqxx.org/development/libpqxx/"
    url = "https://github.com/jtv/libpqxx/archive/refs/tags/7.6.0.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['marcmengel']

    version("7.6.0", sha256="8194ce4eff3fee5325963ccc28d3542cfaa54ba1400833d0df6948de3573c118")
    version("7.5.2", sha256="62e140667fb1bc9b61fa01cbf46f8ff73236eba6f3f7fbcf98108ce6bbc18dcd")
    version("7.5.1", sha256="16a3a4097a6772a9824ba584dbe5a1feee163ab954b94497358fe591eb236e3d")

    depends_on("postgresql")

    def cmake_args(self):
        args = [
            "DPostgreSQL_TYPE_INCLUDE_DIR=%s" % self.spec["postgresql"].prefix.include,
            "DPostgreSQL_INCLUDE_DIR=%s" % self.spec["postgresql"].prefix.include,
            "DPostgreSQL_LIBRAY_DIR=%s" % self.spec["postgresql"].prefix.lib,
        ]
        return args
