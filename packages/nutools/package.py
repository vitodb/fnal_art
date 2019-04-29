# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


def sanitize_environments(*args):
    for env in args:
        for var in ('PATH', 'CET_PLUGIN_PATH',
                    'LD_LIBRARY_PATH', 'DYLD_LIBRARY_PATH', 'LIBRARY_PATH',
                    'CMAKE_PREFIX_PATH', 'ROOT_INCLUDE_PATH'):
            env.prune_duplicate_paths(var)
            env.deprioritize_system_paths(var)


class Nutools(CMakePackage):
    """Nutools"""

    homepage = "http://cdcvs.fnal.gov/redmine/projects/nutools/wiki"
    url      = "http://cdcvs.fnal.gov/projects/nutools/"

    version('MVP1a', git="http://cdcvs.fnal.gov/projects/nutools", branch='feature/MVP1a')

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    depends_on('cetmodules', type='build')
    depends_on('art-root-io')
    depends_on('perl')
    depends_on('pythia6')
    depends_on('libwda')
    depends_on('postgresql')
    depends_on('libxml2')
    depends_on('nusimdata')
    depends_on('dk2nugenie')
    depends_on('geant4~data')
    depends_on('xerces-c')
    depends_on('cry')
    depends_on('ifdh-art')
    depends_on('ifdhc')
    depends_on('ifbeam')
    depends_on('nucondb')
    depends_on('libwda')


    def url_for_version(self, version):
        url = 'http://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/{0}.v{1}.tbz2'
        return url.format(self.name, version.underscored)


    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value),
                '-DROOTSYS={0}'.
                format(self.spec['root'].prefix),
                '-DGENIE_VERSION=v{0}'.
                format(self.spec['genie'].version.underscored),
                '-DGENIE_INC={0}'.
                format(self.spec['genie'].prefix.include),
                '-DCRYHOME={0}/src'.
                format(self.spec['cry'].prefix),
                '-DLOG4CPP_INC={0}'.
                format(self.spec['log4cpp'].prefix.include),
                '-DIFDH_ART_INC={0}'.
                format(self.spec['ifdh-art'].prefix.include),
                '-DIFDHC_INC={0}/inc'.
                format(self.spec['ifdhc'].prefix),
                '-DDK2NUGENIE_INC={0}'.
                format(self.spec['dk2nugenie'].prefix.include),
                '-DDK2NUDATA_INC={0}'.
                format(self.spec['dk2nudata'].prefix.include),
                '-DXERCES_C_INC={0}'.
                format(self.spec['xerces-c'].prefix.include),
                '-DLIBXML2_INC={0}'.
                format(self.spec['libxml2'].prefix.include),
                '-DLIBWDA_INC={0}/inc'.
                format(self.spec['libwda'].prefix),
               ] 
        return args

    def setup_environment(self, spack_env, run_env):
        # Binaries.
        spack_env.prepend_path('PATH',
                               join_path(self.build_directory, 'bin'))
        # Ensure we can find plugin libraries.
        spack_env.prepend_path('CET_PLUGIN_PATH',
                               join_path(self.build_directory, 'lib'))
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
                               join_path(self.build_directory, 'perllib'))
        run_env.prepend_path('PERL5LIB', join_path(self.prefix, 'perllib'))
        # Cleaup.
        sanitize_environments(spack_env, run_env)

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('NUTOOLS_INC',self.prefix.include)
        spack_env.set('NUTOOLS_LIB', self.prefix.lib)
        # Ensure we can find plugin libraries.
        spack_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        run_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        spack_env.prepend_path('PATH', self.prefix.bin)
        run_env.prepend_path('PATH', self.prefix.bin)
        spack_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        spack_env.append_path('FHICL_FILE_PATH','{0}/job'.format(self.prefix))
        run_env.append_path('FHICL_FILE_PATH','{0}/job'.format(self.prefix))
        spack_env.append_path('FW_SEARCH_PATH','{0}/gdml'.format(self.prefix))
        run_env.append_path('FW_SEARCH_PATH','{0}/gdml'.format(self.prefix))
        sanitize_environments(spack_env, run_env)
