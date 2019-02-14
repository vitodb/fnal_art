# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import glob

class Lhapdf(Package):

    homepage = "http://www.hepforge.org/lhapdf"
    url      = "http://www.hepforge.org/archive/lhapdf/lhapdf-5.9.1.tar.gz"

    version('5.9.1', sha256='86b9b046d7f25627ce2aab6847ef1c5534972f4bae18de98225080cf5086919c')

    resource(name='pdfsets', 
             url='http://scisoft.fnal.gov/scisoft/packages/pdfsets/v5_9_1b/pdfsets-5.9.1b-noarch.tar.bz2',
             md5='944e1b7f79b1623afeb50441c9bcffb0')
    

    def patch(self):
        if os.path.exists('./config/config.sub'):
            os.remove('./config/config.sub')
            install(os.path.join(os.path.dirname(__file__), '../../config/config.sub'), './config/config.sub')
        if os.path.exists('./config/config.guess'):
            os.remove('./config/config.guess')
            install(os.path.join(os.path.dirname(__file__), '../../config/config.guess'), './config/config.guess')

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

    def setup_environment(self, spack_env, run_env):
        spack_env.append_flags('CXXFLAGS', self.set_cxxstdflag())


    @run_before('install')
    def copy_pdfs(self):
        mkdirp(join_path(self.spec.prefix.share, 'lhapdf'))
        for pdfsets in glob.glob('pdfsets/*/PDFsets'):
            install_tree(pdfsets, join_path(self.spec.prefix.share, 'lhapdf/PDFsets'))

    def install(self,spec,prefix):
        with working_dir(join_path(self.stage.path,'spack-build'), create=True):
           args = ['--prefix={0}'.format(prefix), '--enable-low-memory', '--disable-pyext', '--disable-octave']
           configure=which(join_path(self.stage.source_path,'configure'))
           configure(*args)
           make()
           make('check')
           make('install')
        

    @run_after('install')
    def copy_examples(self):
      with working_dir(self.stage.source_path):
        install_tree('examples', self.prefix.examples)
      with working_dir(self.prefix.examples):
        for f in glob.glob('Makefile.*'):
            os.remove(f)
        for f in glob.glob('*.py'):
            os.remove(f)
        
