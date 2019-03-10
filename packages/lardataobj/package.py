# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Lardataobj(CMakePackage):
    """Lardataobj"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/lardataobj"
    url      = "http://cdcvs.fnal.gov/projects/lardataobj"

    version('MVP1a', git='http://cdcvs.fnal.gov/projects/lardataobj', branch='feature/Spack-MVP1a')

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    depends_on('clhep')
    depends_on('root+python')
    depends_on('boost')
    depends_on('canvas')
    depends_on('cetlib')
    depends_on('cetlib-except')
    depends_on('fhicl-cpp')
    depends_on('hep-concurrency')
    depends_on('messagefacility')
    depends_on('tbb')
    depends_on('canvas-root-io')

    depends_on('nusimdata')
    depends_on('larcoreobj')
    depends_on('larcorealg')
    depends_on('cetmodules', type='build')

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value),
                '-Dlardataobj_fcl_dir={0}/fcl'.
                format(self.spec.prefix),
                '-Dlardataobj_gdml_dir={0}/gdml'.
                format(self.spec.prefix),
               ]
        return args

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('LARDATAOBJ_INC',dspec['lardataobj'].prefix.include)
        spack_env.set('LARDATAOBJ_LIB', dspec['lardataobj'].prefix.lib)

    @run_after('install')
    def create_dirs(self):
        mkdirp('{0}/fcl'.format(self.spec.prefix))
        mkdirp('{0}/gdml'.format(self.spec.prefix))
