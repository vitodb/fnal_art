
# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys
from spack import *
from spack.environment import *
import os

libdir="%s/var/spack/repos/fnal_art/lib" % os.environ["SPACK_ROOT"]
if not libdir in sys.path:
    sys.path.append(libdir)


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
    git_base = 'https://cdcvs.fnal.gov/projects/hep_concurrency'

    version('MVP1a', branch='feature/Spack-MVP1a',
            git=git_base, preferred=True)
    version('MVP', branch='feature/for_spack', git=git_base)
    version('develop', branch='develop', git=git_base)
    version('1.04.00', tag='v1_04_00', git=git_base, get_full_repo=True)
    version('1.03.04', tag='v1_03_04', git=git_base, get_full_repo=True)
    version('1.04.01', sha256='ab6610a6fac64e9c2cded6732751f880b35b0ea4cb0762914b769da5653d7518')


    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    patch('hep_concurrency.1.04.01.patch', when='@1.04.01')

    # Build-only dependencies.
    depends_on('cmake@3.11:', type='build')
    depends_on('cetmodules', type='build')

    # Build / link dependencies.
    depends_on('cppunit')
    depends_on('tbb')

    if 'SPACKDEV_GENERATOR' in os.environ:
        generator = os.environ['SPACKDEV_GENERATOR']
        if generator.endswith('Ninja'):
            depends_on('ninja', type='build')

    def url_for_version(self, version):
        url = 'https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/{package}.{v}{version}.tbz2'
        return url.format(package='hep_concurrency',
                          v='v' if type(version.version[0]) == int else '',
                          version=version.underscored)

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value)]
        args.append('-DCMAKE_PROJECT_VERSION={0}'.format(self.spec.version))
        return args

    def setup_environment(self, spack_env, run_env):
        # PATH for tests.
        spack_env.prepend_path('PATH', os.path.join(self.build_directory, 'bin'))
        # Cleanup.
        sanitize_environments(spack_env, run_env)
