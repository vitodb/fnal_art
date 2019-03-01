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

    depends_on('pdfsets')

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

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('LHAPDF_INC', '{0}'.format(dspec['lhapdf'].prefix.include))
        spack_env.set('LHAPDF_LIB', '{0}'.format(dspec['lhapdf'].prefix.lib))

    def install(self,spec,prefix):
        with working_dir(self.stage.source_path):
           args = ['--prefix={0}'.format(prefix), '--enable-low-memory', '--disable-pyext', '--disable-octave']
           configure=Executable('./configure')
           configure(*args)
           make()
           make('check')
           make('install')
        
    @run_after('install')
    def link_pdfs(self):
        mkdirp(join_path(self.spec.prefix.share, 'lhapdf/PDFsets'))
        pdfs = ['CT10.LHgrid',
                'cteq61.LHgrid',
                'cteq61.LHpdf',
                'GRV98lo.LHgrid',
                'GRV98nlo.LHgrid',
                'GRVG0.LHgrid',
                'GRVG1.LHgrid',
                'GRVPI0.LHgrid',
                'GRVPI1.LHgrid']
        for pdf in pdfs:
            os.symlink('{0}/PDFsets/{1}'.format(self.spec['pdfsets'].prefix, pdf), 
                       '{0}/lhapdf/PDFsets/{1}'.format(self.spec.prefix.share,pdf))


    @run_after('install')
    def copy_examples(self):
      with working_dir(self.stage.source_path):
        install_tree('examples', self.prefix.examples)
      with working_dir(self.prefix.examples):
        for f in glob.glob('Makefile.*'):
            os.remove(f)
        for f in glob.glob('*.py'):
            os.remove(f)
        
