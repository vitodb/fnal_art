# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os

import sys
libdir="%s/var/spack/repos/fnal_art/lib" % os.environ["SPACK_ROOT"]
if not libdir in sys.path:
    sys.path.append(libdir)
from cetmodules_patcher import cetmodules_dir_patcher

def patcher(x):
    cetmodules_dir_patcher(".","nutools","3.06.01")

def sanitize_environments(*args):
    for env in args:
        for var in ('PATH', 'CET_PLUGIN_PATH',
                    'LD_LIBRARY_PATH', 'DYLD_LIBRARY_PATH', 'LIBRARY_PATH',
                    'CMAKE_PREFIX_PATH', 'ROOT_INCLUDE_PATH'):
            env.prune_duplicate_paths(var)
            env.deprioritize_system_paths(var)


class Nutools(CMakePackage):
    """Nutools"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/nutools/wiki"
    url      = "https://cdcvs.fnal.gov/projects/nutools/"

    version('MVP1a', git="https://cdcvs.fnal.gov/projects/nutools", branch='feature/MVP1a')
    version('3.04.02', tag='v3_04_02', git="https://cdcvs.fnal.gov/projects/nutools")
    version('3.04.03', tag='v3_04_03', git="https://cdcvs.fnal.gov/projects/nutools")
    version('3.05.00', tag='v3_05_00', git="https://cdcvs.fnal.gov/projects/nutools")
    version('3.05.01', tag='v3_05_01', git="https://cdcvs.fnal.gov/projects/nutools")
    version('3.06.00', tag='v3_06_00', git="https://cdcvs.fnal.gov/projects/nutools")
    version('3.06.01', tag='v3_06_01', git="https://cdcvs.fnal.gov/projects/nutools")
    version('3.06.02', tag='v3_06_02', git="https://cdcvs.fnal.gov/projects/nutools")
    version('3.06.06', tag='v3_06_06', git="https://cdcvs.fnal.gov/projects/nutools")

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    patch('nutools.unups.patch')

    depends_on('cetmodules', type='build')
    depends_on('art-root-io')
    depends_on('perl')
    depends_on('pythia6')
    depends_on('libwda')
    depends_on('postgresql')
    depends_on('libxml2')
    depends_on('nusimdata')
    depends_on('dk2nugenie')
    depends_on('genie')
    depends_on('geant4~data')
    depends_on('xerces-c')
    depends_on('cry')
    depends_on('ifdh-art')
    depends_on('ifdhc')
    depends_on('ifbeam')
    depends_on('nucondb')
    depends_on('libwda')


    def url_for_version(self, version):
        url = 'https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/{0}.v{1}.tbz2'
        return url.format(self.name, version.underscored)

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value),
                '-DCRYHOME={0}'.format(self.spec['cry'].prefix),
                '-DGENIE_INC={0}'.format(self.spec['genie'].prefix),
               ]
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

    def setup_dependent_environment(self, spack_env, run_env, dspec):
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
