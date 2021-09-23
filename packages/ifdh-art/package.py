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



class IfdhArt(CMakePackage):
    """The ifdh_art package provides ART service access to the libraries 
from the ifdhc package."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/ifdh-art/wiki"
    url      = "https://cdcvs.fnal.gov/projects/ifdh-art/ifdh_art.git"

    version('2.12.04',  git='https://cdcvs.fnal.gov/projects/ifdh-art/ifdh_art.git', tag='v2_12_02_01', get_full_repo=True)
    version('2.12.02.01',  git='https://cdcvs.fnal.gov/projects/ifdh-art/ifdh_art.git', tag='v2_12_02_01', get_full_repo=True)
    version('2.11.05',  git='https://cdcvs.fnal.gov/projects/ifdh-art/ifdh_art.git', tag='v2_11_05', get_full_repo=True)

    version('develop', git=url, branch='develop', get_full_repo=True)

    version('MVP1a', git='https://cdcvs.fnal.gov/projects/ifdh-art/ifdh_art.git', branch='feature/Spack-MVP1a')
    version('2.10.07',  git='https://cdcvs.fnal.gov/projects/ifdh-art/ifdh_art.git', tag='v2_10_07', get_full_repo=True)
    version('2.10.02',  git='https://cdcvs.fnal.gov/projects/ifdh-art/ifdh_art.git', tag='v2_10_02', get_full_repo=True)
    version('2.10.01',  git='https://cdcvs.fnal.gov/projects/ifdh-art/ifdh_art.git', tag='v2_10_01', get_full_repo=True)
    version('2.10.00',  git='https://cdcvs.fnal.gov/projects/ifdh-art/ifdh_art.git', tag='v2_10_00', get_full_repo=True)
    version('2.10.02',  git='https://cdcvs.fnal.gov/projects/ifdh-art/ifdh_art.git', tag='v2_10_02', get_full_repo=True)
    version('2.10.04',  git='https://cdcvs.fnal.gov/projects/ifdh-art/ifdh_art.git', tag='v2_10_04', get_full_repo=True)

    patch('cetmodules2.patch', when='@develop')

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    depends_on('art')
    depends_on('ifdhc')
    depends_on('ifbeam')
    depends_on('nucondb')
    depends_on('libwda')
    depends_on('cetmodules', type='build')
    depends_on('cetbuildtools', type='build')


    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value)               ]
        return args

    def setup_build_environment(self, spack_env):
        spack_env.set('CETBUILDTOOLS_VERSION', self.spec['cetmodules'].version)
        spack_env.set('CETBUILDTOOLS_DIR', self.spec['cetmodules'].prefix)

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        # Ensure we can find plugin libraries.
        spack_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        run_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        spack_env.prepend_path('PATH', self.prefix.bin)
        run_env.prepend_path('PATH', self.prefix.bin)


    @run_after('install')
    def rename_README(self):
        import os
        if os.path.exists(join_path(self.spec.prefix, "README")):
            os.rename( join_path(self.spec.prefix, "README"),
                       join_path(self.spec.prefix, "README_%s"%self.spec.name))
