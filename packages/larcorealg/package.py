# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Larcorealg(CMakePackage):
    """Larcorealg"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larcorealg"
    url      = "http://cdcvs.fnal.gov/projects/larcorealg"

    version('develop', git='http://cdcvs.fnal.gov/projects/larcorealg', branch='develop')

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    patch('patch')

    depends_on('larcoreobj')
    depends_on('cetmodules', type='build')

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value),
                '-Dlarcorealg_gdml_dir={0}/gdml'.
                format(self.spec.prefix.share),
                '-Dlarcorealg_fcl_dir={0}/fhicl'.
                format(self.spec.prefix.share),
               ]
        return args

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('LARCOREALG_INC',dspec['larcorealg'].prefix.include)
        spack_env.append_path('ROOT_INCLUDE_PATH',dspec['larcorealg'].prefix.include)
        spack_env.set('LARCOREALG_LIB', dspec['larcorealg'].prefix.lib)
