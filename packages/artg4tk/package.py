# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Artg4tk(CMakePackage):
    """Artg4tk """

    homepage = "https://cdcvs.fnal.gov/redmine/projects/artg4tk/wiki"
    url      = "http://cdcvs.fnal.gov/projects/artg4tk/"

    version('develop', git = url, branch="develop")

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')
    patch('patch')

    depends_on('cetmodules', type='build')
    depends_on('art')
    depends_on('geant4')
 
    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value),
                '-Dartg4tk_fcl_dir={0}/fhicl'.
                format(self.spec.prefix.share),
               ]
        return args
