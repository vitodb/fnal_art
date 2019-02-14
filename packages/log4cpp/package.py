# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import os, glob

class Log4cpp(Package):
    """A library of C++ classes for flexible logging to files (rolling),
syslog, IDSA and other destinations. It is modeled after the Log for Java
 library (http://www.log4j.org), staying as close to their API as is 
reasonable."""

    homepage = "https://sourceforge.net/projects/log4cpp/"
    url      = "https://newcontinuum.dl.sourceforge.net/project/log4cpp/log4cpp-1.1.x%20%28new%29/log4cpp-1.1/log4cpp-1.1.3.tar.gz"

    version('1.1.3', '74f0fea7931dc1bc4e5cd34a6318cd2a51322041',extension='tar.gz')

    def patch(self):
        if os.path.exists('./config/config.sub'):
            os.remove('./config/config.sub')
            install(os.path.join(os.path.dirname(__file__), '../../config/config.sub'), './config/config.sub')
        if os.path.exists('./config/config.guess'):
            os.remove('./config/config.guess')
            install(os.path.join(os.path.dirname(__file__), '../../config/config.guess'), './config/config.guess')
        patch('patch/log4cpp.patch')

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

    def install(self,spec,prefix):
        with working_dir(join_path(self.stage.path,'spack-build'), create=True):
           args = ['--prefix={0}'.format(prefix)]
           configure=which(join_path(self.stage.source_path,'configure'))
           configure(*args)
           make()
           make('check')
           make('install')

