# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cetmodules(CMakePackage):
    """CMake glue modules and scripts required by packages originating at
    Fermilab and associated experiments and other collaborations.
    """

    homepage = 'http://cdcvs.fnal.gov/projects/cetmodules'

    version('develop', branch='develop', git=homepage)
    version('master', branch='master', git=homepage)
    version('1.00.00', sha256='67438bb1ee9acdaadb6e245ff670463c4603c3283c69b3c9d1a04d6ee9a3fd16', extension='tbz2')
    version('0.07.00', '60fb6f9ff26605ea4c0648fa43d0a516', extension='tbz2')

    depends_on('cmake@3.4:', type='build')

    def url_for_version(self, version):
        url = 'http://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/{0}.v{1}.tbz2'
        return url.format(self.name, version.underscored)
