# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack import *


class ArtdaqCoreDemo(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
    event building, event reconstruction and analysis (using the art analysis
    framework), process management, system and process state behavior, control
    messaging, local message logging (status and error messages), DAQ process
    and art module configuration, and the writing of event data to disk in ROOT
    format."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/artdaq/wiki"
    url = "https://github.com/art-daq/artdaq_core_demo/archive/refs/tags/v1_10_02.tar.gz"
    git = "https://github.com/art-daq/artdaq_core_demo.git"

    version("develop", branch="develop", get_full_repo=True)
    version("v1_10_04", sha256="dfd8e9fee3ee4db745630664e2a36d3cd2200871d8bc83a6216f88be1adb18a1")
    version("v1_10_03", sha256="c3fc28422e2a08ead7b56e9a9edaf2dac8bd0c769687aa6f21d375609cc6c0c4")
    version("v1_10_02", sha256="ea6b04590bfa158e1528bf4b46cc04a0a7b065848d48ba3ab1cf94ac1bc45389")

    def url_for_version(self, version):
        url = "https://github.com/art-daq/artdaq_core_demo/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", conditional("20",when="@v1_10_04:")),
        multi=False,
        sticky=True,
        description="Use the specified C++ standard when building.",
    )

    depends_on("cetmodules", type="build")
    depends_on("artdaq-core")
