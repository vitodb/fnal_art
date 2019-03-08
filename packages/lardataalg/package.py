# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Lardataalg(CMakePackage):
    """Lardataalg"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/lardataalg"
    url      = "http://cdcvs.fnal.gov/projects/lardataalg"

    version('develop', git='http://cdcvs.fnal.gov/projects/lardataalg', branch='develop')

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    patch('patch')

    depends_on('lardataobj')
    depends_on('larcorealg')
    depends_on('cetmodules', type='build')

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value),
                '-Dlardataalg_fcl_dir={0}/share'.
                format(self.spec.prefix.share),
               ]
        return args

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('LARDATAALG_INC',dspec['lardataalg'].prefix.include)
        spack_env.append_path('ROOT_INCLUDE_PATH',dspec['lardataalg'].prefix.include)
        spack_env.set('LARDATAALG_LIB', dspec['lardataalg'].prefix.lib)
