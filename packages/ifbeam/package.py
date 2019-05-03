# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ifbeam(Package):
    """Data handling client code for intensity frontier experiments"""

    homepage = "http://cdcvs.fnal.gov/redmine/projects/ifbeam"

    version('2.3.0',
            sha256='4b6a29443b631957ca2a7712b5c577620c6543e542ee9c77d246cef1e10f7324',
            extension='tbz2')
    version('2.2.13',
            sha256='b341ffc73421b7187b06c205f9feaccf117bdba06509e9b1b8f491fdc182029c',
            extension='tbz2')

    parallel = False

    depends_on('ifdhc')
    depends_on('libwda')
    
    parallel = False 

    variant('cxxstd',
            default='17',
            values=('default', '98', '11', '14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    def url_for_version(self, version):
        url = 'http://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/{0}.v{1}.tbz2'
        return url.format('ifdhc-' + self.name, version.underscored)

    def install(self, spec, prefix):
        with working_dir(self.stage.source_path+'/src'):
            makefile = FileFilter('Makefile')
            makefile.filter('gcc', '$(CC)')
            makefile.filter('g\+\+', '$(CXX)')
            make.add_default_env('LIBWDA_FQ_DIR',
                                 '{0}'.format(self.spec['libwda'].prefix))
            make.add_default_env('LIBWDA_LIB',
                                 '{0}/lib'.format(self.spec['libwda'].prefix))
            make.add_default_env('IFDHC_FQ_DIR',
                                 '{0}'.format(self.spec['ifdhc'].prefix))
            make.add_default_env('IFDHC_LIB',
                                 '{0}/lib'.format(self.spec['ifdhc'].prefix))
            make.add_default_env('IFDHC_INC',
                                 '{0}/inc'.format(self.spec['ifdhc'].prefix))
            cxxstd_flag\
                = '' if self.spec.variants['cxxstd'].value == 'default' else \
                'cxx{0}_flag'.format(self.spec.variants['cxxstd'].value)
            make.add_default_env('ARCH', getattr(self.compiler, cxxstd_flag))
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
