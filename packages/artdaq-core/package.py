# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class ArtdaqCore(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
 event building, event reconstruction and analysis (using the art analysis
 framework), process management, system and process state behavior, control
 messaging, local message logging (status and error messages), DAQ process 
 and art module configuration, and the writing of event data to disk in ROOT
 format."""

    homepage = "http://cdcvs.fnal.gov/redmine/projects/artdaq/wiki"
    url      = "http://cdcvs.fnal.gov/projects/artdaq-core/"

    version('develop', git = url, branch="develop")

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')
    patch('patch')

    depends_on('cetmodules', type='build')
    depends_on('art')
    depends_on('canvas-root-io')
    depends_on('canvas')
    depends_on('messagefacility')
    depends_on('root')
    depends_on('boost')
    depends_on('trace')
 
    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value),
                '-DCANVAS_VERSION=v3_06_00',
                '-DMESSAGEFACILITY_VERSION=v2_02_05',
                '-DBoost_SYSTEM_LIBRARY=-lboost_system-mt',
                '-DBoost_DATE_TIME_LIBRARY=-lboost_date_time',
                '-DBoost_FILESYSTEM_LIBRARY=-lboost_filesystem',
                '-DBoost_THREAD_LIBRARY=-lboost_thread',
               ]
        return args
