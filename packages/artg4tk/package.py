# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import os
import sys
libdir="%s/var/spack/repos/fnal_art/lib" % os.environ["SPACK_ROOT"]
if not libdir in sys.path:
    sys.path.append(libdir)



def patcher(x):
    cetmodules_20_migrator(".","artg4tk","9.07.01")


class Artg4tk(CMakePackage):
    """Artg4tk """

    homepage = "https://cdcvs.fnal.gov/redmine/projects/artg4tk/wiki"
    url      = "https://cdcvs.fnal.gov/projects/artg4tk"
    version('10.02.01', tag='v10_02_01', git=url, extention='tar.bz2', get_full_repo=True)

    version('MVP1a', git = url, branch = 'feature/Spack-MVP1a',
            extention='tar.bz2')
    version('09.04.04', tag='v09_04_04', git=url, extention='tar.bz2', get_full_repo=True)
    version('09.05.00', tag='v09_05_00', git=url, extention='tar.bz2', get_full_repo=True)
    version('09.05.01', tag='v09_05_01', git=url, extention='tar.bz2', get_full_repo=True)
    version('09.05.02', tag='v09_05_02', git=url, extention='tar.bz2', get_full_repo=True)
    version('09.06.00', tag='v09_06_00', git=url, extention='tar.bz2', get_full_repo=True)
    version('09.04.04', tag='v09_04_04', git=url, extention='tar.bz2', get_full_repo=True)
    version('09.05.00', tag='v09_05_00', git=url, extention='tar.bz2', get_full_repo=True)
    version('09.05.01', tag='v09_05_01', git=url, extention='tar.bz2', get_full_repo=True)
    version('09.05.02', tag='v09_05_02', git=url, extention='tar.bz2', get_full_repo=True)
    version('09.06.00', tag='v09_06_00', git=url, extention='tar.bz2', get_full_repo=True)
    version('09.07.00', tag='v09_07_00', git=url, extention='tar.bz2', get_full_repo=True)
    version('09.07.01', tag='v09_07_01', git=url, extention='tar.bz2', get_full_repo=True)

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')



    depends_on('cetmodules', type='build')
    depends_on('art-root-io')
    depends_on('canvas-root-io')
    depends_on('geant4')
    depends_on('root')
    depends_on('boost')
 
    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value)
               ]
        return args

    def url_for_version(self, version):
        url = 'https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/{0}.v{1}.tbz2'
        return url.format(self.name, version.underscored)

