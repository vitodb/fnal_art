# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class LarsoftData(Package):
    """LarsoftData"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larsoft_data"
    url      = "http://cdcvs.fnal.gov/projects/larsoft_data"

    version('develop', git='http://cdcvs.fnal.gov/projects/larsoft_data', branch='develop')

    def install(self, spec, prefix):
        install_tree(self.stage.source_path, prefix)

