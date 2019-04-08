# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class IfdhArt(CMakePackage):
    """The ifdh_art package provides ART service access to the libraries 
from the ifdhc package."""

    homepage = "http://cdcvs.fnal.gov/redmine/projects/ifdh-art/wiki"
    url      = "http://cdcvs.fnal.gov/projects/ifdh-art/ifdh_art.git"

    version('MVP1a', git='http://cdcvs.fnal.gov/projects/ifdh-art/ifdh_art.git', branch='feature/Spack-MVP1a')

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

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value),
                '-DIFDHC_DIR={0}'.
                format(self.spec['ifdhc'].prefix),
                '-DIFBEAM_DIR={0}'.
                format(self.spec['ifbeam'].prefix),
                '-DNUCONDB_DIR={0}'.
                format(self.spec['nucondb'].prefix),
                '-DLIBWDA_DIR={0}'.
                format(self.spec['libwda'].prefix),
                '-Difdh_art_header_dir={0}'.
                format(self.spec.prefix.include),
               ]
        return args

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('IFDH_ART_FQ_DIR', '{0}'.format(self.prefix))
        spack_env.set('IFDH_ART_DIR', '{0}'.format(self.prefix))
        spack_env.set('IFDH_ART_INC', '{0}/ifdh-art/src'.format(self.prefix.share))
        spack_env.set('IFDH_ART_LIB', '{0}'.format(self.prefix.lib))
        # Ensure we can find plugin libraries.
        spack_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        run_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        spack_env.prepend_path('PATH', self.prefix.bin)
        run_env.prepend_path('PATH', self.prefix.bin)
        spack_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
