# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dk2nudata(Package):
    """This package consolidates the disparate formats of neutrino beam simulation "flux" files.
"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/dk2nu"
    url      = "http://cdcvs.fnal.gov/subversion/dk2nu/tags/v01_07_02"

    version('01_07_02', svn="http://cdcvs.fnal.gov/subversion/dk2nu/tags/v01_07_02")

    depends_on('cmake', type='build')
    depends_on('root')
    depends_on('intel-tbb')
    depends_on('libxml2')
    depends_on('log4cpp')
 
    variant('cxxstd',
            default='17',
            values=('default', '98', '11', '14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    parallel = False

    def set_cxxstdflag(self):
        cxxstd = self.spec.variants['cxxstd'].value
        cxxstdflag = ''
        if cxxstd == '98':
            cxxstdflag = self.compiler.cxx98_flag
        elif cxxstd == '11':
            cxxstdflag = self.compiler.cxx11_flag
        elif cxxstd == '14':
            cxxstdflag = self.compiler.cxx14_flag
        elif cxxstd == '17':
            cxxstdflag = self.compiler.cxx17_flag
        elif cxxstd == 'default':
            pass
        else:
            # The user has selected a (new?) legal value that we've
            # forgotten to deal with here.
            tty.die(
                "INTERNAL ERROR: cannot accommodate unexpected variant ",
                "cxxstd={0}".format(spec.variants['cxxstd'].value))
        return cxxstdflag


    def install(self, spec, prefix):
        args = ['-DCMAKE_INSTALL_PREFIX=%s'%prefix,
                '-DWITH_GENIE=OFF',
                '-DTBB_LIBRARY=%s'%self.spec['intel-tbb'].prefix.lib,
                '%s/dk2nu' % self.stage.source_path]
        cmake = which('cmake')
        with working_dir('%s/spack-build'%self.stage.path, create=True):
            cmake(*args)
            make('VERBOSE=t', 'all','install')

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('DK2NUDATA_INC',dspec['dk2nudata'].prefix.include)
        spack_env.set('DK2NUDATA_LIB', dspec['dk2nudata'].prefix.lib)
