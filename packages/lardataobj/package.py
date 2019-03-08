# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Lardataobj(CMakePackage):
    """Lardataobj"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/lardataobj"
    url      = "http://cdcvs.fnal.gov/projects/lardataobj"

    version('develop', git='http://cdcvs.fnal.gov/projects/lardataobj', branch='develop')

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    patch('patch')

    depends_on('nusimdata')
    depends_on('larcoreobj')
    depends_on('larcorealg')
    depends_on('cetmodules', type='build')

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value),
                '-Dlardataobj_fcl_dir={0}/fhicl'.
                format(self.spec.prefix.share),
                '-Dlardataobj_gdml_dir={0}/gdml'.
                format(self.spec.prefix.share),
               ]
        return args

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('LARDATAOBJ_INC',dspec['lardataobj'].prefix.include)
        spack_env.set('LARDATAOBJ_LIB', dspec['lardataobj'].prefix.lib)
