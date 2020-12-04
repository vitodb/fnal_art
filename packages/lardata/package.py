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
from cetmodules_patcher import cetmodules_20_migrator


def patcher(x):
    cetmodules_20_migrator(".","artg4tk","9.07.01")


def sanitize_environments(*args):
    for env in args:
        for var in ('PATH', 'CET_PLUGIN_PATH',
                    'LD_LIBRARY_PATH', 'DYLD_LIBRARY_PATH', 'LIBRARY_PATH',
                    'CMAKE_PREFIX_PATH', 'ROOT_INCLUDE_PATH'):
            env.prune_duplicate_paths(var)
            env.deprioritize_system_paths(var)


class Lardata(CMakePackage):
    """Lardata"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/lardata"
    url      = "https://github.com/LArSoft/lardata.git"

    version('MVP1a', git='https://github.com/LArSoft/lardata.git', branch='feature/MVP1a')
    version('09.01.03', tag='v09_01_03', git='https://github.com/LArSoft/lardata.git', get_full_repo=True)

    version('08.10.02', tag='v08_10_02', git='https://github.com/LArSoft/lardata.git', get_full_repo=True)
    version('08.11.00', tag='v08_11_00', git='https://github.com/LArSoft/lardata.git', get_full_repo=True)
    version('08.11.01', tag='v08_11_01', git='https://github.com/LArSoft/lardata.git', get_full_repo=True)
    version('08.12.00', tag='v08_12_00', git='https://github.com/LArSoft/lardata.git', get_full_repo=True)
    version('08.13.00', tag='v08_13_00', git='https://github.com/LArSoft/lardata.git', get_full_repo=True)
    version('08.14.02', tag='v08_14_02', git='https://github.com/LArSoft/lardata.git', get_full_repo=True)
    version('08.15.04', tag='v08_15_04', git='https://github.com/LArSoft/lardata.git', get_full_repo=True)

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    patch = patcher

    depends_on('nutools')
    depends_on('larcore')
    depends_on('lardataobj')
    depends_on('lardataalg')
    depends_on('range-v3')
    depends_on('cetmodules', type='build')

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value)
               ]
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
        # Set path to find fhicl files
        spack_env.prepend_path('FHICL_FILE_PATH',
                               os.path.join(self.build_directory, 'job'))
        run_env.prepend_path('FHICL_FILE_PATH', os.path.join(self.prefix, 'job'))
        # Set path to find gdml files
        spack_env.prepend_path('FW_SEARCH_PATH',
                               os.path.join(self.build_directory, 'job'))
        run_env.prepend_path('FW_SEARCH_PATH', os.path.join(self.prefix, 'job'))
        # Cleaup.
        sanitize_environments(spack_env, run_env)

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        # Ensure we can find plugin libraries.
        spack_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        run_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        spack_env.prepend_path('PATH', self.prefix.bin)
        run_env.prepend_path('PATH', self.prefix.bin)
        spack_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        spack_env.append_path('FHICL_FILE_PATH','{0}/job'.format(self.prefix))
        run_env.append_path('FHICL_FILE_PATH','{0}/job'.format(self.prefix))
        spack_env.append_path('FW_SEARCH_PATH','{0}/gdml'.format(self.prefix))
        run_env.append_path('FW_SEARCH_PATH','{0}/gdml'.format(self.prefix))
