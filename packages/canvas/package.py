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
                    'CMAKE_PREFIX_PATH', 'ROOT_INCLUDE_PATH'):
            env.prune_duplicate_paths(var)
            env.deprioritize_system_paths(var)


class Canvas(CMakePackage):
    """The underpinnings for the art suite."""

    homepage = 'https://art.fnal.gov/'

    git_base = 'https://github.com/art-framework-suite/canvas.git'
    url = 'https://github.com/art-framework-suite/canvas/archive/refs/tags/v3_09_01.tar.gz'
    list_url = 'https://api.github.com/repos/art-framework-suite/canvas/tags'

    version('3.12.05', sha256='e0a0506528ab1f4db4b76bd3b68f0ea1ea97a627a68930abbfa1b2bfea069ee9')
    version('3.12.04', sha256='bcbb9680000a0f1eec4ec3983b49d8a89f6820d4abdee2ffcb7bd769a0799974')
    version('3.12.03', sha256='cd96833170c8dafa695eb8cd2ef7aea3dc93efa2d200f2b3b6c1886048ad0ddd')
    version('3.12.02', sha256='714c2b960577062323a4738ab1c3bee5b525c3775d0fa831e27b522c7eda06b1')
    version('3.12.01', sha256='bc76a1e4bb306e4ce251195786797bb4b9bc61c3f5115217bcb11c58e1e810dd')
    version('3.12.00', sha256='0789ddd2d4289aa3c86cf6942aaa95dbf730d1d1d99295d43a6d5acd8cde098f')
    version('3.11.00', sha256='b44241a79043d36ed1b24c20088fd797c3d2dbd84997a1af73077eafd7d55536')
    version('3.10.02', sha256='64d3ea1ed78ff3ee60b87c805770c3ef9deedb9b448516a5a38e43aaa3add309')
    version('3.10.01', sha256='ccb3359bd36aede933d6c1d80c9bd2b7c258c11e07794aea09b99826a2c6f0ac')
    version('3.10.00', sha256='ddf1d073c71d9ac3578727e3542a86a68266841c95b1c9db9b8725d500fc2d78')
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

    depends_on('clhep')
    depends_on('boost')
    depends_on('cetlib')
    depends_on('cetlib-except')
    depends_on('cppunit')
    depends_on('fhicl-cpp')
    depends_on('hep-concurrency', when='@MVP1a')
    depends_on('messagefacility')
    depends_on('range-v3')
    depends_on('tbb', when='@MVP')


    if 'SPACKDEV_GENERATOR' in os.environ:
        generator = os.environ['SPACKDEV_GENERATOR']
        if generator.endswith('Ninja'):
            depends_on('ninja', type='build')

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value)]
        return args

    def setup_build_environment(self, spack_env):
        # Binaries.
        spack_env.prepend_path('PATH', os.path.join(self.build_directory, 'bin'))
        # Cleanup.
        sanitize_environments(spack_env)

    @run_after('install')
    def rename_README(self):
        import os
        if os.path.exists(join_path(self.spec.prefix, "README")):
            os.rename( join_path(self.spec.prefix, "README"),
                       join_path(self.spec.prefix, "README_%s"%self.spec.name))
