# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Lardata(CMakePackage):
    """Lardata"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/lardata"
    url      = "http://cdcvs.fnal.gov/projects/lardata"

    version('MVP1a', git='http://cdcvs.fnal.gov/projects/lardata', branch='feature/Spack-MVP1a')

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    depends_on('range-v3')
    depends_on('nutools')
    depends_on('larcore')
    depends_on('lardataobj')
    depends_on('lardataalg')
    depends_on('cetmodules', type='build')

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value),
               ]
        return args

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('LARDATA_INC',dspec['lardata'].prefix.include)
        spack_env.set('LARDATA_LIB', dspec['lardata'].prefix.lib)
