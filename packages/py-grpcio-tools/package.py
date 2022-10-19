# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyGrpcioTools(PythonPackage):
    """HTTP/2-based RPC framework."""

    homepage = "https://grpc.io/"
    url = "https://pypi.io/packages/source/g/grpcio-tools/grpcio-tools-1.35.0.tar.gz"
    version("1.35.0", sha256="9e2a41cba9c5a20ae299d0fdd377fe231434fa04cbfbfb3807293c6ec10b03cf")

    depends_on("python@3.5:", when="@1.30:", type=("build", "run"))
    depends_on("python@2.7:2.8,3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-grpcio", type=("build", "run"))

    def setup_build_environment(self, env):
        pass

    def patch(self):
        pass
