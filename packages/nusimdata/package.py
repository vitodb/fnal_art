# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Nusimdata(CMakePackage):
    """Nusimdata"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/nusimdata"
    url      = "http://cdcvs.fnal.gov/projects/nusimdata"

    version('develop', git='http://cdcvs.fnal.gov/projects/nusimdata', branch='develop')

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    patch('patch')

    depends_on('canvas-root-io')
    depends_on('canvas')
    depends_on('root')
    depends_on('boost')
    depends_on('dk2nudata')
    depends_on('cetmodules', type='build')

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value),
                '-DDK2NUDATA_INC={0}'.
                format(self.spec['dk2nudata'].prefix.include),
                '-DDK2NUDATA_LIB={0}'.
                format(self.spec['dk2nudata'].prefix.lib),
                '-Dnusimdata_fcl_dir={0}/fhicl'.
                format(self.spec['dk2nudata'].prefix),
               ]
        return args

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('NUSIMDATA_INC',dspec['nusimdata'].prefix.include)
        spack_env.set('NUSIMDATA_LIB', dspec['nusimdata'].prefix.lib)
