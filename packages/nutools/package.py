# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Nutools(CMakePackage):
    """Nutools"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/nutools/wiki"
    url      = "http://cdcvs.fnal.gov/projects/nutools/"

    version('v2_26_01', git=url, tag='v2_26_01')

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    patch('patch')

    depends_on('cmake@3.4:', type='build')
    depends_on('cetmodules', type='build')
    depends_on('cetlib-except')
    depends_on('cetlib')
    depends_on('fhicl-cpp')
    depends_on('messagefacility')
    depends_on('canvas')
    depends_on('canvas-root-io')
    depends_on('boost')
    depends_on('tbb')
    depends_on('root+python')
    depends_on('clhep')
    depends_on('sqlite@3.8.2:')
    depends_on('perl')
    depends_on('nusimdata')
    depends_on('dk2nugenie')
    depends_on('geant4')
    depends_on('cry')
    depends_on('pythia6')
    depends_on('ifdh-art')
    depends_on('libwda')
    depends_on('postgresql-client')
    depends_on('libxml2')

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value),
                '-DROOTSYS={0}'.
                format(self.spec['root'].prefix),
                '-DROOT_BASIC_LIB_LIST=Core;RIO;Net;Imt;Hist;Graf;Graf3d;Gpad;Tree;Rint;Postscript;Matrix;Physics;MathCore;Thread'
               ] 
        return args

    def setup_environment(self, spack_env, run_env):
        spack_env.set('PYLIB', self.spec['pythia6'].prefix.lib)
        spack_env.set('POSTGRESQL_LIBRARIES', self.spec['postgresql-client'].prefix.lib)
