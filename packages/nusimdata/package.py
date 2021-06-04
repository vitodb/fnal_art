# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


import sys
libdir="%s/var/spack/repos/fnal_art/lib" % os.environ["SPACK_ROOT"]
if not libdir in sys.path:
    sys.path.append(libdir)


def patcher(x):
    cetmodules_20_migrator(".","nusimdata","1.21.01")

def sanitize_environments(*args):
    for env in args:
        for var in ('PATH', 'CET_PLUGIN_PATH',
                    'LD_LIBRARY_PATH', 'DYLD_LIBRARY_PATH', 'LIBRARY_PATH',
                    'CMAKE_PREFIX_PATH', 'ROOT_INCLUDE_PATH'):
            env.prune_duplicate_paths(var)
            env.deprioritize_system_paths(var)


class Nusimdata(CMakePackage):
    """Nusimdata"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/nusimdata"
    url      = "https://cdcvs.fnal.gov/projects/nusimdata"

    version('1.22.03', tag='v1_22_03', git='https://cdcvs.fnal.gov/projects/nusimdata', get_full_repo=True)

    version('MVP1a', git='https://cdcvs.fnal.gov/projects/nusimdata', branch='feature/MVP1a', preferred=True)
    version('1.19.01', tag='v1_19_01', git='https://cdcvs.fnal.gov/projects/nusimdata', get_full_repo=True)
    version('1.19.02', tag='v1_19_02', git='https://cdcvs.fnal.gov/projects/nusimdata', get_full_repo=True)
    version('1.20.00', tag='v1_20_00', git='https://cdcvs.fnal.gov/projects/nusimdata', get_full_repo=True)
    version('1.20.01', tag='v1_20_01', git='https://cdcvs.fnal.gov/projects/nusimdata', get_full_repo=True)
    version('1.21.00', tag='v1_21_00', git='https://cdcvs.fnal.gov/projects/nusimdata', get_full_repo=True)
    version('1.21.01', tag='v1_21_01', git='https://cdcvs.fnal.gov/projects/nusimdata', get_full_repo=True)
    version('1.21.02', tag='v1_21_02', git='https://cdcvs.fnal.gov/projects/nusimdata', get_full_repo=True)

    patch('nusimdata.patch',when='@1.22.03') 

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')



    # Build and link dependencies.
    depends_on('canvas-root-io')
    depends_on('dk2nudata')
    depends_on('cetmodules', type='build')

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value)               ]
        return args

    def setup_environment(self, spack_env, run_env):
        # Binaries.
        spack_env.prepend_path('PATH',
                               os.path.join(self.build_directory, 'bin'))
        # Ensure we can find plugin libraries.
        spack_env.prepend_path('CET_PLUGIN_PATH',
                               os.path.join(self.build_directory, 'lib'))
        run_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(root=False, cover='nodes', order='post',
                                    deptype=('link'), direction='children'):
            spack_env.prepend_path('ROOT_INCLUDE_PATH',
                                   str(self.spec[d.name].prefix.include))
            run_env.prepend_path('ROOT_INCLUDE_PATH',
                                 str(self.spec[d.name].prefix.include))
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        # Perl modules.
        spack_env.prepend_path('PERL5LIB',
                               os.path.join(self.build_directory, 'perllib'))
        run_env.prepend_path('PERL5LIB', os.path.join(self.prefix, 'perllib'))
        # Cleaup.
        sanitize_environments(spack_env, run_env)

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.append_path('ROOT_INCLUDE_PATH', self.prefix.include)
        # Ensure we can find plugin libraries.
        spack_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        run_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        spack_env.prepend_path('PATH', self.prefix.bin)
        run_env.prepend_path('PATH', self.prefix.bin)
        spack_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)

    # install_fhicl() is callled but there are no fcl files to install
    # however nusimdataConfig.cmake does a set and check on nusimdata_fcl_dir
    @run_after('install')
    def create_dirs(self):
        mkdirp('{0}/fcl'.format(self.spec.prefix))
