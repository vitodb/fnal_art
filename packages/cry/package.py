# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import glob


class Cry(Package):
    """Generates correlated cosmic-ray particle showers at one of three 
elevations (sea level, 2100m, and 11300m) for use as input to transport 
and detector simulation codes. """

    homepage = "https://nuclear.llnl.gov/simulation/"
    url      = "https://nuclear.llnl.gov/simulation/cry_v1.7.tar.gz"

    version('1.7', sha256='dcee2428f81cba113f82e0c7c42f4d85bff4b8530e5ab5c82c059bed3e570c20')

    parallel = False

    variant('cxxstd',
            default='17',
            values=('default', '98', '11', '14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

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

    def setup_environment(self, spack_env, run_env):
        spack_env.append_flags('CXXFLAGS', self.set_cxxstdflag())


    def install(self, spec, prefix):
        makefile = FileFilter('Makefile.common')
        makefile.filter('CXX = .*', 'CXX = c++')
        with open('Makefile.local', 'w') as f:
            f.write('CXXFLAGS += -fPIC')
        make()
        for f in glob.glob('src/*.o'):
            os.remove(f)
        setup = FileFilter('setup')
        setup.filter('^cd ".*', 'cd "%s"' % prefix)
        install_tree(self.stage.source_path, prefix)

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('CRYHOME',dspec['cry'].prefix)
        spack_env.set('CRY_LIB',dspec['cry'].prefix.lib)
        spack_env.set('CRYDATAPATH', dspec['cry'].prefix.data)
        run_env.set('CRYHOME',dspec['cry'].prefix)
        run_env.set('CRY_LIB',dspec['cry'].prefix.lib)
        run_env.set('CRYDATAPATH', dspec['cry'].prefix.data)
