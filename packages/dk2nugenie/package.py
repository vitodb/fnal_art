# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Dk2nugenie(CMakePackage):
    """This package consolidates the disparate formats of neutrino beam simulation "flux" files.
"""
    homepage = "https://cdcvs.fnal.gov/redmine/projects/dk2nu"
    url      = "http://cdcvs.fnal.gov/subversion/dk2nu/tags/v01_07_02"

    version('01_07_02',  svn="http://cdcvs.fnal.gov/subversion/dk2nu/tags/v01_07_02")

    depends_on('cmake', type='build')
    depends_on('root')
    depends_on('libxml2')
    depends_on('log4cpp')
    depends_on('genie')
    depends_on('dk2nudata')

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
    

    def patch(self):
        patch('dk2nu.patch', when='^genie@3.00.00:', working_dir='v{0}'.format(self.version))
        cmakelists=FileFilter('{0}/dk2nu/genie/CMakeLists.txt'.format(self.stage.source_path))
        cmakelists.filter('\$\{GENIE\}/src', '${GENIE}/include/GENIE')
        cmakelists.filter('\$ENV', '$')
        cmakelists.filter('execute_process', '#execute_process')
    def cmake_args(self):
        prefix=self.prefix
        args = ['-DCMAKE_INSTALL_PREFIX=%s'%prefix,
                '-DGENIE_ONLY=ON',
                '-DTBB_LIBRARY=%s/libtbb.so'%self.spec['intel-tbb'].prefix.lib,
                '-DGENIE_INC=%s/GENIE'%self.spec['genie'].prefix.include,
                '-DGENIE=%s'%self.spec['genie'].prefix,
                '-DGENIE_VERSION=%s'%self.spec['genie'].version,
                '-DDK2NUDATA_DIR=%s'%self.spec['dk2nudata'].prefix.lib ,
                '%s/dk2nu' % self.stage.source_path ]
        return args

    def build(self, spec, prefix):
        with working_dir('%s/spack-build'%self.stage.path, create=True):
            make('VERBOSE=t', 'all')

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('DK2NUGENIE_INC',dspec['dk2nugenie'].prefix.include)
        spack_env.set('DK2NUGENIE_LIB', dspec['dk2nugenie'].prefix.lib)
