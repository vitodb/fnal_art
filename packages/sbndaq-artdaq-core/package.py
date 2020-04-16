# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class SbndaqArtdaqCore(CMakePackage):
    """The toolkit currently provides SBNDAQ extensions to the artdaq-core 
 functionality for data transfer, event building, event reconstruction."""

    homepage = "http://cdcvs.fnal.gov/redmine/projects/sbndaq/wiki"
    url      = "http://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/sbndaq-artdaq-core.v1_2_3.tbz2"
    version('develop', git = url, branch="develop")

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    def url_for_version(self, version):
        url = 'http://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/{0}.v{1}.tbz2'
        return url.format(self.name, version.underscored)


    patch('sbndaq-artdaq-core-unups.patch')

    depends_on('cetmodules', type='build')
    depends_on('artdaq-core')
    depends_on('cetlib')
    depends_on('cetlib-except')
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
