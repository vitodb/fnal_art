# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack import *


class ArtdaqMu2e(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
    event building, event reconstruction and analysis (using the art analysis
    framework), process management, system and process state behavior, control
    messaging, local message logging (status and error messages), DAQ process
    and art module configuration, and the writing of event data to disk in ROOT
    format."""

    homepage = "https://github.com/Mu2e/artdaq_mu2e"
    url = "https://github.com/Mu2e/artdaq_mu2e/archive/refs/tags/v1_05_02.tar.gz"
    git = "https://github.com/Mu2e/artdaq_mu2e.git"

    version("develop", branch="develop", get_full_repo=True)
    version("v1_05_02", commit="a66151c")

    def url_for_version(self, version):
        url = "https://github.com/Mu2e/artdaq_mu2e/archive/refs/tags/{0}.tar.gz"
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
    depends_on("artdaq-core-mu2e")
