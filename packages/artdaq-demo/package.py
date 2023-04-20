# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack import *


class ArtdaqDemo(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
    event building, event reconstruction and analysis (using the art analysis
    framework), process management, system and process state behavior, control
    messaging, local message logging (status and error messages), DAQ process
    and art module configuration, and the writing of event data to disk in ROOT
    format."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/artdaq/wiki"
    url = "https://github.com/art-daq/artdaq_demo/archive/refs/tags/v3_12_02.tar.gz"
    git = "https://github.com/art-daq/artdaq_demo.git"

    version("develop", branch="develop", get_full_repo=True)
    version("v3_12_03", sha256="e068ea0cd09e94fc9e4ad6fce067ca716db82fd79480c07c1e16cd2659325ee2")
    version("v3_12_02", sha256="3044f14e28f2c54318d06a64c22685839d4dba1a85a30d92ebaa9fe2e8f86055")

    def url_for_version(self, version):
        url = "https://github.com/art-daq/artdaq_demo/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    variant(
        "cxxstd",
        default="17",
        values=("14", "17"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("cetmodules", type="build")

    depends_on("artdaq")
    depends_on("artdaq-core-demo")

