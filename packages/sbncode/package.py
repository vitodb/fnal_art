# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import sys


def sanitize_environments(*args):
    for env in args:
        for var in ('PATH', 'CET_PLUGIN_PATH',
                    'LD_LIBRARY_PATH', 'DYLD_LIBRARY_PATH', 'LIBRARY_PATH',
                    'CMAKE_PREFIX_PATH', 'ROOT_INCLUDE_PATH'):
            env.prune_duplicate_paths(var)
            env.deprioritize_system_paths(var)


class Sbncode(CMakePackage):
    """The eponymous package of the Sbn experiment
    framework for particle physics experiments.
    """

    homepage = 'https://cdcvs.fnal.gov/redmine/projects/sbncode'
    url      = 'https://github.com/SBNSoftware/sbncode/archive/refs/tags/v09_35_01.tar.gz'
    git_base = 'https://github.com/SBNSoftware/sbncode.git'
    list_url = 'https://api.github.com/repos/SBNSoftware/sbncode/tags'

    version('develop', branch='develop', git=git_base, get_full_repo=True)
    version('09.35.00', sha256='6dc753dcc24e9583a261a70da99a1275835b70091c816dbbb0ddee60ad698686')

    patch('v09_35_00.patch', when='@09.35.00')

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    # Build-only dependencies.
    depends_on('cmake@3.11:')
    depends_on('cetmodules', type='build')
    depends_on('cetbuildtools', type='build')

    # Build and link dependencies.
    depends_on('artdaq-core', type=('build','run'))
    depends_on('art-root-io', type=('build','run'))
    depends_on('art', type=('build','run'))
    depends_on('artdaq-core', type=('build','run'))
    depends_on('boost', type=('build','run'))
    depends_on('canvas-root-io', type=('build','run'))
    depends_on('canvas', type=('build','run'))
    depends_on('cetlib-except', type=('build','run'))
    depends_on('clhep', type=('build','run'))
    depends_on('cppgsl', type=('build','run'))
    depends_on('eigen', type=('build','run'))
    depends_on('fftw', type=('build','run'))
    depends_on('hep-concurrency', type=('build','run'))
    depends_on('ifdh-art', type=('build','run'))
    depends_on('tbb', type=('build','run'))
    depends_on('gsl', type=('build','run'))
    depends_on('geant4', type=('build','run'))
    depends_on('zlib', type=('build','run'))
    depends_on('xerces-c', type=('build','run'))
    depends_on('larana', type=('build','run'))
    depends_on('larcoreobj', type=('build','run'))
    depends_on('larcore', type=('build','run'))
    depends_on('lardataobj', type=('build','run'))
    depends_on('lardata', type=('build','run'))
    depends_on('larevt', type=('build','run'))
    depends_on('pandora', type=('build','run'))
    depends_on('larpandora', type=('build','run'))
    depends_on('larpandoracontent', type=('build','run'))
    depends_on('py-torch', type=('build','run'))
    depends_on('larreco', type=('build','run'))
    depends_on('larsim', type=('build','run'))
    depends_on('libwda', type=('build','run'))
    depends_on('marley', type=('build','run'))
    depends_on('nug4', type=('build','run'))
    depends_on('nugen', type=('build','run'))
    depends_on('genie', type=('build','run'))
    depends_on('ifdhc', type=('build','run'))
    depends_on('ifbeam', type=('build','run'))
    depends_on('libxml2', type=('build','run'))
    depends_on('nucondb', type=('build','run'))
    depends_on('nutools', type=('build','run'))
    depends_on('postgresql', type=('build','run'))
    depends_on('log4cpp', type=('build','run'))
    depends_on('range-v3', type=('build','run'))
    depends_on('sbnobj', type=('build','run'))
    depends_on('sbnanaobj', type=('build','run'))
    depends_on('sbndaq-artdaq-core', type=('build','run'))
    depends_on('sqlite', type=('build','run'))
    depends_on('trace', type=('build','run'))
    depends_on('dk2nudata', type=('build','run'))
    depends_on('dk2nugenie', type=('build','run'))

    if 'SPACKDEV_GENERATOR' in os.environ:
        generator = os.environ['SPACKDEV_GENERATOR']
        if generator.endswith('Ninja'):
            depends_on('ninja', type='build')

    def url_for_version(self, version):
        #url = 'https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/{0}.v{1}.tbz2'
        url = 'https://github.com/SBNSoftware/{0}/archive/v{1}.tar.gz'
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
                format(self.spec.variants['cxxstd'].value),
                '-DCMAKE_PREFIX_PATH={0}/lib/python{1}/site-packages/torch'
                 .format(self.spec['py-torch'].prefix, self.spec['python'].version.up_to(2)),
                '-DZLIB_ROOT={0}'.format(self.spec['zlib'].prefix),
                '-DIGNORE_ABSOLUTE_TRANSITIVE_DEPENDENCIES=1' ]
        return args

    def setup_build_environment(self, spack_env):
        spack_env.prepend_path('LD_LIBRARY_PATH', self.spec['root'].prefix.lib)
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
        spack_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        # Perl modules.
        spack_env.prepend_path('PERL5LIB',
                               os.path.join(self.build_directory, 'perllib'))
        # Cleaup.
        sanitize_environments(spack_env)

    def setup_run_environment(self, run_env):
        # Binaries.
        run_env.prepend_path('PATH',
                               os.path.join(self.build_directory, 'bin'))
        # Ensure we can find plugin libraries.
        run_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(root=False, cover='nodes', order='post',
                                    deptype=('link'), direction='children'):
            run_env.prepend_path('ROOT_INCLUDE_PATH',
                                 str(self.spec[d.name].prefix.include))
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        # Perl modules.
        run_env.prepend_path('PERL5LIB', os.path.join(self.prefix, 'perllib'))
        # Cleaup.
        sanitize_environments(run_env)

    def setup_dependent_build_environment(self, spack_env, dependent_spec):
        # Binaries.
        spack_env.prepend_path('PATH', self.prefix.bin)
        # Ensure we can find plugin libraries.
        spack_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        # Ensure Root can find headers for autoparsing.
        spack_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        # Perl modules.
        spack_env.prepend_path('PERL5LIB', os.path.join(self.prefix, 'perllib'))
        # Cleanup.
        sanitize_environments(spack_env)
 
    def setup_dependent_run_environment(self, run_env, dependent_spec):
        # Binaries.
        run_env.prepend_path('PATH', self.prefix.bin)
        # Ensure we can find plugin libraries.
        run_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        # Ensure Root can find headers for autoparsing.
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        # Perl modules.
        run_env.prepend_path('PERL5LIB', os.path.join(self.prefix, 'perllib'))
        # Cleanup.
        sanitize_environments(run_env)
