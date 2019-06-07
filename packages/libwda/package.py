# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libwda(MakefilePackage):
    """Fermilab Web Data Access library"""

    homepage = "http://cdcvs.fnal.gov/redmine/projects/libwda"
    url      = "http://cdcvs.fnal.gov/projects/ifdhc-libwda"

    version('2.26.0', git=url, tag='v2_26_0', preferred=True)

    parallel = False

    variant('cxxstd',
            default='17',
            values=('default', '98', '11', '14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')


    build_directory = 'src'

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            makefile = FileFilter('Makefile')
            makefile.filter('gcc', '$(CC)')
            makefile.filter('g\+\+', '$(CXX)')
            cxxstd_flag\
                = '' if self.spec.variants['cxxstd'].value == 'default' else \
                'cxx{0}_flag'.format(self.spec.variants['cxxstd'].value)
            make.add_default_env('ARCH', getattr(self.compiler, cxxstd_flag))
            make('LIBWDA_VERSION=v{0}'.format(self.version.underscored))
            make('PREFIX={0}'.format(prefix), 'install')

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('LIBWDA_INC', '{0}'.format(self.prefix.include))
        spack_env.set('LIBWDA_LIB', '{0}'.format(self.prefix.lib))
        # Ensure we can find plugin libraries.
        spack_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        run_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        spack_env.prepend_path('PATH', self.prefix.bin)
        run_env.prepend_path('PATH', self.prefix.bin)
        spack_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)


