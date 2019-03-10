# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Larreco(CMakePackage):
    """Larreco"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larreco"
    url      = "http://cdcvs.fnal.gov/projects/larreco"

    version('MVP1a', git='http://cdcvs.fnal.gov/projects/larreco', branch='feature/Spack-MVP1a')

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    depends_on('larsim')
    depends_on('nutools')
    depends_on('eigen')
    depends_on('tensorflow')
    depends_on('cetmodules', type='build')

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value),
               ]
        return args

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('LARRECO_INC',dspec['larreco'].prefix.include)
        spack_env.set('LARRECO_LIB', dspec['larreco'].prefix.lib)
