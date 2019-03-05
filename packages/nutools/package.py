# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Nutools(CMakePackage):
    """Nutools"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/nutools/wiki"
    url      = "http://cdcvs.fnal.gov/projects/nutools/"

    version('2.24.01', '7146414c5afe62c869c4a6284e66e11cd95ee341e44f913c42e405694ed0e9d8', extension='.tbz2')

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    patch('patch')

    depends_on('cetmodules', type='build')
#    depends_on('cetlib-except')
#    depends_on('cetlib')
#    depends_on('fhicl-cpp')
#    depends_on('messagefacility')
#    depends_on('canvas')
#    depends_on('canvas-root-io')
#    depends_on('boost')
#    depends_on('tbb')
#    depends_on('root+python')
#    depends_on('clhep')
#    depends_on('sqlite@3.8.2:')
#    depends_on('perl')
#    depends_on('pythia6')
#    depends_on('libwda')
#    depends_on('postgresql-client')
#    depends_on('libxml2')
    depends_on('art')
    depends_on('nusimdata')
    depends_on('dk2nugenie')
    depends_on('geant4')
    depends_on('cry')
    depends_on('ifdh-art')

    def url_for_version(self, version):
        url = 'https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/{0}.v{1}.tbz2'
        return url.format(self.name, version.underscored)


    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value),
                '-DROOTSYS={0}'.
                format(self.spec['root'].prefix),
                '-DROOT_BASIC_LIB_LIST=Core;RIO;Net;Imt;Hist;Graf;Graf3d;Gpad;Tree;Rint;Postscript;Matrix;Physics;MathCore;Thread'
               ] 
        return args

#    def setup_environment(self, spack_env, run_env):
#        spack_env.set('PYLIB', self.spec['pythia6'].prefix.lib)
#        spack_env.set('POSTGRESQL_LIBRARIES', self.spec['postgresql-client'].prefix.lib)
