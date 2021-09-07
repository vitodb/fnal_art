# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import sys
import llnl.util.tty as tty


def sanitize_environments(*args):
    for env in args:
        for var in ('PATH', 'CET_PLUGIN_PATH',
                    'LD_LIBRARY_PATH', 'DYLD_LIBRARY_PATH', 'LIBRARY_PATH',
                    'CMAKE_PREFIX_PATH', 'ROOT_INCLUDE_PATH'):
            env.prune_duplicate_paths(var)
            env.deprioritize_system_paths(var)


class Larcore(CMakePackage):
    """Larcore"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larcore"
    url      = "https://github.com/LArSoft/larcore/archive/v01_02_03.tar.gz"

    version('09.30.00.rc', branch='v09_30_00_rc_br', git='https://github.com/gartung/larcore.git', get_full_repo=True)
    version('09.24.01.01', tag='v09_02_01_01', git='https://github.com/marcmengel/larcore.git', get_full_repo=True)
    version('09.02.01', tag='v09_02_01', git='https://github.com/LArSoft/larcore.git', get_full_repo=True)

    version('mwm1', tag='mwm1', git='https://github.com/marcmengel/larcore.git', get_full_repo=True)
    version('MVP1a', git='https://github.com/LArSoft/larcore.git', branch='feature/MVP1a')
    version('09.00.01', tag='v09_00_01', git='https://github.com/LArSoft/larcore.git', get_full_repo=True)
    version('08.07.00', tag='v08_07_00', git='https://github.com/LArSoft/larcore.git', get_full_repo=True)
    version('08.07.01', tag='v08_07_01', git='https://github.com/LArSoft/larcore.git', get_full_repo=True)
    version('08.08.00', tag='v08_08_00', git='https://github.com/LArSoft/larcore.git', get_full_repo=True)
    version('08.08.01', tag='v08_08_01', git='https://github.com/LArSoft/larcore.git', get_full_repo=True)
    version('08.09.00', tag='v08_09_00', git='https://github.com/LArSoft/larcore.git', get_full_repo=True)
    version('08.10.00', tag='v08_10_00', git='https://github.com/LArSoft/larcore.git', get_full_repo=True)
    version('08.10.01', tag='v08_10_01', git='https://github.com/LArSoft/larcore.git', get_full_repo=True)
    version('08.10.02', tag='v08_10_02', git='https://github.com/LArSoft/larcore.git', get_full_repo=True)
    version('08.10.03', tag='v08_10_03', git='https://github.com/LArSoft/larcore.git', get_full_repo=True)
    version('08.11.03', tag='v08_11_03', git='https://github.com/LArSoft/larcore.git', get_full_repo=True)
    version('08.11.05', tag='v08_11_05', git='https://github.com/LArSoft/larcore.git', get_full_repo=True)

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')


    depends_on('messagefacility')
    depends_on('larcorealg')
    depends_on('art-root-io')
    depends_on('cetmodules', type='build')

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value)
               ]
        return args


    @run_after('cmake')
    def fix_static_boost(self):
        print("fixing filesysem.a references..")
        os.system("set -x; find %s/test/Geometry/CMakeFiles %s/larcore/Geometry/CMakeFiles -type f -print  | tee /tmp/fixlist | xargs perl -pi -e 's/libboost_filesystem.a/libboost_filesystem.so/go;'" % (self.build_directory, self.build_directory ))
        print("done fixing filesysem.a references..")

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
        spack_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
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

