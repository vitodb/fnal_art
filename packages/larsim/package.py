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
from cetmodules_patcher import cetmodules_20_migrator

def patcher(x):
    cetmodules_20_migrator(".","larsim","08.19.03")

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
    url      = "https://github.com/LArSoft/larsim.git"

    version('MVP1a', git='https://github.com/LArSoft/larsim.git', branch='feature/MVP1a')
    version('08.17.00', tag='v08_17_00', git='https://github.com/LArSoft/larsim.git')
    version('08.17.01', tag='v08_17_01', git='https://github.com/LArSoft/larsim.git')
    version('08.18.00', tag='v08_18_00', git='https://github.com/LArSoft/larsim.git')
    version('08.18.01', tag='v08_18_01', git='https://github.com/LArSoft/larsim.git')
    version('08.19.00', tag='v08_19_00', git='https://github.com/LArSoft/larsim.git')
    version('08.19.01', tag='v08_19_01', git='https://github.com/LArSoft/larsim.git')
    version('08.19.02', tag='v08_19_02', git='https://github.com/LArSoft/larsim.git')
    version('08.19.03', tag='v08_19_03', git='https://github.com/LArSoft/larsim.git')
    version('08.19.04', tag='v08_19_04', git='https://github.com/LArSoft/larsim.git')
    version('08.22.03', tag='v08_22_03', git='https://github.com/LArSoft/larsim.git')
    version('08.22.05', tag='v08_22_05', git='https://github.com/LArSoft/larsim.git')

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    patch = patcher

    depends_on('larsoft-data')
    depends_on('larevt')
    depends_on('marley')
    depends_on('genie')
    depends_on('ifdhc')
    depends_on('xerces-c')
    depends_on('libxml2')
    depends_on('clhep')
    depends_on('nug4')
    depends_on('nugen')
    depends_on('nurandom')
    depends_on('cetmodules@2.00:', type='build')

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
        spack_env.prepend_path('FHICL_INCLUDE_PATH',
                               os.path.join(self.build_directory, 'job'))
        run_env.prepend_path('FHICL_INCLUDE_PATH', os.path.join(self.prefix, 'job'))
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
