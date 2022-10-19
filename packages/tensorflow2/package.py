# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *
import llnl.util.tty as tty
import os
from os.path import join, dirname, basename
import io
import glob

class Tensorflow2(Package):
    """TensorFlow is an end-to-end open source platform for machine learning."""

    # override phases
    #phases = ["configure", "build", "install"]
    phases = ["build", "install"]

    homepage = "https://www.tensorflow.org/"
    url = "https://github.com/tensorflow/tensorflow/archive/refs/tags/v2.10.0.tar.gz"

    maintainers = ["marcmengel", "chissg"]

    version("2.10.0", sha256="b5a1bb04c84b6fe1538377e5a1f649bb5d5f0b2e3625a3c526ff3a8af88633e8")
    version("2.9.2", sha256="8cd7ed82b096dc349764c3369331751e870d39c86e73bbb5374e1664a59dcdf7")
    version("2.9.1", sha256="6eaf86ead73e23988fe192da1db68f4d3828bcdd0f3a9dc195935e339c95dbdc")
    version("2.8.3", sha256="4b7ecbe50b36887e1615bc2a582cb86df1250004d8bb540e18336d539803b5a7")
    version("2.8.2", sha256="b3f860c02c22a30e9787e2548ca252ab289a76b7778af6e9fa763d4aafd904c7")
    version("2.7.4", sha256="75b2e40a9623df32da16d8e97528f5e02e4a958e23b1f2ee9637be8eec5d021b")



    variant("cuda", "support CUDA gpu usage")
    depends_on('cuda', type=['build','run'], when='+cuda')
    variant("clang", "use clang for CUDA gpu usage")

    #variant("rocm", "support CUDA gpu usage")
    #depends_on('rocm', type=['build','run'], when='+rocm')

    depends_on("bazel@5.1.1", type="build", when="@2.10.0")
    depends_on("bazel@5.0.0", type="build", when="@2.9.0")
    depends_on("bazel@4.2.1", type="build", when="@2.8.0")
    depends_on("bazel@3.7.2", type="build", when="@2.5.0:2.6.0")
    depends_on("bazel@3.1.0", type="build", when="@2.3.0:2.4.0")
    depends_on("bazel@2.0.0", type="build", when="@2.2.0")
    depends_on("bazel@0.26.1", type="build", when="@2.0.0")
    depends_on('git', type=['build'])
    depends_on('py-pip', type='build')
    depends_on('py-wheel', type='build')
    depends_on('py-packaging', type='build')
    depends_on('py-pybind11', type='build')

    depends_on('curl', type=['build','run'])
    depends_on('eigen', type=['build','run'])
    depends_on('hwloc', type=['build','run'])
    depends_on('jsoncpp', type=['build','run'])
    depends_on('libjpeg-turbo', type=['build','run'])
    depends_on('llvm', type=['build','run'])
    depends_on('protobuf', type=['build','run'])
    depends_on('py-keras-preprocessing', type=['build','run'])
    depends_on('py-numpy', type=['build','run'])
    depends_on('py-opt-einsum', type=['build','run'])
    depends_on('py-requests', type=['build','run'])
    depends_on('python', type=['build','run'])


    def setup_build_environment(self, env):
        # setting lots of variables for the configure script...
        env.set('PYTHON_BIN_PATH',self.spec['python'].prefix.bin.python3)
        env.set('PYTHON_LIB_PATH',self.spec['python'].libs.directories[0])
        env.set('TF_CUDA_CLANG','1' if self.spec.satisfies('+cuda+clang') else '0')
        env.set('TF_DOWNLOAD_CLANG','0')
        env.set('TF_ENABLE_XLA','0')
        env.set('TF_NEED_ROCM','1' if self.spec.satisfies('+rocm') else '0')
        env.set('TF_NEED_CUDA','1' if self.spec.satisfies('+cuda') else '0')
        env.set('TF_NEED_TENSORRT','1' if self.spec.satisfies('+tensorrt') else '0')
        env.set('TF_ANDROID_WORKSPACE','0')

    def configure(self, spec, prefix): 
        configure = which('configure', path=["."])
        input_take_defaults = "\n\n\n\n\n\n\n\n\n\n\n\n"

        with open(".input","w") as f:
            f.write(input_take_defaults)

        with open(".input","r") as f:
            configure(input=f)

    def make_spack_external(self, bpkg, spkg):
        pkgdir = join('spack-external',spkg)
        os.makedirs(pkgdir)
        with open(join(pkgdir,'WORKSPACE'),'w') as f:
             f.write('''
new_local_repository(
    name = "%(spkg)s"
    path = "%(prefix)s"
    build_file_content = ""

''' % {'spkg':spkg, 'prefix': self.spec[spkg].prefix} 
)
             f.write('\n)\n')

        with open(join(pkgdir,'BUILD'),'w') as f:
             f.write('''
filegroup(
    name = "LICENSE.md",
    visibility = ["//visibility:public"],
)
filegroup(
    name = "COPYING",
    visibility = ["//visibility:public"],
)
''')
             try:
                 liblist = self.spec[spkg].libs.names
                 libdir = self.spec[spkg].libs.directories[0]
             except:
                 liblist = []
                 libdir = '/usr'

             for lib in liblist:
                  f.write('''
cc_library(
  name = "%(lib)s",
  linkopts = ["-L %(libdir)s -l%(lib)s"],
  hdrs = glob(["include/**/*.h"]),
  visibility = ["//visibility:public"]
)
''' % {'lib':lib, 'libdir': libdir}          
                  )

        for item in glob.glob('%s/*' % self.spec[spkg].prefix):
            symlink( item, '%s/%s'%(pkgdir, basename(item)))

        licensefilename = "%s/LICENSE.md" % pkgdir
        copyingfilename = "%s/COPYING" % pkgdir
       
        for fn in (licensefilename, copyingfilename):
            if not os.path.exists(fn):
                with open(fn,"w") as f:
                    pass

    def build(self, spec, prefix):

        # list of packages, two parts separated by colons, what the bazel config calls them,
        #    and what spack call them....
        pkglist =  [
            "curl:curl", "eigen3:eigen", "git:git", 
            "llvm:llvm", "protobuf:protobuf", "libjpeg_turbo:libjpeg-turbo",
        ]

        output_user_root = '{0}'.format(join(dirname(self.stage.source_path),'spack-build'))
        os.makedirs(output_user_root)
        bazelargs = [
            '--output_user_root={0}'.format(output_user_root),
           'build',
            '--experimental_cc_shared_library',
        ]
        if self.spec.satisfies('+cuda'):
            bazelargs.append('--config=cuda')
            pkglist.append("cuda:cuda")
            pkglist.append("nccl:nccl")
            pkglist.append("pybind11:py-pybind11")
        else:
            bazelargs.append("--config=nonccl")

        srcdir = os.path.realpath('.')
        for pkgpair in pkglist:
            (bpkg, spkg) = pkgpair.split(":")
            if spkg in self.spec:
                self.make_spack_external(bpkg, spkg)
                bazelargs.append("--override_repository={0}={1}/spack-external/{2}".format(bpkg, srcdir, spkg))
            else:
                tty.debug('tensorflow2: missing dependency on {0}?'.format(spkg))

        # bits we might need?
        #bazelargs.append("//tensorflow/cc:cc_ops")
        #bazelargs.append("//tensorflow/core:core_cpu")
        #bazelargs.append("//tensorflow/core:framework")
        #bazelargs.append("//tensorflow/core:framework_internal")
        #bazelargs.append("//tensorflow/core:lib")

        # build c++ libraries and python pip package
        bazelargs.append("//tensorflow/core:protos_all_cc")
        bazelargs.append('//tensorflow:libtensorflow_cc.so')
        bazelargs.append('//tensorflow/tools/pip_package:build_pip_package')
 
        
        bazel(*bazelargs)

        build_pip_package = which('build_pip_package',path='tensorflow/tools/pip_package')
        build_pip_package()

    def install(self, spec, prefix):

        bash = which('bash')
        includedir = "{0}/include".format(prefix)
        libdir = "{0}/lib".format(prefix)
        bash( "-c", "cd bazel-bin && find tensorflow -name '*.h' -print | grep -v internal | cpio -dump {0}".format(includedir))
        bash( "-c", "cd bazel-bin/tensorflow && find . -name '*.so*' -print |  cpio -dump {0}".format(libdir))
