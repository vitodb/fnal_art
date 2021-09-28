# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Gm2midas(CMakePackage):
    """Gm2 experiment tracking code"""

    homepage = "https://redmine.fnal.gov/projects/gm2midas"
    url      = "https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/gm2midas.v9_60_00.tbz2" 
    git_base = 'https://cdcvs.fnal.gov/projects/gm2midas'
    version('spack_branch', branch='feature/mengel_spack', git=git_base, get_full_repo=True)
    def url_for_version(self, version):
        return "https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/gm2midas.v%s.tbz2" % version.underscored

    variant('cxxstd',default='17')

    depends_on('root', type=('build','run'))
    depends_on('zlib', type=('build','run'))
    depends_on('openssl', type=('build','run'))

    root_cmakelists_dir = 'midas'

    def patch(self):
        filter_file('^PROJECT.*','PROJECT({0} VERSION {1} LANGUAGES CXX C)' 
           .format(self.name, self.version), 
           'midas/CMakeLists.txt')

    def cmake_args(self):
        # FIXME: Add arguments other than
        # FIXME: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
        # FIXME: If not needed delete this function
        args = []
        return args
