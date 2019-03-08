# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Larpandoracontent(CMakePackage):
    """Larpandoracontent"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larpandoracontent/wiki"
    url      = "http://cdcvs.fnal.gov/projects/larpandoracontent"

    version('develop', git='http://cdcvs.fnal.gov/projects/larpandoracontent', branch='develop')

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    patch('patch')

    depends_on('cetmodules', type='build')
    depends_on('eigen')
    depends_on('pandora')


    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value),
               ]
        return args

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('LARPANDORACONTENT_INC', dspec['larpandoracontent'].prefix.include)
        spack_env.set('LARPANDORACONTENT_LIB', dspec['larpandoracontent'].prefix.lib)
