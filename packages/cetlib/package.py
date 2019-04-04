# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.environment import *
import os


def sanitize_environments(*args):
    for env in args:
        for var in ('PATH', 'CET_PLUGIN_PATH',
                    'LD_LIBRARY_PATH', 'DYLD_LIBRARY_PATH', 'LIBRARY_PATH',
                    'CMAKE_INSTALL_RPATH', 'CMAKE_PREFIX_PATH', 'ROOT_INCLUDE_PATH'):
            env.prune_duplicate_paths(var)
            env.deprioritize_system_paths(var)


class Cetlib(CMakePackage):
    """A utility library for the art suite."""

    homepage = 'http://art.fnal.gov/'
    git_base = 'ssh://p-larsoft@cdcvs.fnal.gov/cvs/projects/cetlib'

    version('MVP', branch='feature/for_spack',
            git=git_base, preferred=True)
    version('MVP1a', branch='feature/Spack-MVP1a',
            git=git_base, preferred=True)

    #patch('cetlib-catch2.patch', when='@MVP1a')

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    # Build-only dependencies.
    depends_on('cmake@3.4:', type='build', when='@MVP')
    depends_on('cmake@3.11:', type='build', when='@MVP1a')
    depends_on('cetmodules', type='build')
    #depends_on('catch@2.3.0:~single_header', type='build')
    depends_on('catch@2.3.0:~single_header')

    # Build / link dependencies.
    depends_on('boost')
    depends_on('sqlite@3.8.2:')
    depends_on('cetlib-except')
    depends_on('hep-concurrency', when='@MVP1a')
    depends_on('openssl')
    depends_on('sqlite')
    depends_on('perl')  # Module skeletons, etc.

    if 'SPACKDEV_GENERATOR' in os.environ:
        generator = os.environ['SPACKDEV_GENERATOR']
        if generator.endswith('Ninja'):
            depends_on('ninja', type='build')

    def url_for_version(self, version):
        url = 'https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/{0}.v{1}.tbz2'
        return url.format(self.name, version.underscored)

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value)]
        return args

    def setup_environment(self, spack_env, run_env):
        # Binaries.
        spack_env.prepend_path('PATH', join_path(self.build_directory, 'bin'))
        # For plugin tests (not needed for installed package).
        spack_env.prepend_path('CET_PLUGIN_PATH',
                               join_path(self.build_directory, 'lib'))
        # Perl modules.
        spack_env.prepend_path('PERL5LIB',
                               join_path(self.build_directory, 'perllib'))
        run_env.prepend_path('PERL5LIB', join_path(self.prefix, 'perllib'))
        # Cleanup.
        sanitize_environments(spack_env, run_env)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        # Binaries.
        spack_env.prepend_path('PATH', self.prefix.bin)
        run_env.prepend_path('PATH', self.prefix.bin)
        # Perl modules.
        spack_env.prepend_path('PERL5LIB', join_path(self.prefix, 'perllib'))
        run_env.prepend_path('PERL5LIB', join_path(self.prefix, 'perllib'))
