# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from llnl.util import tty
import sys
import os
import re
import spack.util.spack_json as sjson


class Cetmodules(CMakePackage):
    """CMake glue modules and scripts required by packages originating at
    Fermilab and associated experiments and other collaborations.
    """

    homepage = 'https://cdcvs.fnal.gov/redmine/projects/cetmodules'
    git_base = 'https://github.com/FNALssi/cetmodules.git'
    url = 'https://github.com/FNALssi/cetmodules/archive/refs/tags/2.29.04.tar.gz'
    list_url = 'https://api.github.com/repos/FNALssi/cetmodules/tags'

    version('develop', branch='develop', git=git_base, get_full_repo=True)
    #version('3.00.00', sha256='11c87f5433ce2077172ba2708e0dbfda094024eff1df2ec21da1025a01577188')
    #version('2.30.01', sha256='f547dbb48e552c769644507ab15a2e44f4feb41bd2ac838dc69e170816ce0db8')
    #version('2.30.00', sha256='2c1e695b6a2695f1cea165dadf010b5006db7f478a2eb62903ed8bce9bbd3e43')
    version('2.29.14', sha256='2c919adc474d7ea815033d21fe9e12cf3af541906ff93f746110d76b02e234f9')
    version('2.29.13', sha256='2b494cf58da9b39aa643258bbdfd3b0d93dfd822870300275b7d3c0c95401b86')
    version('2.29.12', sha256='f3002bcd6c99ce0175c9aef85e14269ec9770d907753f2a96cfa6b5c821b6b2a')
    version('2.29.11', sha256='bf465542d976efb258a8ae17b14de9af7dfc2ecbfd944141bb53009df84ee6fc')
    version('2.29.10', sha256='043e2f8470c796d49f05bba3cf95bc163797f38137f843170e5c788054a0f1d9')
    version('2.29.11', sha256='bf465542d976efb258a8ae17b14de9af7dfc2ecbfd944141bb53009df84ee6fc')
    version('2.29.10', sha256='043e2f8470c796d49f05bba3cf95bc163797f38137f843170e5c788054a0f1d9')
    version('2.29.09', sha256='cd31bbd303cec9d8e1207c2da11b9eef96a78fe8d14258b367f1e3a1898b6e0f')
    version('2.29.08', sha256='7a59d8c5c91ee59f2b56dd73dcef9f3957e47ebd247e0a9baf5da8ddcd124218')
    version('2.29.07', sha256='372a0f2c46df49c9d86633dbc11bf69213d9749945f160a1f8b50a7badf81e99')
    version('2.29.06', sha256='8eefc5f18b2c094c4d784c0c025cde88c09a9b3bf2cca5e28b256a079ad20fa3')
    version('2.29.05', sha256='35e70edd7126b66c22982fd442df61d0d7439c72760642ac920c6e76a87c8767')
    version('2.29.04', sha256='3042ae45814f9c196d085abed8e6f0dbc1d2c0e8c61c1e457de1b9711b32b715')
    version('2.29.03', sha256='e40485a6cc7170a51669656901a956896d237f778f26f7f3e62671d092c7bfd5')
    version('2.29.02', sha256='519a7c685122c0cab8b699773785f15b3e05292fb566db950478b6506bfbb065')
    version('2.29.00', sha256='74af89f2540b1e116207dc278ab77df19cfac959dfbf64055ba975563979d1c1')
    version('2.28.03', sha256='ae1a451862eab9fdc992e5c918b626c26a431af90f25b66cbc535492c96529a0')
    version('2.28.02', sha256='8abcdd4ea6b4c3a3325cd2c080e00adccb402531ed336351db2b592ef830b442')
    version('2.28.01', sha256='8afafa7d995c29d694775afeecb5c2ffb513d3e266cba8ca01ec0eae82173de2')
    version('2.16.02', sha256='43082380b23b3367303368b6ec698d7a3624b19a8a99842752bd13bcb474625e')
    version('2.14.00', sha256='360b719133d644d47f092f42895f3037891cfb30adf6897472f62f037a3129f1')
    version('2.09.00', sha256='8c4d9a5f3d39a7dff5e9136576dab1bcf50a410c6cc028e5b47a2546c57e3860')
    version('1.04.00', sha256='4ba077e7146e19a805476f2fcf2a537a2cd24dbd602f5f5c348431b5018379da')
    version('1.03.00', sha256='40b0f8fa88f9522d14cae87a4242a494aa724b13505b6b740a0007153cc85e18')
    version('1.02.04', sha256='4e5063748aa8821b34a2a3ae150927afcd890beade83ad98e03f93e5d93d8ee7')
    version('1.02.03', sha256='04cf68a443e7701985e9e72fcc26e5fdfa46304b01c9295a4f0b526eeafa1b63')
    version('1.02.02', sha256='b7bd22219afe34942d29287df4d864eb1a6114eed0ebf2c5d3912884d6c2594a')
    version('1.02.01', sha256='6357771a5dd56dc25f0211d491d30cea6fe48114a18ef82e17f848a04d0cbc88')
    version('1.02.00', sha256='1a72b77730efd5efff56218f950917c3c3b6b4f157d4b16c1d1bb4e40cbd760f')
    version('1.01.03', sha256='6f9168e7f638aa6e7b7798fac384a38f825518e7599e24daeaf0551b6dc3f0fd')
    version('1.01.02', sha256='dddc8992f011fec77d152990dc89ac1027b280bb31c3e5ac093b2945847d74c7')
    version('1.01.01', sha256='0b7e28d4c29c9941a6960609e8ab4aa33f90736ef1dc81fc7b1b520e99ee0ae7')
    version('1.01.00', sha256='80bf9a77852751f90b1446e5d5966bea9b73d5b35e024195b35c851dc93a5443')
    version('1.00.00', sha256='67438bb1ee9acdaadb6e245ff670463c4603c3283c69b3c9d1a04d6ee9a3fd16')

    depends_on('cmake@3.11:', type='build', when='@:1.01.99')
    depends_on('cmake@3.12:', type='build', when='@1.02.00:')
    depends_on('cmake@3.18:', type='build', when='@2.07.00:')
    depends_on('py-sphinxcontrib-moderncmakedomain', when='@2.00.10:', type='build')
    depends_on('py-sphinxcontrib-moderncmakedomain', when='@develop',type='build')
    depends_on('py-sphinx-rtd-theme', when='@2.00.10:',type='build')
    depends_on('py-sphinx-rtd-theme', when='@develop',type='build')
    depends_on('git@2.35:')
    depends_on('py-sphinx', type='build',when='@2.00.10:')
    depends_on('py-sphinx-design', type='build',when='@2.00.10:')
    depends_on('py-sphinx', type='build',when='@develop')
    depends_on('py-sphinx-design', type='build',when='@develop')

    @run_before('cmake')
    def fix_fix_man(self):
        filter_file('exit \$status', 'exit 0', '%s/libexec/fix-man-dirs' % self.stage.source_path)

    def url_for_version(self, version):
        url = 'https://github.com/FNALssi/{0}/archive/refs/tags/{1}.tar.gz'
        return url.format(self.name, version)

    def fetch_remote_versions(self, concurrency=None):
        return dict(map(lambda v: (v.dotted, self.url_for_version(v)),
                        [ Version(d['name']) for d in
                          sjson.load(
                              spack.util.web.read_from_url(
                                  self.list_url,
                                  accept_content_type='application/json')[2])
                          if re.match(r'^[0-9]',d['name']) ]))

    def setup_run_environment(self, run_env):
        run_env.prepend_path('CMAKE_PREFIX_PATH', '{0}/Modules'.format(self.prefix))

    @run_after('install')
    def rename_README(self):
        import os
        if os.path.exists(join_path(self.spec.prefix, "README")):
            os.rename( join_path(self.spec.prefix, "README"),
                       join_path(self.spec.prefix, "README_%s"%self.spec.name))
