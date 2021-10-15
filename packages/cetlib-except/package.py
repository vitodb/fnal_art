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


class CetlibExcept(CMakePackage):
    """Exception libraries for the art suite."""

    homepage = 'https://art.fnal.gov/'
    git_base = 'https://github.com/art-framework-suite/cetlib-except.git'
    url = 'https://github.com/art-framework-suite/cetlib-except/archive/refs/tags/v1_07_04.tar.gz'
    list_url = 'https://api.github.com/repos/art-framework-suite/cetlib-except/tags'

    version('1.07.04', sha256='d021d26fda9f4f57b57850bc6f5ac0a79aed913ef1cde68a96838ad85d332d70')
    version('1.07.03', sha256='30ecc2e20899eb35e71f88754f7ae5142b7b5b61432c8191dc3fe4e802b515f2')
    version('1.07.02', sha256='5228cd4634c79dd67d727523c506a53f56b4d63d4581f72b9752795b1e1df30f')
    version('1.07.01', sha256='e2a8466801a5c6d2d3bfa65bdea87814e2151fc782139134a74a47c6cb17756d')
    version('1.07.00', sha256='a9d5d39c6aa2537a7befda3e2e0bf6b518014b8bcafa755124645739a9ca9fd0')
    version('1.06.00', sha256='836b549bda499045e846acccb4fa4f6877189b106d36b1182d5b03fa2d50d3d8')
    version('1.05.00', sha256='a00262819d2b9c34f4a96c0f7ab299b9763633c81ca7ec22ccc024aae404895e')
    version('1.04.01', sha256='1d2c8cca4894deeeed5ecba6d0ee089f33104471e15712d554fc5eee5a3b9cf2')
    version('1.04.00', sha256='43bb4588b418219db96ce05fe63bdbabc3b4eae3d0c644bab1a936af2d204f88')
    version('1.03.04', sha256='bca1442bfbd7e67b0051ee93f3e5c25ce07fe36bed6aec613a7605743b7d74e6')
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

    depends_on('cmake@3.11:', type='build')
    depends_on('cetmodules', type='build')
    depends_on('cetpkgsupport', type=('build','run'))
    depends_on('catch2', type=('build','run'))

    if 'SPACKDEV_GENERATOR' in os.environ:
        generator = os.environ['SPACKDEV_GENERATOR']
        if generator.endswith('Ninja'):
            depends_on('ninja', type='build')

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value)]
        return args

    def setup_build_environment(self, spack_env):
        # For tests.
        spack_env.prepend_path('PATH', os.path.join(self.build_directory, 'bin'))
        # Cleanup.
        sanitize_environments(spack_env)

    @run_after('install')
    def rename_README(self):
        import os
        if os.path.exists(join_path(self.spec.prefix, "README")):
            os.rename( join_path(self.spec.prefix, "README"),
                       join_path(self.spec.prefix, "README_%s"%self.spec.name))
