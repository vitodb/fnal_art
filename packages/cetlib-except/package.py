# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import sys
import os
libdir="%s/var/spack/repos/fnal_art/lib" % os.environ["SPACK_ROOT"]
if not libdir in sys.path:
    sys.path.append(libdir)



def patcher(x):
    cetmodules_20_migrator(".","artg4tk","9.07.01")


def sanitize_environments(*args):
    for env in args:
        for var in ('PATH', 'CET_PLUGIN_PATH',
                    'LD_LIBRARY_PATH', 'DYLD_LIBRARY_PATH', 'LIBRARY_PATH',
                    'CMAKE_INSTALL_RPATH', 'CMAKE_PREFIX_PATH', 'ROOT_INCLUDE_PATH'):
            env.prune_duplicate_paths(var)
            env.deprioritize_system_paths(var)


class CetlibExcept(CMakePackage):
    """Exception libraries for the art suite."""

    homepage = 'https://art.fnal.gov/'
    git_base = 'https://cdcvs.fnal.gov/projects/cetlib_except'
    url = 'https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/cetlib_except.v1_04_00.tbz2'
    version('1.07.02', tag='v1_07_02', git=git_base, get_full_repo=True)
    version('1.04.00', tag='v1_04_00', git=git_base, get_full_repo=True)

    version('1.07.00', tag='v1_07_00', git=git_base, get_full_repo=True)
    version('MVP1a', branch='feature/Spack-MVP1a',
            git=git_base, preferred=True)
    version('MVP', branch='feature/for_spack', git=git_base, get_full_repo=True)
    version('develop', branch='develop', git=git_base, get_full_repo=True)
    #version('1.04.00', tag='v1_04_00', git=git_base, get_full_repo=True)
    version('1.04.01', tag='v1_04_01', git=git_base, get_full_repo=True)
    version('1.14.01', tag='v1_14_01', git=git_base, get_full_repo=True)



    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    depends_on('cmake@3.11:', type='build')
    depends_on('cetmodules', type='build')
    depends_on('cetpkgsupport', type=('build','run'))
    depends_on('catch2', type=('build','run'))

    if 'SPACKDEV_GENERATOR' in os.environ:
        generator = os.environ['SPACKDEV_GENERATOR']
        if generator.endswith('Ninja'):
            depends_on('ninja', type='build')

    def url_for_version(self, version):
        url = 'https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/cetlib_except.v{0}.tbz2'
        return url.format(version.underscored)

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value)]
        return args

    def setup_environment(self, spack_env, run_env):
        # For tests.
        spack_env.prepend_path('PATH', os.path.join(self.build_directory, 'bin'))
        # Cleanup.
        sanitize_environments(spack_env, run_env)

    @run_after('install')
    def rename_README(self):
        import os
        os.rename( join_path(self.spec.prefix, "README"),
                   join_path(self.spec.prefix, "README_%s"%self.spec.name))
