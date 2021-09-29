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


class Larsim(CMakePackage):
    """Larsim"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larsim"
    url      = "https://github.com/LArSoft/larsim/archive/v01_02_03.tar.gz"

    version('09.30.00.rc', branch='v09_30_00_rc_br', git='https://github.com/gartung/larsim.git', get_full_repo=True)

    version('09.13.02.01', tag='v09_13_02_01', git='https://github.com/LArSoft/larsim.git', get_full_repo=True)
    version('09.13.01', tag='v09_13_01', git='https://github.com/LArSoft/larsim.git', get_full_repo=True)
    version('mwm1', tag='mwm1', git='https://github.com/marcmengel/larsim.git', get_full_repo=True)

    version('MVP1a', git='https://github.com/LArSoft/larsim.git', branch='feature/MVP1a')
    version('09.06.00', tag='v09_06_00', git='https://github.com/LArSoft/larsim.git', get_full_repo=True)
    version('08.17.01', tag='v08_17_01', git='https://github.com/LArSoft/larsim.git', get_full_repo=True)
    version('08.17.01', tag='v08_17_01', git='https://github.com/LArSoft/larsim.git', get_full_repo=True)
    version('08.18.00', tag='v08_18_00', git='https://github.com/LArSoft/larsim.git', get_full_repo=True)
    version('08.18.01', tag='v08_18_01', git='https://github.com/LArSoft/larsim.git', get_full_repo=True)
    version('08.19.00', tag='v08_19_00', git='https://github.com/LArSoft/larsim.git', get_full_repo=True)
    version('08.19.01', tag='v08_19_01', git='https://github.com/LArSoft/larsim.git', get_full_repo=True)
    version('08.19.02', tag='v08_19_02', git='https://github.com/LArSoft/larsim.git', get_full_repo=True)
    version('08.19.03', tag='v08_19_03', git='https://github.com/LArSoft/larsim.git', get_full_repo=True)
    version('08.19.04', tag='v08_19_04', git='https://github.com/LArSoft/larsim.git', get_full_repo=True)
    version('08.22.03', tag='v08_22_03', git='https://github.com/LArSoft/larsim.git', get_full_repo=True)
    version('08.22.05', tag='v08_22_05', git='https://github.com/LArSoft/larsim.git', get_full_repo=True)

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')



    depends_on('larsoft-data')
    depends_on('larevt')
    depends_on('marley')
    depends_on('cry')
    depends_on('genie')
    depends_on('ifdhc')
    depends_on('xerces-c')
    depends_on('libxml2')
    depends_on('clhep')
    depends_on('nug4')
    depends_on('nugen')
    depends_on('nurandom')
    depends_on('sqlite')
    depends_on('cetmodules', type='build')

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value),
               '-DIFDH_INC={0}'.
                format(self.spec['ifdhc'].prefix.include),
               '-DIFDH_LIB={0}'.
                format(self.spec['ifdhc'].prefix),
               '-DGENIE_INC={0}'.
                format(self.spec['genie'].prefix.include),
                '-DGENIE_VERSION=v{0}'.
                format(self.spec['genie'].version.underscored),
                '-DLARSOFT_DATA_DIR=v{0}'.
                format(self.spec['larsoft-data'].prefix),
                '-DLARSOFT_DATA_VERSION=v{0}'.
                format(self.spec['larsoft-data'].version.underscored),
                '-DIGNORE_ABSOLUTE_TRANSITIVE_DEPENDENCIES=1'
        ]
        return args

    def flag_handler(self, name, flags):
        if name == 'cxxflags' and  self.spec.compiler.name == 'gcc':
            flags.append('-Wno-error=deprecated-declarations')
            flags.append('-Wno-error=class-memaccess')
        return (flags, None, None)

    def setup_environment(self, spack_env, run_env):
        spack_env.prepend_path('LD_LIBRARY_PATH', str(self.spec['root'].prefix.lib))
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
        spack_env.prepend_path('FHICL_INCLUDE_PATH',
                               os.path.join(self.build_directory, 'job'))
        run_env.prepend_path('FHICL_INCLUDE_PATH', os.path.join(self.prefix, 'job'))
        # Set path to find gdml files
        spack_env.prepend_path('FW_SEARCH_PATH',
                               os.path.join(self.build_directory, 'job'))
        run_env.prepend_path('FW_SEARCH_PATH', os.path.join(self.prefix, 'job'))
        # Cleaup.
        sanitize_environments(spack_env, run_env)

        # ups env vars used in build...
        spack_env.set('LIBXML2_FQ_DIR', self.spec['libxml2'].prefix)
        spack_env.set('GEANT4_FQ_DIR', self.spec['geant4'].prefix)
        spack_env.set('XERCES_C_INC', self.spec['xerces-c'].prefix.include)
        spack_env.set('GENIE_FQ_DIR', self.spec['genie'].prefix)
        spack_env.set('GENIE_INC', self.spec['genie'].prefix.include)
        spack_env.set('CRYHOME', self.spec['cry'].prefix)


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
