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


class Art(CMakePackage):
    """The eponymous package of the art suite; art is an event-processing
    framework for particle physics experiments.
    """

    homepage = 'https://art.fnal.gov/'
    git_base = 'https://github.com/art-framework-suite/art.git'
    url = 'https://github.com/art-framework-suite/art/archive/refs/tags/v3_09_01.tar.gz'
    list_url = 'https://api.github.com/repos/art-framework-suite/art/tags'

    version('3.09.03', sha256='f185fecd5593217185d2852d2ecf0a818326e7b4784180237461316b1c11f60d')
    version('3.09.02', sha256='76ac3cd3de86c2b935ba6c32c3e4524d607b489e5ca2d3f10905010337144d6c')
    version('3.09.01', sha256='f0039080405b27b798cbdef0948af725ab4efa27f0069f8cc27b4312d5ad6314')
    version('MVP1a', branch='feature/Spack-MVP1a', git=git_base, preferred=True)
    version('MVP', branch='feature/for_spack', git=git_base)
    version('develop', branch='develop', git=git_base)

    def url_for_version(self, version):
        url = 'https://github.com/art-framework-suite/{0}/archive/v{1}.tar.gz'
        return url.format(self.name, version.underscored)

    def fetch_remote_versions(self, concurrency=None):
        # FIXME: probably want to deal with pagination here (see
        #        https://docs.github.com/en/rest/guides/traversing-with-pagination)
        #        and possible error conditions like GitHub's rate
        #        limiting.
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
    depends_on('cmake@3.4:', type='build')
    depends_on('cetmodules', type='build')
    depends_on('catch2@2.3.0:', type='build')

    # Build and link dependencies.
    depends_on('clhep')
    depends_on('boost')
    depends_on('canvas')
    depends_on('cetlib')
    depends_on('cetlib-except')
    depends_on('fhicl-cpp')
    depends_on('hep-concurrency')
    depends_on('messagefacility')
    depends_on('tbb')
    depends_on('root+python')
    depends_on('sqlite@3.8.2:')
    depends_on('perl')
    depends_on('range-v3', when="@3.04.00:")
    depends_on('rapidjson', when='@3.06:')

    patch('art.external_rapidjson.patch',when='@3.06:3.09.01')
    #patch('art.ScheduleID.patch',when='@develop')
    #patch('art.ScheduleID.patch',when='@3.06:')

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
        # Cleaup.
        sanitize_environments(spack_env, run_env)
        spack_env.set("ART_DIR",self.prefix)
        run_env.set("ART_DIR",self.prefix)
        spack_env.set("ART_VERSION",str(self.version))
        run_env.set("ART_VERSION",str(self.version))

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        # Binaries.
        spack_env.prepend_path('PATH', self.prefix.bin)
        run_env.prepend_path('PATH', self.prefix.bin)
        # Ensure we can find plugin libraries.
        spack_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        run_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        # Ensure Root can find headers for autoparsing.
        spack_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        # Perl modules.
        spack_env.prepend_path('PERL5LIB', os.path.join(self.prefix, 'perllib'))
        run_env.prepend_path('PERL5LIB', os.path.join(self.prefix, 'perllib'))
        # Cleanup.
        sanitize_environments(spack_env, run_env)
        spack_env.set("ART_DIR",self.prefix)
        run_env.set("ART_DIR",self.prefix)

    @run_after('install')
    def rename_README(self):
        import os
        if os.path.exists(join_path(self.spec.prefix, "README")):
            os.rename( join_path(self.spec.prefix, "README"),
                   join_path(self.spec.prefix, "README_%s"%self.spec.name))
