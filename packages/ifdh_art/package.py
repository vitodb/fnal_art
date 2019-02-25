# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class IfdhArt(CMakePackage):
    """The ifdh_art package provides ART service access to the libraries 
from the ifdhc package."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/ifdh-art/wiki"
    url      = "http://cdcvs.fnal.gov/projects/ifdh-art/ifdh_art.git"

    version('develop', git='http://cdcvs.fnal.gov/projects/ifdh-art/ifdh_art.git', branch='develop')

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')
    patch('patch')

    depends_on('art')
    depends_on('root')
    depends_on('fhicl-cpp')
    depends_on('cetlib')
    depends_on('cetlib_except')
    depends_on('messagefacility')
    depends_on('ifdhc')
    depends_on('ifbeam')
    depends_on('nucondb')
    depends_on('libwda')
    depends_on('cetmodules', type='build')

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value),
                '-DIFBEAM={0}/libifbeam.so'.
                format(self.spec['ifbeam'].prefix.lib),
                '-DNUCONDB={0}/libnucondb.so'.
                format(self.spec['nucondb'].prefix.lib),
               ]
        return args
