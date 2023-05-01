# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack import *


class ArtdaqCore(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
    event building, event reconstruction and analysis (using the art analysis
    framework), process management, system and process state behavior, control
    messaging, local message logging (status and error messages), DAQ process
    and art module configuration, and the writing of event data to disk in ROOT
    format."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/artdaq/wiki"
    url = "https://github.com/art-daq/artdaq_core/archive/refs/tags/v3_09_04.tar.gz"
    git = "https://github.com/art-daq/artdaq_core.git"

    version("develop", branch="develop", get_full_repo=True)
    version("v3_09_08", sha256="5689cdf8384276835be9dfd50489917d3729242833f9f2da115445d9245978b2")
    version("v3_09_07", sha256="3bf9285171c86e9f039e5d48a99b577544ab4a17d6f4a4f1a79d6bfb797eeede")
    version("v3_09_04", sha256="8d4315e0ebe7b663d171352d8e08dd87393d34319f672837eb8c93ea83b8ba63")

    def url_for_version(self, version):
        url = "https://github.com/art-daq/artdaq_core/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    variant(
        "cxxstd",
        default="17",
        values=("14", "17"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    # art dependencies
    depends_on("canvas-root-io")
    depends_on("cetmodules", type="build")

    # artdaq dependencies
    depends_on("trace+mf")
