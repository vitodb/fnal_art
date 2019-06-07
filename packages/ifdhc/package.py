# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class Ifdhc(Package):
    """Data handling client code for intensity frontier experiments"""

    homepage = "http://cdcvs.fnal.gov/redmine/projects/ifdhc"
    url      = "http://cdcvs.fnal.gov/projects/ifdhc/ifdhc.git"

    version('2.3.10', git='http://cdcvs.fnal.gov/projects/ifdhc/ifdhc.git', tag='v2_3_10')

    depends_on('python')
    depends_on('swig', type='build')

    variant('cxxstd',
            default='17',
            values=('default', '98', '11', '14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    parallel = False 

    def install(self, spec, prefix):
        makefile = FileFilter('Makefile')
        makefile.filter('gcc', '$(CC)')
        makefile.filter('g\+\+', '$(CXX)')
        cxxstd_flag\
            = '' if self.spec.variants['cxxstd'].value == 'default' else \
            'cxx{0}_flag'.format(self.spec.variants['cxxstd'].value)
        make.add_default_env('ARCH', getattr(self.compiler, cxxstd_flag))
        make('IFDH_VERSION=v{0}'.format(self.version.underscored))
        make('install')
        install_tree(self.stage.source_path, prefix)

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('IFDHC_FQ_DIR', '{0}'.format(self.prefix))
        spack_env.set('IFDHC_DIR', '{0}'.format(self.prefix))
        spack_env.set('IFDHC_INC', '{0}/ifdhc/src'.format(self.prefix.share))
        spack_env.set('IFDHC_LIB', '{0}'.format(self.prefix.lib))
        # Ensure we can find plugin libraries.
        spack_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        run_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        spack_env.prepend_path('PATH', self.prefix.bin)
        run_env.prepend_path('PATH', self.prefix.bin)
        spack_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
