# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import sys
import os

def sanitize_environments(*args):
    for env in args:
        for var in ('PATH', 'CET_PLUGIN_PATH',
                    'LD_LIBRARY_PATH', 'DYLD_LIBRARY_PATH', 'LIBRARY_PATH',
                    'CMAKE_PREFIX_PATH', 'ROOT_INCLUDE_PATH'):
            env.prune_duplicate_paths(var)
            env.deprioritize_system_paths(var)


class Larsimrad(CMakePackage):
    """larsimrad """

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larsimrad"
    git_base = 'https://github.com/SBNSoftware/larsimrad.git'
    url      = "https://cdcvs.fnal.gov/projects/larsimrad"

    version('09.30.00.rc', branch='origin/v09_30_00_rc_br', git='https://github.com/gartung/larsimrad.git', get_full_repo=True)
    version('mwm1', tag='mwm1', git='https://github.com/marcmengel/larsimrad.git', get_full_repo=True)
    version('09.01.08', tag='v09_01_08', git=git_base, get_full_repo=True)
    version('09.01.08', tag='v09_01_08', git=git_base, get_full_repo=True)
    version('09.00.13', tag='v09_00_13', git=git_base, get_full_repo=True)
    version('09.00.12', tag='v09_00_12', git=git_base, get_full_repo=True)
    version('09.00.11', tag='v09_00_11', git=git_base, get_full_repo=True)

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    depends_on('cetmodules', type='build')
    depends_on('art-root-io')
    depends_on('larbatch')
    depends_on('py-pycurl')
    depends_on('bxdecay0')
    depends_on('lardata')
    depends_on('nugen')
    depends_on('larsim')

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value)
               ]
        return args

    def setup_environment(self, spack_env, run_env):
        # Binaries.
        spack_env.prepend_path('PATH',
                               os.path.join(self.build_directory, 'bin'))
        spack_env.prepend_path('PYTHONPATH',
                               os.path.join(self.build_directory, 'bin'))
        spack_env.prepend_path('PYTHONPATH',
                               os.path.join(self.build_directory, 'python'))
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
        sanitize_environments(spack_env, run_env)

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('LARSIMRAD_INC',self.prefix.include)
        spack_env.set('LARSIMRAD_LIB', self.prefix.lib)
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
