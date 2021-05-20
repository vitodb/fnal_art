# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import sys
import os
libdir="%s/var/spack/repos/fnal_art/lib" % os.environ["SPACK_ROOT"]
if not libdir in sys.path:
    sys.path.append(libdir)



def patcher(x):
    cetmodules_20_migrator(".","artg4tk","9.07.01")

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
    git_base = 'https://cdcvs.fnal.gov/projects/art'
    url = 'https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/art.v3_0_2.tbz2'

    version('MVP1a', branch='feature/Spack-MVP1a',
            git=git_base, preferred=True)
    version('MVP', branch='feature/for_spack', git=git_base, get_full_repo=True)
    version('develop', branch='develop', git=git_base, get_full_repo=True)
    version('v20_6-branch', branch='v2_06-branch', git=git_base, get_full_repo=True)
    version('3.02.03', tag='v3_02_03', git=git_base, get_full_repo=True)
    version('3.02.04', tag='v3_02_04', git=git_base, get_full_repo=True)
    version('3.02.05', tag='v3_02_05', git=git_base, get_full_repo=True)
    version('3.02.06', tag='v3_02_06', git=git_base, get_full_repo=True)
    version('3.03.01', tag='v3_03_01', git=git_base, get_full_repo=True)
    version('3.02.03', tag='v3_02_03', git=git_base, get_full_repo=True)
    version('3.02.04', tag='v3_02_04', git=git_base, get_full_repo=True)
    version('3.02.05', tag='v3_02_05', git=git_base, get_full_repo=True)
    version('3.02.06', tag='v3_02_06', git=git_base, get_full_repo=True)
    version('3.03.01', tag='v3_03_01', git=git_base, get_full_repo=True)
    version('3.04.00', tag='v3_04_00', git=git_base, get_full_repo=True)
    version('3.08.00', tag='v3_08_00', git=git_base, get_full_repo=True)
    version('3.08.00', tag='v3_08_00', git=git_base, get_full_repo=True)

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

    patch('art.external_rapidjson.patch',when='@3.06:')
    #patch('art.ScheduleID.patch',when='@develop')
    #patch('art.ScheduleID.patch',when='@3.06:')

    if 'SPACKDEV_GENERATOR' in os.environ:
        generator = os.environ['SPACKDEV_GENERATOR']
        if generator.endswith('Ninja'):
            depends_on('ninja', type='build')

    def url_for_version(self, version):
        url = 'https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/{0}.v{1}.tbz2'
        return url.format(self.name, version.underscored)

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
        os.rename( join_path(self.spec.prefix, "README"),
                   join_path(self.spec.prefix, "README_%s"%self.spec.name))
