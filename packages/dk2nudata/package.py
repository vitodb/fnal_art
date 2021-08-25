# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import sys


class Dk2nudata(CMakePackage):
    """This package consolidates the disparate formats of neutrino beam simulation "flux" files.
"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/dk2nu"
    url      = "https://cdcvs.fnal.gov/subversion/dk2nu/tags/v01_07_02"

    version('01.10.00', svn="https://cdcvs.fnal.gov/subversion/dk2nu/tags/v01_10_00")
    version('01.09.02', svn="https://cdcvs.fnal.gov/subversion/dk2nu/tags/v01_09_02")
    version('01.09.01', svn="https://cdcvs.fnal.gov/subversion/dk2nu/tags/v01_09_01")
    version('01.09.00', svn="https://cdcvs.fnal.gov/subversion/dk2nu/tags/v01_09_00")
    version('01.08.00', svn="https://cdcvs.fnal.gov/subversion/dk2nu/tags/v01_08_00")
    version('01.07.02', svn="https://cdcvs.fnal.gov/subversion/dk2nu/tags/v01_07_02")
    version('01.08.00',  svn="https://cdcvs.fnal.gov/subversion/dk2nu/tags/v01_08_00")

    # Variant is still important even though it's not passed to compiler
    # flags (use of ROOT, etc.).
    variant('cxxstd',
            default='11',
            values=('11', '14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    depends_on('cmake', type='build')
    depends_on('root')
    depends_on('tbb')
    depends_on('libxml2')
    depends_on('log4cpp')
 
    parallel = False

    root_cmakelists_dir = 'dk2nu'
    
    def cmake_args(self):
        prefix=self.spec.prefix
        args = [
                '-DWITH_GENIE=OFF',
                '-DTBB_LIBRARY=%s/libtbb.so'%self.spec['intel-tbb'].prefix.lib]
        return args

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        # Ensure we can find plugin libraries.
        spack_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        run_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        spack_env.set('DK2NUDATA_LIB', self.prefix.lib)

