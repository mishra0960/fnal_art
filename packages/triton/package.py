# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

from spack import *


# decorator to try a method twice...
def tryagain(f):
    def double_f(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except Exception:
            f(*args, **kwargs)

    return double_f


class Triton(CMakePackage):
    """C++ client code for Triton Inference Server."""

    homepage = "https://github.com/triton-inference-server/server"
    url = "https://github.com/triton-inference-server/server/archive/v2.6.0.tar.gz"

    maintainers = ["marcmengel", "github_user2"]

    version("2.3.0", sha256="3e46d09f0d3dd79513e10112170a81ed072db0719b75b95943d824b1afd149c4")
    version("2.6.0", sha256="c4fad25c212a0b5522c7d65c78b2f25ab0916ccf584ec0295643fec863cb403e")
    version("2.7.0", sha256="7ad24acb3c7138ff5667137e143de3f7345f03df61f060004214495faa7fa16e")

    variant("cuda", default=False)
    variant(
        "cxxstd",
        default="17",
        values=("14", "17"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("cmake@3.18:", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-wheel", type="build")
    depends_on("py-grpcio", type=("build", "run"))
    depends_on("py-grpcio-tools", type=("build", "run"))
    depends_on("py-numpy")
    depends_on("py-geventhttpclient")
    depends_on("py-python-rapidjson")
    depends_on("rapidjson")
    depends_on("protobuf")
    depends_on("googletest")
    depends_on("google-cloud-cpp")
    depends_on("crc32c")
    depends_on("c-ares")
    depends_on("libb64")
    depends_on("libevent")
    depends_on("libevhtp")
    depends_on("c-ares")
    depends_on("abseil-cpp")
    depends_on("grpc")
    depends_on("prometheus-cpp")
    depends_on("curl@7.56:")
    depends_on("opencv ~videoio~gtk~java~vtk~jpeg", when="~cuda")
    depends_on("opencv ~videoio~gtk~java~vtk~jpeg+cuda+cudalegacy+cudaobjdetect", when="+cuda")
    depends_on("cuda", when="+cuda")
    depends_on("nccl", when="+cuda")

    patch("cms.patch", when="@2.3.0")
    patch("proto.patch", when="@2.3.0")

    # trying doubled build...
    build = tryagain(CMakePackage.build)

    @run_before("cmake")
    def patch_version(self):
        filter_file(
            r"^project.*",
            "PROJECT({0} VERSION {1} LANGUAGES CXX C)".format("client", self.version),
            "build/client/CMakeLists.txt",
        )
        filter_file(
            r'data_files \+= \[\("bin", \["perf_analyzer", "perf_client"\]\)\]',
            "data_files = data_files",
            "src/clients/python/library/setup.py",
        )
        filter_file(
            r".*\.\./\.\./\.\./(protobuf|grpc)/.*", "", "src/clients/c++/library/CMakeLists.txt"
        )

    def cmake_args(self):
        args = [
            "-DCMAKE_BUILD_TYPE=RelWithDebInfo",
            "-DCMAKE_C_COMPILER=cc",
            "-DCMAKE_CXX_COMPILER=c++",
            "-DTRITON_CURL_WITHOUT_CONFIG:BOOL=ON",
            "-DTRITON_CLIENT_SKIP_EXAMPLES:BOOL=ON",
            "-DTRITON_ENABLE_HTTP:BOOL=OFF",
            "-DTRITON_ENABLE_GRPC:BOOL=ON",
            "-DTRITON_VERSION={0}".format(self.spec.version),
            "-DCMAKE_CXX_STANDARD={0}".format(self.spec.variants["cxxstd"].value),
            "-DTRITON_COMMON_REPO_TAG:STRING=main",
            "-DTRITON_CORE_REPO_TAG:STRING=main",
        ]

        if "+cuda" in self.spec:
            args.append("-DTRITON_ENABLE_GPU:BOOL=ON")
            args.append("-DTRITON_ENABLE_METRICS_GPU:BOOL=ON")
        else:
            args.append("-DTRITON_ENABLE_GPU:BOOL=OFF")
            args.append("-DTRITON_ENABLE_METRICS_GPU:BOOL=OFF")

        return args

    #
    # we want our cmake/modules directory in the CMAKE_PREFIX_PATH
    # but its built in _std_args(), and we want all that plus ours...
    #
    @property
    def std_cmake_args(self):
        std_cmake_args = CMakePackage._std_args(self)
        fixed = []
        for arg in std_cmake_args:
            if arg.startswith("-DCMAKE_PREFIX_PATH:STRING="):
                fixed.append(arg + ";" + self.stage.source_path + "/cmake/modules")
            else:
                fixed.append(arg)
        return fixed

    #
    # also push our cmake/modules on the environment CMAKE_PREFIX_PATH for
    # ExternalPackage calls...
    #
    def setup_build_environment(self, env):
        env.prepend_path("CMAKE_PREFIX_PATH", self.stage.source_path + "/cmake/modules")
        pass

    root_cmakelists_dir = "build/client"

    def flag_handler(self, name, flags):
        if name == "cxxflags" and self.spec.compiler.name == "gcc":
            flags.append("-Wno-error=deprecated-declarations")
            flags.append("-Wno-error=class-memaccess")
        return (flags, None, None)

    #    @tryagain
    #    def build(self, spec, prefix):
    #        with working_dir(self.build_directory):
    #            make('cshm','all')

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            make("install")

    @run_before("install")
    def install_model_headers(self):
        mkdirp(self.prefix.include)
        for f in glob.glob(join_path(self.build_directory, "src/core/*.pb.h")):
            copy(f, join_path(self.prefix.include, os.path.basename(f)))
