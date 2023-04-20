# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack import *


class ArtdaqDaqinterface(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
    event building, event reconstruction and analysis (using the art analysis
    framework), process management, system and process state behavior, control
    messaging, local message logging (status and error messages), DAQ process
    and art module configuration, and the writing of event data to disk in ROOT
    format."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/artdaq/wiki"
    url = "https://github.com/art-daq/artdaq_daqinterface/archive/refs/tags/v3_12_02.tar.gz"
    git = "https://github.com/art-daq/artdaq_daqinterface.git"

    def url_for_version(self, version):
        url = "https://github.com/art-daq/artdaq_daqinterface/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    version("develop", branch="develop", get_full_repo=True)
    version("v3_12_03", sha256="d56efaa1af93d07acb5e7139c608141f72dfb1a6166e5f25107dc518dfe49f30")
    version("v3_12_02", sha256="b1a6d45d6723ec697bec1c0a50eac34605bd6c5f4becf5b76f0aeac96c54f8ac")

    variant(
        "cxxstd",
        default="17",
        values=("14", "17"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("cetmodules", type="build")
    depends_on("python@3:")
