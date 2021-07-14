# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import sys

def sanitize_environments(*args):
    for env in args:
        for var in ('PATH', 'CET_PLUGIN_PATH',
                    'LD_LIBRARY_PATH', 'DYLD_LIBRARY_PATH', 'LIBRARY_PATH',
                    'CMAKE_PREFIX_PATH', 'ROOT_INCLUDE_PATH'):
            env.prune_duplicate_paths(var)
            env.deprioritize_system_paths(var)


class Larana(CMakePackage):
    """Larana"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larana"
    url      = "https://github.com/LArSoft/larana.git"
    version('09.02.05.01', tag='v09_02_05_01', git='https://github.com/LArSoft/larana.git', get_full_repo=True)
    version('09.02.04', tag='v09_02_04', git='https://github.com/LArSoft/larana.git', get_full_repo=True)

    version('MVP1a', git='https://github.com/LArSoft/larana.git', branch='feature/MVP1a')
    version('09.00.15', tag='v09_00_15', git='https://github.com/LArSoft/larana.git', get_full_repo=True)
    version('08.13.03', tag='v08_13_03', git='https://github.com/LArSoft/larana.git', get_full_repo=True)
    version('08.14.00', tag='v08_14_00', git='https://github.com/LArSoft/larana.git', get_full_repo=True)
    version('08.14.01', tag='v08_14_01', git='https://github.com/LArSoft/larana.git', get_full_repo=True)
    version('08.15.00', tag='v08_15_00', git='https://github.com/LArSoft/larana.git', get_full_repo=True)
    version('08.15.01', tag='v08_15_01', git='https://github.com/LArSoft/larana.git', get_full_repo=True)
    version('08.16.01', tag='v08_16_01', git='https://github.com/LArSoft/larana.git', get_full_repo=True)
    version('08.16.02', tag='v08_16_02', git='https://github.com/LArSoft/larana.git', get_full_repo=True)
    version('08.16.03', tag='v08_16_03', git='https://github.com/LArSoft/larana.git', get_full_repo=True)
    version('08.16.04', tag='v08_16_04', git='https://github.com/LArSoft/larana.git', get_full_repo=True)
    version('08.17.03', tag='v08_17_03', git='https://github.com/LArSoft/larana.git', get_full_repo=True)
    version('08.17.05', tag='v08_17_05', git='https://github.com/LArSoft/larana.git', get_full_repo=True)

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')



    depends_on('larreco')
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
        # Cleaup.
        sanitize_environments(spack_env, run_env)

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('LARANA_INC',self.prefix.include)
        spack_env.set('LARANA_LIB', self.prefix.lib)
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

    def flag_handler(self, name, flags):
        if name == 'cxxflags' and  self.spec.compiler.name == 'gcc':
            flags.append('-Wno-error=deprecated-declarations')
            flags.append('-Wno-error=class-memaccess')
        return (flags, None, None)

    version('mwm1', tag='mwm1', git='https://github.com/marcmengel/larana.git', get_full_repo=True)
