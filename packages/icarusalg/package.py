# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import sys
import os

def sanitize_environments(*args):
    for env in args:
        for var in ('PATH', 'CET_PLUGIN_PATH',
                    'LD_LIBRARY_PATH', 'DYLD_LIBRARY_PATH', 'LIBRARY_PATH',
                    'CMAKE_PREFIX_PATH', 'ROOT_INCLUDE_PATH'):
            env.prune_duplicate_paths(var)
            env.deprioritize_system_paths(var)


class Icarusalg(CMakePackage):
    """SignalProcessing for icarus
    framework for particle physics experiments.
    """

    homepage = 'https://cdcvs.fnal.gov/redmine/projects/icarusalg'
    #git_base = 'https://cdcvs.fnal.gov/projects/icarusalg'
    git_base = 'https://github.com/SBNSoftware/icarusalg.git'

    version('develop', branch='develop', git='https://github.com/gartung/icarusalg.git', get_full_repo=True)
    version('09.06.00', tag='v09_06_00', git=git_base, get_full_repo=True)
    version('09.07.00', tag='v09_07_00', git=git_base, get_full_repo=True)
    version('09.08.00', tag='v09_08_00', git=git_base, get_full_repo=True)
    version('09.09.00', tag='v09_09_00', git=git_base, get_full_repo=True)
    version('09.09.01', tag='v09_09_01', git=git_base, get_full_repo=True)
    version('09.10.01', tag='v09_10_01', git=git_base, get_full_repo=True)

    patch('mwm.patch', when='@09.28.01')


    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    # Build-only dependencies.
    depends_on('cmake@3.11:')
    depends_on('cetmodules', type='build')

    # Build and link dependencies.
    depends_on('clhep', type=('build','run'))
    depends_on('gsl', type=('build','run'))
    depends_on('cppgsl', type=('build','run'))
    depends_on('lardataobj', type=('build','run'))
    depends_on('larcoreobj', type=('build','run'))
    depends_on('lardataalg', type=('build','run'))
    depends_on('larcorealg', type=('build','run'))
    depends_on('nusimdata', type=('build','run'))
    depends_on('canvas-root-io', type=('build','run'))
    depends_on('canvas', type=('build','run'))
    depends_on('cetlib-except', type=('build','run'))
    depends_on('cetlib', type=('build','run'))
    depends_on('gallery', type=('build','run'))
    depends_on('messagefacility', type=('build','run'))
    depends_on('boost', type=('build','run'))
    depends_on('tbb', type=('build','run'))
    depends_on('range-v3', type=('build','run'))
    depends_on('hep-concurrency', type=('build','run'))


    if 'SPACKDEV_GENERATOR' in os.environ:
        generator = os.environ['SPACKDEV_GENERATOR']
        if generator.endswith('Ninja'):
            depends_on('ninja', type='build')

    def url_for_version(self, version):
        #url = 'https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/{0}.v{1}.tbz2'
        url = 'https://github.com/SBNSoftware/{0}/archive/v{1}.tar.gz'
        return url.format(self.name, version.underscored)

    def cmake_args(self):
        # Set CMake args.
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value),
                '-DCPPGSL_INC={0}'.
                format(self.spec['cppgsl'].prefix.include)]
        return args

    def setup_environment(self, spack_env, run_env):

        # easier to set these than patch the CMakeLists.txts for now
        # but there sure are a lot of them...
        spack_env.set('BOOST_INC',self.spec['boost'].prefix.include)
        spack_env.set('CANVAS_INC',self.spec['canvas'].prefix.include)
        spack_env.set('CANVAS_ROOT_IO_INC',self.spec['canvas-root-io'].prefix.include)
        spack_env.set('CETLIB_EXCEPT_INC',self.spec['cetlib-except'].prefix.include)
        spack_env.set('CETLIB_INC',self.spec['cetlib'].prefix.include)
        spack_env.set('CLHEP_INC',self.spec['clhep'].prefix.include)
        spack_env.set('FHICLCPP_INC',self.spec['fhicl-cpp'].prefix.include)
        spack_env.set('GALLERY_INC',self.spec['gallery'].prefix.include)
        spack_env.set('ICARUSALG_INC', self.spec.prefix.include)
        spack_env.set('HEP_CONCURRENCY_INC',self.spec['hep-concurrency'].prefix.include)
        spack_env.set('LARCOREALG_INC',self.spec['larcorealg'].prefix.include)
        spack_env.set('LARCOREOBJ_INC',self.spec['larcoreobj'].prefix.include)
        spack_env.set('LARDATAALG_INC',self.spec['lardataalg'].prefix.include)
        spack_env.set('LARDATAOBJ_INC',self.spec['lardataobj'].prefix.include)
        spack_env.set('MESSAGEFACILITY_INC',self.spec['messagefacility'].prefix.include)
        spack_env.set('NUSIMDATA_INC',self.spec['nusimdata'].prefix.include)
        spack_env.set('ROOT_INC',self.spec['root'].prefix.include)

        spack_env.prepend_path('LD_LIBRARY_PATH', str(self.spec['root'].prefix.lib))
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
