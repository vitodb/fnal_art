# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import os

class GeniePhyoptDkcharmtau(Package):
    """Data files used by genie."""

    homepage = "http://www.example.com"
    url="http://scisoft.fnal.gov/scisoft/packages/genie_phyopt/v2_12_10/genie_phyopt-2.12.10-noarch-dkcharmtau.tar.bz2"
    version('2.12.10', url=url,
             sha256='ff0ecafd9a9455e8c20963c608c666f7229324c3f43e69fa58902584de08532a')

    def install(self, spec, prefix):
        install_tree(self.stage.source_path,prefix)

