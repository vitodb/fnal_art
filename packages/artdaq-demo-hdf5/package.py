# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack import *


class ArtdaqDemoHdf5(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
    event building, event reconstruction and analysis (using the art analysis
    framework), process management, system and process state behavior, control
    messaging, local message logging (status and error messages), DAQ process
    and art module configuration, and the writing of event data to disk in ROOT
    format."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/artdaq/wiki"
    url = "https://github.com/art-daq/artdaq_demo_hdf5/archive/refs/tags/v1_04_02.tar.gz"
    git = "https://github.com/art-daq/artdaq_demo_hdf5.git"

    version("develop", branch="develop", get_full_repo=True)
    version("v1_04_03", sha256="68c2bad6f57ac540accafc7f77247e4fbca23d9f78cfb7ee581d2a2043d27365")
    version("v1_04_02", sha256="5eb2439158e07d0449c501596e89d7fae61d738ecab177c1da2f4bc16b8f3753")

    def url_for_version(self, version):
        url = "https://github.com/art-daq/artdaq_demo_hdf5/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    variant(
        "cxxstd",
        default="17",
        values=("14", "17"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("cetmodules", type="build")
    depends_on("hdf5")

    depends_on("artdaq")

