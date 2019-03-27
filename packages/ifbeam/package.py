# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ifbeam(Package):
    """Data handling client code for intensity frontier experiments"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/ifbeam"
    url      = "http://cdcvs.fnal.gov/projects/ifdhc-ifbeam"

    version('2.2.13', git=url, tag='v2_2_13')

    parallel = False

    depends_on('ifdhc')
    depends_on('libwda')
    
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

    def install(self, spec, prefix):
        with working_dir(self.stage.source_path+'/src'):
            makefile = FileFilter('Makefile')
            makefile.filter('gcc', '$(CC)')
            makefile.filter('g\+\+', '$(CXX)')
            make.add_default_env('LIBWDA_FQ_DIR', '{0}'.format(self.spec['libwda'].prefix))
            make.add_default_env('LIBWDA_LIB', '{0}/lib'.format(self.spec['libwda'].prefix))
            make.add_default_env('IFDHC_FQ_DIR', '{0}'.format(self.spec['ifdhc'].prefix))
            make.add_default_env('IFDHC_LIB', '{0}/lib'.format(self.spec['ifdhc'].prefix))
            make.add_default_env('IFDHC_INC', '{0}/inc'.format(self.spec['ifdhc'].prefix))
            make.add_default_env('ARCH', self.set_cxxstdflag())
            make()
            make('DESTDIR=' + prefix, 'install')

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('IFBEAM_FQ_DIR', '{0}'.format(self.prefix))
        spack_env.set('IFBEAM_DIR', '{0}'.format(self.prefix))
        spack_env.set('IFBEAM_INC', '{0}/ifbeam/src'.format(self.prefix.share))
        spack_env.set('IFBEAM_LIB', '{0}'.format(self.prefix.lib))
        # Ensure we can find plugin libraries.
        spack_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        run_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        spack_env.prepend_path('PATH', self.prefix.bin)
        run_env.prepend_path('PATH', self.prefix.bin)
        spack_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
