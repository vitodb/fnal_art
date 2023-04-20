# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack import *


class ArtdaqEpicsPlugin(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
    event building, event reconstruction and analysis (using the art analysis
    framework), process management, system and process state behavior, control
    messaging, local message logging (status and error messages), DAQ process
    and art module configuration, and the writing of event data to disk in ROOT
    format."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/artdaq/wiki"
    url = "https://github.com/art-daq/artdaq_epics_plugin/archive/refs/tags/v1_05_02.tar.gz"
    git = "https://github.com/art-daq/artdaq_epics_plugin.git"

    version("develop", branch="develop", get_full_repo=True)
    version("v1_05_03", sha256="68937458d87d53ac20607b9e62ac13616c143f3f074675b047897a0b10cf20f0")
    version("v1_05_02", sha256="8a8d12f29a357c2426c16c3aef1a745b6bf3308ede38aae2300584eff582a3cf")

    def url_for_version(self, version):
        url = "https://github.com/art-daq/artdaq_epics_plugin/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    variant(
        "cxxstd",
        default="17",
        values=("14", "17"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("cetmodules", type="build")
    depends_on("epics-base")

    depends_on("artdaq-utilities")


