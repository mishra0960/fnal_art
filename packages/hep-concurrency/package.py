
# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
from llnl.util import tty
import sys
import os
import spack.util.spack_json as sjson


def sanitize_environments(*args):
    for env in args:
        for var in ('PATH', 'CET_PLUGIN_PATH',
                    'LD_LIBRARY_PATH', 'DYLD_LIBRARY_PATH', 'LIBRARY_PATH',
                    'CMAKE_INSTALL_RPATH', 'CMAKE_PREFIX_PATH', 'ROOT_INCLUDE_PATH'):
            env.prune_duplicate_paths(var)
            env.deprioritize_system_paths(var)


class HepConcurrency(CMakePackage):
    """A concurrency library for the art suite."""

    homepage = 'https://art.fnal.gov/'
    git_base = 'https://github.com/art-framework-suite/hep-concurrency.git'
    url = 'https://github.com/art-framework-suite/hep-concurrency/archive/refs/tags/v1_07_04.tar.gz'
    list_url = 'https://api.github.com/repos/art-framework-suite/hep-concurrency/tags'

    version('1.07.04', sha256='442db7ea3c0057e86165a001ef77c1fc0e5ed65c62fd1dd53e68fb8fe9a5fef3')
    version('1.07.03', sha256='6e4009766ae3e50257c4aa64ce9ca530c52d2541fefaa34a9b4f4c2414a628dd')
    version('1.07.02', sha256='87cecb5e73ae42e442b90ed41399148fedb94ef4e36a35eca81e2c6e3476b03f')
    version('1.07.01', sha256='7f8f5e7ddee2eacd33e1222107696b1c85e173c729947f935fdec00b61411c59')
    version('1.07.00', sha256='1c397d024bb91e0c0b740a93526abc375c9303dc353407f5ca8837a4391bdc02')
    version('1.06.00', sha256='1841739ce8baafef5f7510da91aeb0c0547defc039af0402d66a5ac67d88a2b7')
    version('1.05.00', sha256='5e0ec05be98938be53f668891e3c0569d16ccdaff529aa3ebcb2d3a31f9e1f01')
    version('1.04.01', sha256='2150d8b732164ef3e5e9d9202d9816a90df4f050056d9490300eb1ede122b275')
    version('1.04.00', sha256='0b724ed9f185cd01b90912474ead369d08105e82c798e9632ea8bfedc10068ce')
    version('1.03.04', sha256='49426f2b061ff7349c33c7b5532faa55a1df057bac016403ecd95490d7d55b7f')
    version('MVP1a', branch='archive/feature/Spack-MVP1a',git=git_base, get_full_repo=True)
    version('MVP', branch='archive/feature/for_spack',git=git_base, get_full_repo=True)
    version('develop', branch='develop', git=git_base, get_full_repo=True)

    def url_for_version(self, version):
        url = 'https://github.com/art-framework-suite/{0}/archive/v{1}.tar.gz'
        return url.format(self.name, version.underscored)

    def fetch_remote_versions(self, concurrency=None):
        return dict(map(lambda v: (v.dotted, self.url_for_version(v)),
                        [ Version(d['name'][1:]) for d in
                          sjson.load(
                              spack.util.web.read_from_url(
                                  self.list_url,
                                  accept_content_type='application/json')[2])
                          if d['name'].startswith('v') ]))

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    patch('hep_concurrency.1.04.01.patch', when='@1.04.01')
    patch('hep_concurrency.1.07.04.patch', when='@1.07.04')

    # Build-only dependencies.
    depends_on('cmake@3.11:', type='build')
    depends_on('cetmodules', type='build')
    depends_on('cetlib-except', type=('build','run'))

    # Build / link dependencies.
    depends_on('cppunit')
    depends_on('catch2')
    depends_on('tbb')

    if 'SPACKDEV_GENERATOR' in os.environ:
        generator = os.environ['SPACKDEV_GENERATOR']
        if generator.endswith('Ninja'):
            depends_on('ninja', type='build')

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value)]
        args.append('-DCMAKE_PROJECT_VERSION={0}'.format(self.spec.version))
        return args

    def setup_build_environment(self, spack_env):
        # PATH for tests.
        spack_env.prepend_path('PATH', os.path.join(self.build_directory, 'bin'))
        # Cleanup.
        sanitize_environments(spack_env)
