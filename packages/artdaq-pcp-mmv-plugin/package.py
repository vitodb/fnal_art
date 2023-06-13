# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack import *


class ArtdaqPcpMmvPlugin(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
    event building, event reconstruction and analysis (using the art analysis
    framework), process management, system and process state behavior, control
    messaging, local message logging (status and error messages), DAQ process
    and art module configuration, and the writing of event data to disk in ROOT
    format."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/artdaq/wiki"
    url = "https://github.com/art-daq/artdaq_pcp_mmv_plugin/archive/refs/tags/v1_03_02.tar.gz"
    git = "https://github.com/art-daq/artdaq_pcp_mmv_plugin.git"

    version("develop", branch="develop", get_full_repo=True)
    version("v1_03_04", sha256="7f7bebc059e7f174c4591017cbb754f8bc447c1edde9b347c76641aa8251ee7f")
    version("v1_03_03", sha256="699dc00f34ed9c698621087aa203d4df163fba96ed0246f993a8e09513929302")
    version("v1_03_02", sha256="c758895726c01b72f8937ef9a1a3f30c5e1e4c94557bf8f043bd9694790a6bfe")

    def url_for_version(self, version):
        url = "https://github.com/art-daq/artdaq_pcp_mmv_plugin/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", conditional("20",when="@v1_03_04:")),
        multi=False,
        sticky=True,
        description="Use the specified C++ standard when building.",
    )

    depends_on("cetmodules", type="build")

    depends_on("artdaq-utilities")
    
