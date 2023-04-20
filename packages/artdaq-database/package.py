# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack import *


class ArtdaqDatabase(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
    event building, event reconstruction and analysis (using the art analysis
    framework), process management, system and process state behavior, control
    messaging, local message logging (status and error messages), DAQ process
    and art module configuration, and the writing of event data to disk in ROOT
    format."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/artdaq/wiki"
    url = "https://github.com/art-daq/artdaq_database/archive/refs/tags/v1_07_02.tar.gz"
    git = "https://github.com/art-daq/artdaq_database.git"

    version("develop", branch="develop", get_full_repo=True)
    version("v1_07_03", sha256="670a5d44236091bdb85ca643e27dc59fd263fdb2a7dcbeaa7ec04e2b5f67df40")
    version("v1_07_02", sha256="8cb937967d16f25b59ee8e7104cd968956d892dbe24b29e393c5db982969e432")

    def url_for_version(self, version):
        url = "https://github.com/art-daq/artdaq_database/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    variant(
        "cxxstd",
        default="17",
        values=("14", "17"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )
    variant("builtin_fhicl", default=True, description="Use built-in FHiCL-cpp with database fixes")

    depends_on("curl")
    depends_on("boost+filesystem+program_options")
    depends_on("swig", type="build")
    depends_on("node-js", type="build")
    depends_on("python", type="build")

    depends_on("cetmodules", type="build")

    depends_on("cetlib", when="~builtin_fhicl")

    depends_on("trace+mf")

    def cmake_args(self):
        args = [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
                "-DUSE_FHICLCPP={0}".format("TRUE" if "+builtin_fhicl" in self.spec else "FALSE")]
        return args
