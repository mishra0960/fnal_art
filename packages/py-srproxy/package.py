# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class PySrproxy(Package):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://github.com/cafana/SRProxy/"
    url      = "https://github.com/cafana/SRProxy/archive/v00.16.tar.gz"

    version('00.31', sha256='6a4b191add1ae1637b75f95da4dd56db8139c8dcf4504897d3f20e4d6d98d528')
    version('00.16', sha256='98507bf7adfe7b7ddfbfb043ef40c5c3eed55b3818be0c62766b759f06fc0b59')
    version('00.15', sha256='90bed72a1a2924132171d108799698602a28a4143ca2234d0ee988d80bd60d83')
    version('00.14', sha256='fc8c12331e2dcaaa0d5063dd86ae8b65f1221d1505ddb14a4490e6f23019d510')

    depends_on('castxml')
    depends_on('py-pygccxml')

    def install(self, spec, prefix):
        mkdirp(self.prefix.bin)
        mkdirp(self.prefix.include)
        copy(join_path(self.stage.source_path, 'gen_srproxy'), self.prefix.bin)
        copy(join_path(self.stage.source_path, '*.h'), self.prefix.include)
        copy(join_path(self.stage.source_path, '*.cxx'), self.prefix.include)
