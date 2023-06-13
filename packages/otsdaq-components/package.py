# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack import *


class OtsdaqComponents(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
    event building, event reconstruction and analysis (using the art analysis
    framework), process management, system and process state behavior, control
    messaging, local message logging (status and error messages), DAQ process
    and art module configuration, and the writing of event data to disk in ROOT
    format."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/artdaq/wiki"
    url = "https://github.com/art-daq/otsdaq_components/archive/refs/tags/v2_06_08.tar.gz"
    git = "https://github.com/art-daq/otsdaq_components.git"

    version("develop", branch="develop", get_full_repo=True)
    version("v2_06_10", sha256="8ddb188223df272c295b0745d4c9e3a6f33a7fdad624506a781d622d64ea9616")
    version("v2_06_09", sha256="425a6dcc78394f2fa46a70cac1cd9f627846a024c71e9335ff69518be6d5482e")
    version("v2_06_08", sha256="59bdb4fd6aab1fc97072890824530cf8c9db7e57bd9d9647faf8f32aaaada4a5")

    def url_for_version(self, version):
        url = "https://github.com/art-daq/otsdaq_components/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", conditional("20",when="@v2_06_10:")),
        multi=False,
        sticky=True,
        description="Use the specified C++ standard when building.",
    )

    depends_on("cetmodules", type="build")

    depends_on("otsdaq")
    depends_on("otsdaq-utilities")

