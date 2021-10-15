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

    version('4.15.03', sha256='99ae2b7557c671d0207dea96529e7c0fca2274974b6609cc7c6bf7e8d04bd12b')
    version('4.15.02', sha256='272af50c39ade4b517ff2f9f881fc68f4cf383f6b8a1afca61f51c3a8710c0cd')
    version('4.15.01', sha256='a7226945fe0e0abf0471a08b39651d8727a008f2efdafd6f78812a4420148f4a')
    version('4.15.00', sha256='6bbe5a203e5f33114834aca5dafb92a2d2d392eb7d5b213a331bd41826673aad')
    version('4.14.00', sha256='55f9ebfbfc88d27ee0776e96ce33f4183b4b87a4ac4944b5108b67e764803c80')
    version('4.13.00', sha256='1db473e9d9e491416d220dc28906b027b2356c63204da1a8bbac93e3a0e2ae24')
    version('4.12.02', sha256='bb5eee853f646904721f928c5d721ceba7e93776cb961a031ac4357e542e7be6')
    version('4.12.01', sha256='18a7fcf755b4f13273247e73b6a866348cd5f8a4b6d6defe46097f98725ae05b')
    version('4.12.00', sha256='353f318db3c864fb338ae60a5327dd0db8de3e527bb8c6f600952d3181520f04')
    version('4.11.02', sha256='17f14ce8ef8ad7c4bf17be1e0ad9b457142d448f7eafaac1d387a7c627569041')
    version('MVP1a', branch='feature/Spack-MVP1a', git=git_base, get_full_repo=True)
    version('MVP', branch='feature/for_spack', git=git_base, get_full_repo=True)
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

    def setup_build_environment(self, spack_env):
        # Path for tests.
        spack_env.prepend_path('PATH', os.path.join(self.build_directory, 'bin'))
        # Cleanup
        sanitize_environments(spack_env)

    def setup_dependent_build_environment(self, spack_env, dependent_spec):
        # Binaries.
        spack_env.prepend_path('PATH', self.prefix.bin)
        spack_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)

    def setup_dependent_run_environment(self, run_env, dependent_spec):
        # Binaries.
        run_env.prepend_path('PATH', self.prefix.bin)
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)

    @run_after('install')
    def rename_README(self):
        import os
        if os.path.exists(join_path(self.spec.prefix, "README")):
            os.rename( join_path(self.spec.prefix, "README"),
                       join_path(self.spec.prefix, "README_%s"%self.spec.name))
