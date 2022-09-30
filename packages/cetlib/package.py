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


class Cetlib(CMakePackage):
    """A utility library for the art suite."""

    homepage = 'https://art.fnal.gov/'
    git_base = 'https://github.com/art-framework-suite/cetlib.git'
    url = 'https://github.com/art-framework-suite/cetlib/archive/refs/tags/v3_09_01.tar.gz'
    list_url = 'https://api.github.com/repos/art-framework-suite/cetlib/tags'

    version('3.13.04', sha256='40ca829cfb172f6cbf516bd3427fc7b7e893f9c916d969800261194610c45edf')
    version('3.13.03', sha256='708624fab8f7a5460e4cc5b1e82ed9e0a6c1706ad7a58be81c518eebc6696cf0')
    version('3.13.02', sha256='6fe88cb504be82e1c2e86f424976189833c1dc11f7187bf95335b892ae1a31d5')
    version('3.13.01', sha256='5c223456aa75b2a4b6894757607bb626a2db7bed466476345d53674a9ac26cb8')
    version('3.13.00', sha256='706cab15229ad77d885c3027b1425255aaf9a3d0e55e21c1c364f5e5261d731f')
    version('3.12.00', sha256='651bc5c616034ea3e5378931cdcb41ec5ffbcf4cf66367ff85d1fa1f69adb045')
    version('3.11.01', sha256='1dd2d270fb69f74592db4879d897673fc722eb18e0ba9931096d0113560e6c18')
    version('3.11.00', sha256='e75975bbb9256c9820588d413b76f4c7fb0e5bece84db0e90aec4888faaa8ad2')
    version('3.10.01', sha256='7dc10c6b2cbe6713fdbe4888e4e24d6a898163a9292cc0daecc03b00a169ce5c')
    version('3.10.00', sha256='8edeaba3a15b548c1330bc199a3c4ed21f971e763429ab9886ee87b2d8cf66ec')
    version('MVP1a', branch='archive/feature/Spack-MVP1a', git=git_base, get_full_repo=True)
    version('MVP', branch='archive/feature/for_spack', git=git_base, get_full_repo=True)
    version('develop', branch='develop', git=git_base, get_full_repo=True)
   
    #patch('cetlib-notests.patch', when='@develop')

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

    # Build-only dependencies.
    depends_on('cmake@3.11:', type='build')
    depends_on('cetmodules', type='build')
    depends_on('catch2@2.3.0:', type=('build', 'link'))
    depends_on('tbb', type=('build', 'link'))

    # Build / link dependencies.
    depends_on('boost')
    depends_on('sqlite@3.8.2:')
    depends_on('cetlib-except')
    depends_on('hep-concurrency', when='@3.0.5:')
    depends_on('openssl')
    depends_on('sqlite')
    depends_on('perl')  # Module skeletons, etc.

    if 'SPACKDEV_GENERATOR' in os.environ:
        generator = os.environ['SPACKDEV_GENERATOR']
        if generator.endswith('Ninja'):
            depends_on('ninja', type='build')

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value),
		'-DIGNORE_ABSOLUTE_TRANSITIVE_DEPENDENCIES=1'
	]
        return args

    def setup_build_environment(self, spack_env):
        # Binaries.
        spack_env.prepend_path('PATH', os.path.join(self.build_directory, 'bin'))
        # For plugin tests (not needed for installed package).
        spack_env.prepend_path('CET_PLUGIN_PATH',
                               os.path.join(self.build_directory, 'lib'))
        # Perl modules.
        spack_env.prepend_path('PERL5LIB',
                               os.path.join(self.build_directory, 'perllib'))
        spack_env.set('CETLIB_DIR', self.prefix)
        # Cleanup.
        sanitize_environments(spack_env)

    def setup_run_environment(self, run_env):
        # Perl modules.
        run_env.prepend_path('PERL5LIB', os.path.join(self.prefix, 'perllib'))
        run_env.set('CETLIB_DIR', self.prefix)
        # Cleanup.
        sanitize_environments(run_env)

    def setup_dependent_build_environment(self, spack_env, dependent_spec):
        # Binaries.
        spack_env.prepend_path('PATH', self.prefix.bin)
        # Perl modules.
        spack_env.prepend_path('PERL5LIB', os.path.join(self.prefix, 'perllib'))
        spack_env.set('CETLIB_DIR', self.prefix)

    def setup_dependent_run_unvironment(self, run_env, dependent_spec):
        # Binaries.
        run_env.prepend_path('PATH', self.prefix.bin)
        # Perl modules.
        run_env.prepend_path('PERL5LIB', os.path.join(self.prefix, 'perllib'))
        run_env.set('CETLIB_DIR', self.prefix)

    @run_after('install')
    def rename_README(self):
        import os
        if os.path.exists(join_path(self.spec.prefix, "README")):
            os.rename( join_path(self.spec.prefix, "README"),
                       join_path(self.spec.prefix, "README_%s"%self.spec.name))
