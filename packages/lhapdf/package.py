# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os

class Lhapdf(AutotoolsPackage):

    homepage = "http://www.hepforge.org/lhapdf"
    url      = "http://www.hepforge.org/archive/lhapdf/lhapdf-5.9.1.tar.gz"

    version('5.9.1', sha256='86b9b046d7f25627ce2aab6847ef1c5534972f4bae18de98225080cf5086919c')

    def patch(self):
        if os.path.exists('./config/config.sub'):
            os.remove('./config/config.sub')
            install(os.path.join(os.path.dirname(__file__), 'patches/config.sub'), './config/config.sub')
        if os.path.exists('./config/config.guess'):
            os.remove('./config/config.guess')
            install(os.path.join(os.path.dirname(__file__), 'patches/config.guess'), './config/config.guess')

    

    def configure_args(self):
        args = ['--enable-low-memory', '--disable-pyext', '--disable-octave']
        return args

    @run_after('install')
    def copy_examples(self):
      with working_dir(self.stage.source_path):
        install('examples', self.prefix)
      with working_dir(self.prefix):
        for f in glob.glob('examples/Makefile.*'):
            os.remove(f)
        for f in glob.glob('examples/*.py'):
            os.remove(f)
        
