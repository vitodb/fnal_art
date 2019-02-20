# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import os

class GeniePhyoptDkcharm(Package):
    """Data files used by genie."""

    homepage = "http://www.example.com"
    url = "http://scisoft.fnal.gov/scisoft/packages/genie_phyopt/v2_12_10/genie_phyopt-2.12.10-noarch-dkcharm.tar.bz2"
    version('2.12.10',url=url,
             sha256='5764cc6e7fc23f721177761526b75725b73970cd941064c23563d9ccaa3de0dc')

    def install(self, spec, prefix):
        install_tree(self.stage.source_path,prefix)

