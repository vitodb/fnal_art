# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack import *


class Mu2ePcieUtils(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
    event building, event reconstruction and analysis (using the art analysis
    framework), process management, system and process state behavior, control
    messaging, local message logging (status and error messages), DAQ process
    and art module configuration, and the writing of event data to disk in ROOT
    format."""

    homepage = "https://github.com/Mu2e/pcie_linux_kernel_module/"
    url = "https://github.com/Mu2e/mu2e_pcie_utils/archive/refs/tags/v2_08_00.tar.gz"
    git = "https://github.com/Mu2e/mu2e_pcie_utils.git"

    version("develop", branch="develop", get_full_repo=True)
    version("v2_08_00", commit="32899a1")

    def url_for_version(self, version):
        url = "https://github.com/Mu2e/mu2e_pcie_utils/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    variant(
        "cxxstd",
        default="17",
        values=("14", "17"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )


    depends_on("cetmodules", type="build")
    depends_on("messagefacility")

    depends_on("trace+kmod")

    
