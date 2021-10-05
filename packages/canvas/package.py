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
                    'CMAKE_PREFIX_PATH', 'ROOT_INCLUDE_PATH'):
            env.prune_duplicate_paths(var)
            env.deprioritize_system_paths(var)


class Canvas(CMakePackage):
    """The underpinnings for the art suite."""

    homepage = 'https://art.fnal.gov/'
    git_base = 'https://cdcvs.fnal.gov/projects/canvas'
    url = 'https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/canvas.v3_05_01.tbz2'
    version('3.12.02', tag='v3_12_02', git=git_base, get_full_repo=True)

    version('3.09.00', tag='v3_09_00', git=git_base, get_full_repo=True)
    version('MVP1a', branch='feature/Spack-MVP1a',
            git=git_base, preferred=True)
    version('MVP', branch='feature/for_spack', git=git_base)
    version('develop', branch='develop', git=git_base,get_full_repo=True)
    version('3.12.00', tag='v3_12_00', git=git_base, get_full_repo=True)
    version('3.10.00', tag='v3_10_00', git=git_base, get_full_repo=True)
    version('3.05.00', tag='v3_05_00', git=git_base, get_full_repo=True)
    version('3.05.01', tag='v3_05_01', git=git_base, get_full_repo=True)
    version('3.07.03', tag='v3_07_03', git=git_base, get_full_repo=True)
    version('3.07.04', tag='v3_07_04', git=git_base, get_full_repo=True)
    version('3.08.00', tag='v3_08_00', git=git_base, get_full_repo=True)
    version('3.05.00', tag='v3_05_00', git=git_base, get_full_repo=True)
    version('3.05.01', tag='v3_05_01', git=git_base, get_full_repo=True)
    version('3.07.03', tag='v3_07_03', git=git_base, get_full_repo=True)
    version('3.07.04', tag='v3_07_04', git=git_base, get_full_repo=True)
    version('3.08.00', tag='v3_08_00', git=git_base, get_full_repo=True)

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')



    # Build-only dependencies.
    depends_on('cmake@3.11:', type='build')
    depends_on('cetmodules', type='build')

    depends_on('clhep')
    depends_on('boost')
    depends_on('cetlib')
    depends_on('cetlib-except')
    depends_on('cppunit')
    depends_on('fhicl-cpp')
    depends_on('hep-concurrency', when='@MVP1a')
    depends_on('messagefacility')
    depends_on('range-v3')
    depends_on('tbb', when='@MVP')

    patch('canvas_new.patch')

    if 'SPACKDEV_GENERATOR' in os.environ:
        generator = os.environ['SPACKDEV_GENERATOR']
        if generator.endswith('Ninja'):
            depends_on('ninja', type='build')

    def url_for_version(self, version):
        #url = 'https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/{0}.v{1}.tbz2'
        url = 'https://github.com/art-framework-suite/{0}/archive/refs/tags/v{1}.tar.gz'
        return url.format(self.name, version.underscored)

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value)]
        return args

    def setup_environment(self, spack_env, run_env):
        # Binaries.
        spack_env.prepend_path('PATH', os.path.join(self.build_directory, 'bin'))
        # Cleanup.
        sanitize_environments(spack_env, run_env)

    @run_after('install')
    def rename_README(self):
        import os
        if os.path.exists(join_path(self.spec.prefix, "README")):
            os.rename( join_path(self.spec.prefix, "README"),
                       join_path(self.spec.prefix, "README_%s"%self.spec.name))
