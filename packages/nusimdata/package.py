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


class Nusimdata(CMakePackage):
    """Nusimdata"""

    homepage = "http://cdcvs.fnal.gov/redmine/projects/nusimdata"
    url      = "http://cdcvs.fnal.gov/projects/nusimdata"

    version('MVP1a', git='http://cdcvs.fnal.gov/projects/nusimdata', branch='feature/Spack-MVP1a', preferred=True)

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')


    # Build and link dependencies.
    depends_on('canvas-root-io')
    depends_on('dk2nudata')
    depends_on('cetmodules', type='build')

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value),
                '-DDK2NUDATA_INC={0}'.
                format(self.spec['dk2nudata'].prefix.include),
                '-DDK2NUDATA_LIB={0}'.
                format(self.spec['dk2nudata'].prefix.lib),
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
        spack_env.set('NUSIMDATA_INC',self.prefix.include)
        spack_env.set('NUSIMDATA_LIB', self.prefix.lib)
        spack_env.append_path('ROOT_INCLUDE_PATH', self.prefix.include)
        # Ensure we can find plugin libraries.
        spack_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        run_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        spack_env.prepend_path('PATH', self.prefix.bin)
        run_env.prepend_path('PATH', self.prefix.bin)
        spack_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)

    # install_fhicl() is callled but there are no fcl files to install
    # however nusimdataConfig.cmake does a set and check on nusimdata_fcl_dir
    @run_after('install')
    def create_dirs(self):
        mkdirp('{0}/fcl'.format(self.spec.prefix))
