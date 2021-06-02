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
    cetmodules_20_migrator(".","artg4tk","9.07.01")



def sanitize_environments(*args):
    for env in args:
        for var in ('PATH', 'CET_PLUGIN_PATH',
                    'LD_LIBRARY_PATH', 'DYLD_LIBRARY_PATH', 'LIBRARY_PATH',
                    'CMAKE_PREFIX_PATH', 'ROOT_INCLUDE_PATH'):
            env.prune_duplicate_paths(var)
            env.deprioritize_system_paths(var)


class Larsoft(CMakePackage):
    """Larsoft"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larsoft"
    url      = "https://github.com/LArSoft/larsoft.git"
    version('09.24.01', tag='v09_24_01', git='https://github.com/LArSoft/larsoft.git', get_full_repo=True)
    version('09.23.01.01', tag='v09_23_01_01', git='https://github.com/LArSoft/larsoft.git', get_full_repo=True)
    version('09.22.01', tag='v09_22_01', git='https://github.com/LArSoft/larsoft.git', get_full_repo=True)

    version('MVP1a', git='https://github.com/LArSoft/larsoft.git', branch='feature/MVP1a')
    version('09.09.00', tag='v09_09_00', git='https://github.com/LArSoft/larsoft.git', get_full_repo=True)
    version('08.38.01', tag='v08_38_01', git='https://github.com/LArSoft/larsoft.git', get_full_repo=True)
    version('08.39.00', tag='v08_39_00', git='https://github.com/LArSoft/larsoft.git', get_full_repo=True)
    version('08.40.00', tag='v08_40_00', git='https://github.com/LArSoft/larsoft.git', get_full_repo=True)
    version('08.43.00', tag='v08_43_00', git='https://github.com/LArSoft/larsoft.git', get_full_repo=True)
    version('08.50.00', tag='v08_50_00', git='https://github.com/LArSoft/larsoft.git', get_full_repo=True)
    version('08.50.02', tag='v08_50_02', git='https://github.com/LArSoft/larsoft.git', get_full_repo=True)

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')


    depends_on('cetmodules', type='build')
    depends_on('ifdh-art')
    depends_on('larana')
    depends_on('lareventdisplay')
    depends_on('larexamples')
    depends_on('larg4')
    depends_on('larpandora')
    depends_on('larreco')
    depends_on('larrecodnn')
    depends_on('larsimrad')
    depends_on('larsoft-data')
    depends_on('larsoftobj')
    depends_on('larwirecell')

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value)
               ]
        return args


    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('LARSOFT_INC',self.prefix.include)
        spack_env.set('LARSOFT_LIB', self.prefix.lib)
        spack_env.prepend_path('PATH', self.prefix.bin)
        run_env.prepend_path('PATH', self.prefix.bin)
        spack_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        spack_env.prepend_path('PATH', self.prefix.bin)
        run_env.prepend_path('PATH', self.prefix.bin)
        spack_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        spack_env.append_path('FHICL_FILE_PATH','{0}/job'.format(self.prefix))
        run_env.append_path('FHICL_FILE_PATH','{0}/job'.format(self.prefix))
        spack_env.append_path('FW_SEARCH_PATH','{0}/gdml'.format(self.prefix))
        run_env.append_path('FW_SEARCH_PATH','{0}/gdml'.format(self.prefix))
        sanitize_environments(spack_env, run_env)

    @run_after('install')
    def rename_bin_python(self):
        import os
        os.rename( join_path(self.spec.prefix, "bin/python"),
                   join_path(self.spec.prefix, "bin/python-scripts"))

