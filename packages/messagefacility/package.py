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


class Messagefacility(CMakePackage):
    """A configurable message logging facility for the art suite."""

    homepage = 'https://art.fnal.gov/'
    git_base = 'https://github.com/art-framework-suite/messagefacility.git'
    url = 'https://github.com/art-framework-suite/messagefacility/archive/refs/tags/v3_09_01.tar.gz'
    list_url = 'https://api.github.com/repos/art-framework-suite/messagefacility/tags'

    version('2.08.04', sha256='dcf71449b0f73b01e2d32d1dc5b8eefa09a4462d1c766902d916ed6869b6c682')
    version('2.08.03', sha256='bf10264d94e77e14c488e02107e36e676615fa12c9e2795c4caccf0c913ba7b9')
    version('2.08.02', sha256='677980a394395943b730f561118534c5d6c2ba1315de2a887a7eb597a9f43803')
    version('2.08.01', sha256='850672115b949df92fc87b2b439e53bf51ce9a3fee6a346c16d9b1fe75aeb759')
    version('2.08.00', sha256='a2c833071dfe7538c40a0024d15f19ba062fd5f56b26f83f5cb739c12ff860ec')
    version('2.07.03', sha256='950d9ac6702d1878c4b7d51604d870f74b4ccd289a2166a3f5acf143a50863e0')
    version('2.07.02', sha256='4ea94b36291a1d23f071e63ea011ce30bf7137c61bb9d067be8f84915fe47789')
    version('2.07.01', sha256='68061ccaffc49d94c8368f2a7bf8e33ea81bded1df75a7dd806365af34248544')
    version('2.07.00', sha256='cdcbcf649b3d90fcfeeb6a11bfb09fe72fda3eb93120042b9a91a599f5baf9c2')
    version('2.06.02', sha256='8b53be1e152d2bc711cb8d5229e296e8f2b5bb67a158d8d523a93562a9b0110e')
    version('MVP1a', branch='archive/feature/Spack-MVP1a', git=git_base, get_full_repo=True)
    version('MVP', branch='archive/feature/for_spack', git=git_base, get_full_repo=True)
    version('v2_06-branch', branch='v2_06-branch', git=git_base, get_full_repo=True)
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
    depends_on('catch2@2.3.0:', type='build')
    depends_on('py-pybind11', type='build')

    # Build / link dependencies.
    depends_on('cetlib-except')
    depends_on('cetlib')
    depends_on('boost')
    depends_on('fhicl-cpp')
    depends_on('hep-concurrency')
    depends_on('sqlite', when='@MVP')
    depends_on('perl')
    depends_on('tbb', when='@MVP')

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
        # Binaries.
        spack_env.prepend_path('PATH',
                               os.path.join(self.build_directory, 'bin'))
        # Ensure we can find plugin libraries.
        spack_env.prepend_path('CET_PLUGIN_PATH',
                               os.path.join(self.build_directory, 'lib'))
        # Perl modules.
        spack_env.prepend_path('PERL5LIB',
                               os.path.join(self.build_directory, 'perllib'))
        # Cleaup.
        sanitize_environments(spack_env)

    def setup_run_environment(self, run_env):
        # Ensure we can find plugin libraries.
        run_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        # Perl modules.
        run_env.prepend_path('PERL5LIB', os.path.join(self.prefix, 'perllib'))
        # Cleaup.
        sanitize_environments(run_env)

    def setup_dependent_build_environment(self, spack_env, dependent_spec):
        # Binaries.
        spack_env.prepend_path('PATH', self.prefix.bin)
        spack_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        # Ensure we can find plugin libraries.
        spack_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        # Perl modules.
        spack_env.prepend_path('PERL5LIB', os.path.join(self.prefix, 'perllib'))
        # Cleanup.
        sanitize_environments(spack_env)

    def setup_dependent_run_environment(self, run_env, dependent_spec):
        # Binaries.
        run_env.prepend_path('PATH', self.prefix.bin)
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        # Ensure we can find plugin libraries.
        run_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        # Perl modules.
        run_env.prepend_path('PERL5LIB', os.path.join(self.prefix, 'perllib'))
        # Cleanup.
        sanitize_environments(run_env)

    @run_after('install')
    def rename_README(self):
        import os
        if os.path.exists(join_path(self.spec.prefix, "README")):
            os.rename( join_path(self.spec.prefix, "README"),
                       join_path(self.spec.prefix, "README_%s"%self.spec.name))
