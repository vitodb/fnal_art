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


class FhiclCpp(CMakePackage):
    """A C++ implementation of the FHiCL configuration language for the art
    suite.
    """

    homepage = 'https://art.fnal.gov/'
    git_base = 'https://github.com/art-framework-suite/fhicl-cpp.git'
    url = 'https://github.com/art-framework-suite/fhicl-cpp/archive/refs/tags/v3_09_01.tar.gz'
    list_url = 'https://api.github.com/repos/art-framework-suite/fhicl-cpp/tags'


    version('MVP1a', branch='feature/Spack-MVP1a', git=git_base, preferred=True)
    version('MVP', branch='feature/for_spack', git=git_base)
    version('develop', branch='develop', git=git_base, get_full_repo=True)


    #patch('fhicl-cpp-dev.patch', when='@develop')

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
    depends_on('py-pybind11', type='build')

    # Build / link dependencies.
    depends_on('boost')
    depends_on('cetlib')
    depends_on('cetlib-except')
    depends_on('hep-concurrency')
    depends_on('sqlite')
    depends_on('openssl')
    depends_on('python')

    if 'SPACKDEV_GENERATOR' in os.environ:
        generator = os.environ['SPACKDEV_GENERATOR']
        if generator.endswith('Ninja'):
            depends_on('ninja', type='build')

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value)]
        return args

    def setup_environment(self, spack_env, run_env):
        # Path for tests.
        spack_env.prepend_path('PATH', os.path.join(self.build_directory, 'bin'))
        # Cleanup
        sanitize_environments(spack_env, run_env)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        # Binaries.
        spack_env.prepend_path('PATH', self.prefix.bin)
        run_env.prepend_path('PATH', self.prefix.bin)
        spack_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)

    @run_after('install')
    def rename_README(self):
        import os
        if os.path.exists(join_path(self.spec.prefix, "README")):
            os.rename( join_path(self.spec.prefix, "README"),
                       join_path(self.spec.prefix, "README_%s"%self.spec.name))
