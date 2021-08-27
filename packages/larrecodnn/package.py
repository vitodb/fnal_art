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


class Larrecodnn(CMakePackage):
    """Larrecodnn"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larrecodnn"
    url      = "https://github.com/LArSoft/larrecodnn.git"


    version('09.06.07', sha256='f0aca1bc7b53f07a377006c8f36e3682d29e29c2a1cedf478be40d263e03658f')
    version('9.06.06', sha256='b914e26f2537d1f26035a8c357f0ad09ba5c80d1c38fdaa62de9b72b559b0499')
    version('9.06.05', sha256='a99775d149afaf072a1b139795f9ba5075525ab85e42f52267bcced105257c2d')
    version('9.06.04', sha256='867e1ec2fb006189e5bd7f12433a97d8ec3b6916cc9dcc55384360d0e936ba66')

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    def url_for_version(self, version):
        return "https://github.com/LArSoft/larrecodnn/archive/refs/tags/v{0}.tar.gz".format(version.underscored)

    depends_on('cetmodules', type='build')
    depends_on('larcoreobj')
    depends_on('larcorealg')
    depends_on('larcore')
    depends_on('lardataobj')
    depends_on('lardataalg')
    depends_on('lardata')
    depends_on('larevt')
    depends_on('larsim')
    depends_on('larreco')
    depends_on('nutools')
    depends_on('nug4')
    depends_on('nurandom')
    depends_on('art')
    depends_on('art-root-io')
    depends_on('postgresql')
    depends_on('range-v3')
    depends_on('eigen')
    depends_on('root')
    depends_on('py-tensorflow')
    depends_on('triton')
    depends_on('tbb')

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

    def flag_handler(self, name, flags):
        if name == 'cxxflags' and  self.spec.compiler.name == 'gcc':
            flags.append('-Wno-error=deprecated-declarations')
            flags.append('-Wno-error=class-memaccess')
        return (flags, None, None)


    version('mwm1', tag='mwm1', git='https://github.com/marcmengel/larrecodnn.git', get_full_repo=True)
