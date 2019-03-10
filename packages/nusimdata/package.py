# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Nusimdata(CMakePackage):
    """Nusimdata"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/nusimdata"
    url      = "http://cdcvs.fnal.gov/projects/nusimdata"

    version('MVP1a', git='http://cdcvs.fnal.gov/projects/nusimdata', branch='feature/Spack-MVP1a', preferred=True)

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')


    # Build and link dependencies.
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
    depends_on('dk2nudata')
    depends_on('cetmodules', type='build')

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value),
                '-DDK2NUDATA_INC={0}'.
                format(self.spec['dk2nudata'].prefix.include),
                '-DDK2NUDATA_LIB={0}'.
                format(self.spec['dk2nudata'].prefix.lib),
                '-Dnusimdata_fcl_dir={0}/fcl'.
                format(self.spec.prefix),
               ]
        return args

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('NUSIMDATA_INC',dspec['nusimdata'].prefix.include)
        spack_env.set('NUSIMDATA_LIB', dspec['nusimdata'].prefix.lib)
        spack_env.append_path('ROOT_INCLUDE_PATH', dspec['nusimdata'].prefix.include)

    @run_after('install')
    def create_dirs(self):
        mkdirp('{0}/fcl'.format(self.spec.prefix))
