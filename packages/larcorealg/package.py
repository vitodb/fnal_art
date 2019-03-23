# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


def sanitize_environments(*args):
    for env in args:
        for var in ('PATH', 'CET_PLUGIN_PATH',
                    'LD_LIBRARY_PATH', 'DYLD_LIBRARY_PATH', 'LIBRARY_PATH',
                    'CMAKE_PREFIX_PATH', 'ROOT_INCLUDE_PATH'):
            env.prune_duplicate_paths(var)
            env.deprioritize_system_paths(var)


class Larcorealg(CMakePackage):
    """Larcorealg"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larcorealg"
    url      = "http://cdcvs.fnal.gov/projects/larcorealg"

    version('MVP1a', git='http://cdcvs.fnal.gov/projects/larcorealg', branch='feature/Spack-MVP1a', preferred=True)

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')


    depends_on('larcoreobj')
    depends_on('cetmodules', type='build')

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value),
               ]
        return args

    def setup_environment(self, spack_env, run_env):
        # Binaries.
        spack_env.prepend_path('PATH',
                               join_path(self.build_directory, 'bin'))
        # Ensure we can find plugin libraries.
        spack_env.prepend_path('CET_PLUGIN_PATH',
                               join_path(self.build_directory, 'lib'))
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
                               join_path(self.build_directory, 'perllib'))
        run_env.prepend_path('PERL5LIB', join_path(self.prefix, 'perllib'))
        # Cleaup.
        sanitize_environments(spack_env, run_env)

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('LARCOREALG_INC',dspec['larcorealg'].prefix.include)
        spack_env.append_path('FHICL_FILE_PATH','{0}/job'.format(dspec['larcorealg'].prefix))
        spack_env.append_path('ROOT_INCLUDE_PATH',dspec['larcorealg'].prefix.include)
        spack_env.set('LARCOREALG_LIB', dspec['larcorealg'].prefix.lib)
