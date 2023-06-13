# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack import *


class Otsdaq(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
    event building, event reconstruction and analysis (using the art analysis
    framework), process management, system and process state behavior, control
    messaging, local message logging (status and error messages), DAQ process
    and art module configuration, and the writing of event data to disk in ROOT
    format."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/artdaq/wiki"
    url = "https://github.com/art-daq/otsdaq/archive/refs/tags/v2_06_08.tar.gz"
    git = "https://github.com/art-daq/otsdaq.git"

    version("develop", branch="develop", get_full_repo=True)
    version("v2_06_10", sha256="c876cb556451063513b8d4f49dd9d329769f62ad1c05357017729c0e07ccdf39")
    version("v2_06_09", sha256="921c9c603439950ca4d5c2bf756053ec260d839e3ca6214b023616a9d94ed9e8")
    version("v2_06_08", sha256="cf377646249f018e3a19890000a82d2513c7ebe853244b6b23bc82a5379c2500")
    version("v2_06_07", sha256="825cc7ba889e5be37ff2494b62e515d0e1544cb02e44e55b5e3e4e97f2179171")

    def url_for_version(self, version):
        url = "https://github.com/art-daq/otsdaq/archive/refs/tags/{0}.tar.gz"
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
    depends_on("xdaq")

    depends_on("artdaq")
    depends_on("artdaq-database~builtin_fhicl")
    depends_on("artdaq-daqinterface")
