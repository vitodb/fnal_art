# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install gm2tracker
#
# You can edit this file again by typing:
#
#     spack edit gm2tracker
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Gm2tracker(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://redmine.fnal.gov/projects/gm2tracker"
    url      = "https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/gm2tracker.v9_60_00.tbz2" 
    def url_for_version(self, version):
        return "https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/gm2tracker.v%s.tbz2" % version.underscored

    version('9.60.00', sha256='1efd2e99333d99c8fcbaa6743e5e5b86aa0f6d93f7c2c7db823ff08980feedde')

    variant('cxxstd',default='17')

    depends_on('pkgconfig', type='build')
    depends_on('cetpkgsupport', type=('build'))
    depends_on('cetbuildtools', type=('build'))
    depends_on('cetmodules', type=('build'))
    depends_on('artg4', type=('build','run'))
    depends_on('gm2geom', type=('build','run'))
    depends_on('gm2dataproducts', type=('build','run'))
    depends_on('gm2util', type=('build','run'))
    depends_on('gsl', type=('build','run'))
    depends_on('eigen', type=('build','run'))

    def patch(self):
        filter_file('^CMAKE_MINIMUM_REQUIRED.*',
           'CMAKE_MINIMUM_REQUIRED( VERSION 3.14 )\nfind_package(cetmodules)',
           'CMakeLists.txt')
        filter_file('^PROJECT.*','PROJECT({0} VERSION {1} LANGUAGES CXX C)' 
           .format(self.name, self.version), 
           'CMakeLists.txt')

    def cmake_args(self):
        # FIXME: Add arguments other than
        # FIXME: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
        # FIXME: If not needed delete this function
        args = []
        return args
