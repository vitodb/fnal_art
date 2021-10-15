# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
from llnl.util import tty
import sys
import os
import spack.util.spack_json as sjson


def sanitize_environments(*args):
    for env in args:
        for var in ('PATH', 'CET_PLUGIN_PATH',
                    'LD_LIBRARY_PATH', 'DYLD_LIBRARY_PATH', 'LIBRARY_PATH',
                    'CMAKE_INSTALL_RPATH', 'CMAKE_PREFIX_PATH', 'ROOT_INCLUDE_PATH'):
            env.prune_duplicate_paths(var)
            env.deprioritize_system_paths(var)


class Critic(CMakePackage):
    """Compatibility tests for the art and gallery applications of the art
    suite.
    """

    homepage = 'https://art.fnal.gov/'
    git_base = 'https://github.com/art-framework-suite/critic.git'
    url = 'https://github.com/art-framework-suite/critic/archive/refs/tags/v3_09_01.tar.gz'
    list_url = 'https://api.github.com/repos/art-framework-suite/critic/tags'

    version('2.08.04', sha256='74582f77a8ab39e6a814b900d53248ab3227c45861cb019ac45c92116a0b8b33')
    version('2.08.03', sha256='858fd4d099a628663d0a61b3bfaf2db5937bd6019403769699e8c313b6563dcc')
    version('2.08.02', sha256='aea48582e1927610c2c34df5a4f9491eb390ab72d64dd50a7c16d4542d774eed')
    version('2.08.01', sha256='a8a95b007451f297373cbb0e2dc97e86eed36026c264aee6b69d7b6347e1ba5d')
    version('2.08.00', sha256='435e06d16b887016df52899262326ed355bf5213cff4b4e8a6ce9d32bfafeb74')
    version('2.07.00', sha256='431baa00cfcc5e7de36f0dae04231bb90fa4f4127a9a78dd9b585d4e2bdbc431')
    version('2.06.00', sha256='fb55b0cf31dd2bb7be24511cc4946fa4aa6bcf117d83ec3dc2cae724e5f26933')
    version('2.05.03', sha256='15ac1f8e905dbebccb6818ca680bdc71eacdbb39899f62f5e535a3ae4fff3e26')
    version('2.05.02', sha256='94025a9707043d81448209893a3d191b614163f71052f35126fb5ef3dc1fd9e9')
    version('2.05.01', sha256='3a92d50e0df7d285e1f6f64447623e56373433a0e6d610675d494cd9ca6be0fc')
    version('MVP1a', branch='archive/feature/Spack-MVP1a', git=git_base, get_full_repo=True)
    version('MVP', branch='archive/feature/for_spack', git=git_base, get_full_repo=True)
    version('develop', branch='develop', git=git_base, get_full_repo=True)

    def url_for_version(self, version):
        url = 'https://github.com/art-framework-suite/{0}/archive/v{1}.tar.gz'
        return url.format(self.name, version.underscored)

    def fetch_remote_versions(self, concurrency=None):
        return dict(map(lambda v: (v.dotted, self.url_for_version(v)),
                        [ Version(d['name'][1:]) for d in
                          sjson.load(
                              spack.util.web.read_from_url(
                                  self.list_url,
                                  accept_content_type='application/json')[2])
                          if d['name'].startswith('v') ]))

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')


    # Build-only dependencies.
    depends_on('cmake@3.11:', type='build')
    depends_on('cetmodules', type='build')

    # Build and link dependencies.
    depends_on('clhep@2.4.1.0:', when='@MVP1a')
    depends_on('art')
    depends_on('art-root-io', when='@MVP1a')
    depends_on('boost')
    depends_on('canvas')
    depends_on('cetlib')
    depends_on('fhicl-cpp', when='@MVP1a')
    depends_on('gallery')
    depends_on('hep-concurrency', when='@MVP1a')
    depends_on('messagefacility', when='@MVP1a')
    depends_on('root+python')
    depends_on('python')

    if 'SPACKDEV_GENERATOR' in os.environ:
        generator = os.environ['SPACKDEV_GENERATOR']
        if generator.endswith('Ninja'):
            depends_on('ninja', type='build')

    def cmake_args(self):
        # Set CMake args.
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value)]
        return args

    def setup_build_environment(self, spack_env):
        spack_env.prepend_path('LD_LIBRARY_PATH', str(self.spec['root'].prefix.lib))
        # Binaries.
        spack_env.prepend_path('PATH',
                               os.path.join(self.build_directory, 'bin'))
        # Ensure we can find plugin libraries.
        spack_env.prepend_path('CET_PLUGIN_PATH',
                               os.path.join(self.build_directory, 'lib'))
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(root=False, cover='nodes', order='post',
                                    deptype=('link'), direction='children'):
            spack_env.prepend_path('ROOT_INCLUDE_PATH',
                                   str(self.spec[d.name].prefix.include))
        # Cleanup.
        sanitize_environments(spack_env)

    def setup_run_environment(self, run_env):
        # Ensure we can find plugin libraries.
        run_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(root=False, cover='nodes', order='post',
                                    deptype=('link'), direction='children'):
            run_env.prepend_path('ROOT_INCLUDE_PATH',
                                 str(self.spec[d.name].prefix.include))
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        # Cleanup.
        sanitize_environments(run_env)

    def setup_dependent_build_environment(self, spack_env, dependent_spec):
        # Ensure we can find plugin libraries.
        spack_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        # Cleanup.
        sanitize_environments(spack_env)

    def setup_dependent_run_environment(self, run_env, dependent_spec):
        # Ensure we can find plugin libraries.
        run_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        # Cleanup.
        sanitize_environments(run_env)
