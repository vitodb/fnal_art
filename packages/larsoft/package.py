# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
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


class Larsoft(CMakePackage):
    """Larsoft"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larsoft"
    url      = "https://github.com/LArSoft/larsoft.git"

    version('MVP1a', git='https://github.com/LArSoft/larsoft.git', branch='feature/MVP1a')
    version('08.38.01', tag='v08_38_01', git='https://github.com/LArSoft/larsoft.git')
    version('08.39.00', tag='v08_39_00', git='https://github.com/LArSoft/larsoft.git')
    version('08.40.00', tag='v08_40_00', git='https://github.com/LArSoft/larsoft.git')
    version('08.43.00', tag='v08_43_00', git='https://github.com/LArSoft/larsoft.git')
    version('08.50.00', tag='v08_50_00', git='https://github.com/LArSoft/larsoft.git')
    version('08.50.02', tag='v08_50_02', git='https://github.com/LArSoft/larsoft.git')

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')
    patch = patcher

    depends_on('lareventdisplay')
    depends_on('larexamples')
    depends_on('larana')
    depends_on('larreco')
    depends_on('larg4')
    depends_on('larpandora')
    depends_on('larwirecell')
    depends_on('larsoftobj')
    depends_on('larsoft-data')
    depends_on('ifdh-art')
    depends_on('cetmodules@2.00:', type='build')

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
