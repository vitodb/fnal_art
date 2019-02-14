# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libwda(MakefilePackage):
    """Fermilab Web Data Access library"""

    homepage = "http://cdcvs.fnal.gov/redmine/projects/libwda"
    url      = "http://cdcvs.fnal.gov/projects/ifdhc-libwda"

    version('v2_26_0', git=url, preferred=True)

    parallel = False

    build_directory = 'src'

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            make()
            make("PREFIX=" + prefix, 'install')

