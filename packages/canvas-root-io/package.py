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


class CanvasRootIo(CMakePackage):
    """A Root I/O library for the art suite."""

    homepage = 'https://art.fnal.gov/'
    git_base = 'https://github.com/art-framework-suite/canvas-root-io.git'
    url = 'https://github.com/art-framework-suite/canvas-root-io/archive/refs/tags/v3_09_01.tar.gz'
    list_url = 'https://api.github.com/repos/art-framework-suite/canvas-root-io/tags'

    version('1.09.05', sha256='50f8d4375f3672934192ad997b74e169e598d45823f856ac1e6683215f49b8ea')
    version('1.09.04', sha256='cb854b4fdc72be24856886d985f96ceb3b0049729df0b4a11fb501ff7c48847b')
    version('1.09.03', sha256='80214367dcd9bcaf6542c28d2a047f149174d11efe42b7f5456adff30a3afde9')
    version('1.09.02', sha256='a19b1df354d38d23360c7ce7dd24c335c815823a5ea755cc1a3621adffe86474')
    version('1.09.01', sha256='aeca3255688866096edc3f730fb2ba12bf98b512065d9b9aa73cca5480ff28a0')
    version('1.09.00', sha256='032b293971f9c8fe02f786e50526116e7a318bab80da5d0119808f73ae6acdde')
    version('1.08.00', sha256='62fb11533fbd784cacee73b9a2780b1f387e0a5124a85dc825576860de4fb4cc')
    version('1.07.03', sha256='9c3b348f41824208741619d6886f5105706cc0c37272acd18df96df37b958c2e')
    version('1.07.02', sha256='4083dbbd38ed77193df0f22cdca64fff5e7225ac912637c782ceceb4047e8687')
    version('1.07.01', sha256='09b11617c19388091184649de0724b1cd97b0d6d336534f48d52f400140a8e86')
    version('MVP1a', branch='archive/feature/Spack-MVP1a', get_full_repo=True, git=git_base)
    version('MVP', branch='archive/feature/for_spack', get_full_repo=True, git=git_base)
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
    depends_on('clhep')
    depends_on('root+python')
    depends_on('boost')
    depends_on('canvas')
    depends_on('cetlib')
    depends_on('cetlib-except')
    depends_on('fhicl-cpp')
    depends_on('hep-concurrency', when='@MVP1a')
    depends_on('messagefacility')
    depends_on('tbb', when='@MVP')

    if 'SPACKDEV_GENERATOR' in os.environ:
        generator = os.environ['SPACKDEV_GENERATOR']
        if generator.endswith('Ninja'):
            depends_on('ninja', type='build')

    def build(self, spec, prefix):
        """Make the build targets"""
        with working_dir(self.build_directory):
            if self.generator == 'Unix Makefiles':
                try:
                    make(*self.build_targets) 
                except:
                    make(*self.build_targets) 
            elif self.generator == 'Ninja':
                self.build_targets.append("-v")
                try:
                    ninja(*self.build_targets)
                except:
                    ninja(*self.build_targets)


    def cmake_args(self):
        # Set CMake args.
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value),
                '-DCANVAS_ROOT_IO_INC={0}'.
                format(os.path.join(self.build_directory, 'include')) ]
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
        spack_env.set("CANVAS_ROOT_IO_DIR", self.prefix)

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
        run_env.set("CANVAS_ROOT_IO_DIR", self.prefix)

    def setup_dependent_build_environment(self, spack_env, dependent_spec):
        # Ensure we can find plugin libraries.
        spack_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        # Ensure Root can find headers for autoparsing.
        spack_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        # Cleanup.
        sanitize_environments(spack_env)
        spack_env.set("CANVAS_ROOT_IO_DIR", self.prefix)

    def setup_dependent_run_environment(self, run_env, dependent_spec):
        # Ensure we can find plugin libraries.
        run_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        # Ensure Root can find headers for autoparsing.
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        # Cleanup.
        sanitize_environments(run_env)
        run_env.set("CANVAS_ROOT_IO_DIR", self.prefix)

    @run_after('install')
    def rename_README(self):
        import os
        if os.path.exists(join_path(self.spec.prefix, "README")):
            os.rename( join_path(self.spec.prefix, "README"),
                       join_path(self.spec.prefix, "README_%s"%self.spec.name))
