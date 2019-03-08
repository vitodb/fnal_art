# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Larcoreobj(CMakePackage):
    """Larcoreobj"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larcoreobj"
    url      = "http://cdcvs.fnal.gov/projects/larcoreobj"

    version('develop', git='http://cdcvs.fnal.gov/projects/larcoreobj', branch='develop')

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    patch('patch')

    depends_on('canvas-root-io')
    depends_on('cetmodules', type='build')

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value),
               ]
        return args

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('LARCOREOBJ_INC',dspec['larcoreobj'].prefix.include)
        spack_env.append_path('ROOT_INCLUDE_PATH',dspec['larcoreobj'].prefix.include)
        spack_env.set('LARCOREOBJ_LIB', dspec['larcoreobj'].prefix.lib)
