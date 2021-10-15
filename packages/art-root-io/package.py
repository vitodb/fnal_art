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


class ArtRootIo(CMakePackage):
    """Root-based input/output for the art suite.
    """

    homepage = 'https://art.fnal.gov/'
    git_base = 'https://github.com/art-framework-suite/art-root-io.git'
    url = 'https://github.com/art-framework-suite/art-root-io/archive/refs/tags/v3_09_01.tar.gz'
    list_url = 'https://api.github.com/repos/art-framework-suite/art-root-io/tags'

    version('1.08.04', sha256='1289e25fe2cfecb41d3de8e30cf614533a987314da0ed6bf701450632611e814')
    version('1.08.03', sha256='fefdb0803bc139a65339d9fa1509f2e9be1c5613b64ec1ec84e99f404663e4bf')
    version('1.08.02', sha256='c3434c77b827927514578d2e194efb2e03a4cba6ad9dda95fe51a8fe64d61a7b')
    version('1.08.01', sha256='e9c403ef2dca38bc51dc91564f193124e75ce64396a7cbb9e2343cb923864d6b')
    version('1.08.00', sha256='9a635df873efd126cc122629eed0c8dcc39759bf1733524e59ca3bf203b7e381')
    version('1.07.00', sha256='d0428cc58d420451db7a6bc767d3454f06a2d3c317ffeed233db65166aedd331')
    version('1.06.00', sha256='a3d000be1ac8cbd441c73e5bb4e90cd372ae389c551596565c5d220a59194edc')
    version('1.05.03', sha256='3b55770d30a248601efed2ee742653759d71c2f3dfdad0435326429d82e004b8')
    version('1.05.02', sha256='30b6cac5e9df1a05594ae4fa6a14bc06247186dc91c52121896ac0b74034e9ae')
    version('1.05.01', sha256='03197ab0d268351ab55897904e6f366f2e21e56b8c4851fe3fff0af3fef0ea5c')
    version('MVP1a', branch='archive/feature/Spack-MVP1a', git=git_base, get_full_repo=True)
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
    depends_on('root+python')
    depends_on('art')
    depends_on('boost')
    depends_on('canvas')
    depends_on('canvas-root-io')
    depends_on('cetlib')
    depends_on('fhicl-cpp')
    depends_on('hep-concurrency')
    depends_on('messagefacility')
    depends_on('sqlite@3.8.2:')

    if 'SPACKDEV_GENERATOR' in os.environ:
        generator = os.environ['SPACKDEV_GENERATOR']
        if generator.endswith('Ninja'):
            depends_on('ninja', type='build')

    def cmake_args(self):
        # Set CMake args.
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value),
                '-Dart_MODULE_PLUGINS=FALSE']
        return args

    def setup_build_environment(self, spack_env):
        # Binaries.
        spack_env.prepend_path('PATH',
                               os.path.join(self.build_directory, 'bin'))
        # Ensure we can find plugin libraries.
        spack_env.prepend_path('CET_PLUGIN_PATH',
                               os.path.join(self.build_directory, 'lib'))
        # Set LD_LIBRARY_PATH sp CheckClassVersion.py can find cppyy lib
        spack_env.prepend_path('LD_LIBRARY_PATH',
                                join_path(self.spec['root'].prefix.lib))
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
        # Binaries.
        spack_env.prepend_path('PATH',self.prefix.bin)
        # Ensure we can find plugin libraries.
        spack_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        spack_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        # Cleanup.
        sanitize_environments(spack_env)

    def setup_dependent_run_environment(self, run_env, dependent_spec):
        # Ensure we can find plugin libraries.
        run_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        # Cleanup.
        sanitize_environments(run_env)
