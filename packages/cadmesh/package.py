# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class Cadmesh(CMakePackage):
    """Load triangular mesh based CAD files into Geant4 quickly and easily."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/christopherpoole/CADMesh/"
    url      = "https://github.com/christopherpoole/CADMesh/archive/refs/tags/v2.0.3.tar.gz"

    # maintainers = ['marcmengel']

    version('2.0.3', sha256='fc0765fc984b32a7b7b6687bb84a57b3d1c0c1db8991a651b3443b4971e48c01')
    version('2.0.2', sha256='069f5bef295a49b8868c27d973acf3a0b84011af9d53a0869c1eacafa697b7da')
    version('2.0.1', sha256='b3a79cccb08d852fb14233a0874a9fc65dea01b97e552dfcbf5569e638f1c708')
    version('2.0',   sha256='352ac41df3b87169999e9e1b10fc7a1a67f44b276b4f0d1b26ad9dfeb81945d5')

    def url_for_version(self, version):

        url = "https://github.com/christopherpoole/CADMesh/archive/refs/tags/v{0}.tar.gz"
        return url.format(self.name, version)


    variant('cxxstd',default='17')

    def cmake_args(self):
        # FIXME: Add arguments other than
        # FIXME: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
        # FIXME: If not needed delete this function
        args = []
        return args
