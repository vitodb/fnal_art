# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Nutools(CMakePackage):
    """Nutools"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/nutools/wiki"
    url      = "http://cdcvs.fnal.gov/projects/nutools/"

    version('MVP1a', git="http://cdcvs.fnal.gov/projects/nutools", branch='feature/Spack-MVP1a')

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

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
    depends_on('pythia6')
    depends_on('libwda')
    depends_on('postgresql')
    depends_on('libxml2')
    depends_on('art')
    depends_on('nusimdata')
    depends_on('dk2nugenie')
    depends_on('geant4~data')
    depends_on('xerces-c')
    depends_on('cry')
    depends_on('ifdh-art')
    depends_on('ifdhc')
    depends_on('ifbeam')
    depends_on('nucondb')
    depends_on('libwda')


    def url_for_version(self, version):
        url = 'https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/{0}.v{1}.tbz2'
        return url.format(self.name, version.underscored)


    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value),
                '-DROOTSYS={0}'.
                format(self.spec['root'].prefix),
                '-Dnutools_fcl_dir=fcl'.
                format(self.spec['root'].prefix),
                '-DGENIE_INC={0}'.
                format(self.spec['genie'].prefix.include),
                '-DCRYHOME={0}/src'.
                format(self.spec['cry'].prefix),
                '-DLOG4CPP_INC={0}'.
                format(self.spec['log4cpp'].prefix.include),
                '-DIFDH_ART_INC={0}'.
                format(self.spec['ifdh-art'].prefix.include),
                '-DIFDHC_INC={0}/inc'.
                format(self.spec['ifdhc'].prefix),
                '-DDK2NUGENIE_INC={0}'.
                format(self.spec['dk2nugenie'].prefix.include),
                '-DDK2NUDATA_INC={0}'.
                format(self.spec['dk2nudata'].prefix.include),
                '-DXERCES_C_INC={0}'.
                format(self.spec['xerces-c'].prefix.include),
                '-DLIBXML2_INC={0}'.
                format(self.spec['libxml2'].prefix.include),
                '-DLIBWDA_INC={0}'.
                format(self.spec['libwda'].prefix.include),
               ] 
        return args
