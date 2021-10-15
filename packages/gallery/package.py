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


class Gallery(CMakePackage):
    """A library to allow reading of Root output files produced by the art
    suite.
    """

    homepage='https://art.fnal.gov/'
    git_base = 'https://github.com/art-framework-suite/gallery'
    url = 'https://github.com/art-framework-suite/gallery/archive/refs/tags/v1_18_05.tar.gz'
    list_url = 'https://api.github.com/repos/art-framework-suite/gallery/tags'

    version('1.18.05', sha256='11b6316baf804934fa2189b74923233de8f038c427a6e82c515e999902ffa8f4')
    version('1.18.04', sha256='832c9bf794a915708d659181610f23db6e107388749f4602f6f3fb29dd1896f4')
    version('1.18.03', sha256='748eb315e1ae96bd95c500c82283b023904654c5336d5cb7f866087d0329a374')
    version('1.18.02', sha256='c3ae7eb0bac4bdb1200f68f4a47171a8db22ec5b12ac1d4d5d9885d969a47a76')
    version('1.16.02', sha256='bbc9db71d03da8545a9d2c6fbb39cf9c1c4cf299dce5f5004bf345a5d61277c8')
    version('1.14.02', sha256='411a69f60c9e161172f60ed80e6f7d8d1afc2562b94e97fccb61a02e15a7cc44')
    version('1.14.01', sha256='392145f91f0926b27f06d3bd67063488894668ba884c1fa369f17cc6dbe10032')
    version('1.14.00', sha256='47e32155b54aca12c93f26cfaa765fceff0b166e0cce07893acc04f65444fbe9')
    version('1.13.01', sha256='5d2e063723c77b68e4d681086aa5d8db6fabe237c73b31ca47d245182ed5d85b')
    version('1.13.00', sha256='a24a34cf8e30c670092c4d01ecfbdb3a919dae675ba63efd275f6ad3c0194d5c')
    version('1_12_07', sha256='11a0a6ae294d27ebf3b485314b27506135551acdba9d8a9f9e67c9858b42a2b2')
    version('MVP1a', branch='archive/feature/Spack-MVP1a', git=git_base, get_full_repo=True)
    version('MVP', branch='archive/feature/for_spack', git=git_base, get_full_repo=True)
    version('develop', branch='develop', git=git_base, get_full_repo=True)

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    # Build-only dependencies.
    depends_on('cmake@3.11:', type='build')
    depends_on('cetmodules', type='build')

    # Build and link dependencies.
    depends_on('canvas-root-io')
    depends_on('canvas')
    depends_on('cetlib')
    depends_on('root+python')

    if 'SPACKDEV_GENERATOR' in os.environ:
        generator = os.environ['SPACKDEV_GENERATOR']
        if generator.endswith('Ninja'):
            depends_on('ninja', type='build')

    def url_for_version(self, version):
        #url = 'https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/{0}.v{1}.tbz2'
        url = 'https://github.com/art-framework-suite/{0}/archive/refs/tags/v{1}.tar.gz'
        return url.format(self.name, version.underscored)

    def fetch_remote_versions(self, concurrency=None):
        return dict(map(lambda v: (v.dotted, self.url_for_version(v)),
                        [ Version(d['name'][1:]) for d in
                          sjson.load(
                              spack.util.web.read_from_url(
                                  self.list_url,
                                  accept_content_type='application/json')[2])
                          if d['name'].startswith('v') ]))

    def cmake_args(self):
        # Set CMake args.
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value)]
        return args

    def setup_environment(self, spack_env, run_env):
        # Binaries.
        spack_env.prepend_path('PATH',
                               os.path.join(self.build_directory, 'bin'))
        # Ensure we can find plugin libraries.
        spack_env.prepend_path('CET_PLUGIN_PATH',
                               os.path.join(self.build_directory, 'lib'))
        run_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        # Set LD_LIBRARY_PATH sp CheckClassVersion.py can find cppyy lib
        spack_env.prepend_path('LD_LIBRARY_PATH',
                                join_path(self.spec['root'].prefix.lib))
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(root=False, cover='nodes', order='post',
                                    deptype=('link'), direction='children'):
            spack_env.prepend_path('ROOT_INCLUDE_PATH',
                                   str(self.spec[d.name].prefix.include))
            run_env.prepend_path('ROOT_INCLUDE_PATH',
                                 str(self.spec[d.name].prefix.include))
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        # Cleanup.
        sanitize_environments(spack_env, run_env)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.prepend_path('PATH', self.prefix.bin)
        run_env.prepend_path('PATH', self.prefix.bin)
        spack_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        # Ensure we can find plugin libraries.
        spack_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        run_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        # Cleanup.
        sanitize_environments(spack_env, run_env)

    @run_after('install')
    def rename_README(self):
        import os
        if os.path.exists(join_path(self.spec.prefix, "README")):
            os.rename( join_path(self.spec.prefix, "README"),
                       join_path(self.spec.prefix, "README_%s"%self.spec.name))
