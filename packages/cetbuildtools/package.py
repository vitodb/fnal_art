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
#     spack install cetbuildtools
#
# You can edit this file again by typing:
#
#     spack edit cetbuildtools
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Cetbuildtools(CMakePackage):

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://cdcvs.fnal.gov/redmine/projects/cetbuildtools"

    version('8.06.00', sha256='eeceb410c6ec710c384ea4b3bca4d02adc8b6d8c84886d9d3647204c32d3d8ef')

    def url_for_version(self, version):
        url = 'https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/{0}.v{1}.tbz2'
        return url.format(self.name, version.underscored)

    depends_on('cetmodules@2:')

    maintainers = ['marc_mengel']

    def cmake_args(self):
        # FIXME: Add arguments other than
        # FIXME: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
        # FIXME: If not needed delete this function
        args = []
        return args

    def setup_dependent_build_environment(self, env, dep):
        # lots of CMakefiles check this...
        env.set("CETBUILDTOOLS_VERSION", "v%s" % self.version.underscored)
        # they look in $CETBUILDTOOLS_DIR/Modules for things that are now
        # in cetmodules...
        env.set("CETBUILDTOOLS_DIR", self.spec['cetmodules'].prefix)
        env.prepend_path('CMAKE_PREFIX_PATH', self.prefix )

