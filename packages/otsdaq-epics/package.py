# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack import *


class OtsdaqEpics(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
    event building, event reconstruction and analysis (using the art analysis
    framework), process management, system and process state behavior, control
    messaging, local message logging (status and error messages), DAQ process
    and art module configuration, and the writing of event data to disk in ROOT
    format."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/artdaq/wiki"
    url = "https://github.com/art-daq/otsdaq_epics/archive/refs/tags/v2_06_08.tar.gz"
    git = "https://github.com/art-daq/otsdaq_epics.git"

    version("develop", branch="develop", get_full_repo=True)
    version("v2_06_09", sha256="96c5e5b9a88fd0f18a6682d210bde83dbad7a25b9c8ca5ce4acf072cf02702a8")
    version("v2_06_08", sha256="5f24df325f4e27dfbd5a30892a80ba75a3eef642d60a759d1580f846f2e22813")

    def url_for_version(self, version):
        url = "https://github.com/art-daq/otsdaq_epics/archive/refs/tags/{0}.tar.gz"
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
    depends_on("libpqxx")

    depends_on("otsdaq")
    depends_on("otsdaq-utilities")


