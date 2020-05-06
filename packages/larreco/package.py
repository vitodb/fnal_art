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
from cetmodules_patcher import cetmodules_dir_patcher

def patcher(x):
    cetmodules_dir_patcher(".","larreco","08.28.00")

def sanitize_environments(*args):
    for env in args:
        for var in ('PATH', 'CET_PLUGIN_PATH',
                    'LD_LIBRARY_PATH', 'DYLD_LIBRARY_PATH', 'LIBRARY_PATH',
                    'CMAKE_PREFIX_PATH', 'ROOT_INCLUDE_PATH'):
            env.prune_duplicate_paths(var)
            env.deprioritize_system_paths(var)


class Larreco(CMakePackage):
    """Larreco"""

    homepage = "http://cdcvs.fnal.gov/redmine/projects/larreco"
    url      = "https://github.com/LArSoft/larreco.git"

    version('MVP1a', git='https://github.com/LArSoft/larreco.git', branch='feature/MVP1a')
    version('08.25.00', tag='v08_25_00', git='https://github.com/LArSoft/larreco.git')
    version('08.25.01', tag='v08_25_01', git='https://github.com/LArSoft/larreco.git')
    version('08.26.00', tag='v08_26_00', git='https://github.com/LArSoft/larreco.git')
    version('08.26.01', tag='v08_26_01', git='https://github.com/LArSoft/larreco.git')
    version('08.28.00', tag='v08_28_00', git='https://github.com/LArSoft/larreco.git')
    version('08.29.00', tag='v08_29_00', git='https://github.com/LArSoft/larreco.git')
    version('08.31.00', tag='v08_31_00', git='https://github.com/LArSoft/larreco.git')
    version('08.31.01', tag='v08_31_01', git='https://github.com/LArSoft/larreco.git')
    version('08.31.03', tag='v08_31_03', git='https://github.com/LArSoft/larreco.git')

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')
    variant('tf', default=False, description='Build tensorflow dependent libraries.')
    
    patch('larreco.unups.patch', when='@08.29.00')
    patch('larreco.08.31.01.patch', when='@08.31.01:')

    depends_on('tbb')
    depends_on('clhep')
    depends_on('root')
    depends_on('geant4')
    depends_on('boost')
    depends_on('art')
    depends_on('canvas-root-io')
    depends_on('larsim')
    depends_on('larsoft-data')
    depends_on('marley')
    depends_on('nutools')
    depends_on('eigen+fftw')
    depends_on('tensorflow', when='+tf')
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
        spack_env.set('LARRECO_INC',self.prefix.include)
        spack_env.set('LARRECO_LIB', self.prefix.lib)
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
        sanitize_environments(spack_env, run_env)

