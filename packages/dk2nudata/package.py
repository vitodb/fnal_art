# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dk2nudata(CMakePackage):
    """This package consolidates the disparate formats of neutrino beam simulation "flux" files.
"""

    homepage = "http://cdcvs.fnal.gov/redmine/projects/dk2nu"
    url      = "http://cdcvs.fnal.gov/subversion/dk2nu/tags/v01_07_02"

    version('01_07_02', svn="http://cdcvs.fnal.gov/subversion/dk2nu/tags/v01_07_02")

    depends_on('cmake', type='build')
    depends_on('root')
    depends_on('intel-tbb')
    depends_on('libxml2')
    depends_on('log4cpp')
 
    parallel = False


    def cmake_args(self):
        prefix=self.spec.prefix
        args = [
                '-DWITH_GENIE=OFF',
                '-DTBB_LIBRARY=%s'%self.spec['intel-tbb'].prefix.lib,
                '%s/dk2nu' % self.stage.source_path]
        return args

    def build(self, spec, prefix):
        with working_dir('%s/spack-build'%self.stage.path, create=True):
            make('VERBOSE=t', 'all')

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        # Ensure we can find plugin libraries.
        spack_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        run_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
