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
    version('2.10.01', git='http://cdcvs.fnal.gov/projects/ifdh-art/ifdh_art.git', tag='v2_10_01')
    version('2.10.00', git='http://cdcvs.fnal.gov/projects/ifdh-art/ifdh_art.git', tag='v2_10_00')

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
    depends_on('cetmodules@1.02.03:', type='build')

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value)               ]
        return args

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        # Ensure we can find plugin libraries.
        spack_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        run_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        spack_env.prepend_path('PATH', self.prefix.bin)
        run_env.prepend_path('PATH', self.prefix.bin)
    patch('ifdh_art.unups.patch')
