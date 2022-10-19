# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack import *


class H5cpp(Package):
    """Hierarchical Data Format C++ templates for Serial and Paralell HDF5"""

    homepage = "https://h5cpp.org/"
    url = "https://github.com/steven-varga/h5cpp/archive/refs/tags/v1.10.4-6.tar.gz"

    version("1.10.4.6", sha256="4fbc8e777dc78a37ec2fe8c7b6a47114080ffe587f083e83a2046b5e794aef93")
    version("1.10.4.5", sha256="661ccc4d76e081afc73df71ef11d027837d92dd1089185f3650afcaec9d418ec")

    def url_for_version(self, version):
        return "https://github.com/steven-varga/h5cpp/archive/refs/tags/v{0}.tar.gz".format(
            re.sub(r"\.([0-9])$", r"-\1", str(version))
        )

    def install(self, spec, prefix):
        install_tree(self.stage.source_path + "/h5cpp", prefix + "/include/h5cpp")
