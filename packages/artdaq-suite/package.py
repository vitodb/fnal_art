# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class ArtdaqSuite(BundlePackage):
    """The artdaq suite; artdaq is a data acquisition framework that leverages the analysis capabilities of art"""

    homepage="https://github.com/art-daq"

    version("v3_12_04")
    version("v3_12_03")
    version("v3_12_02")

    squals = ("112", "117", "118", "120", "120a", "122", "123", "124")
    variant(
        "s",
        default="0",
        values=("0",) + squals,
        multi=False,
        description="Art suite version to use",
    )
    for squal in squals:
        depends_on(f"art-suite@s{squal}+root", when=f"s={squal}")
    depends_on("art-suite+root", when="s=0")

    variant("demo", default=False, description="Also install artdaq_demo components")
    variant("db", default=True, description="Install artdaq_database")
    variant("epics", default=True, description="Install artdaq EPICS plugin")
    variant("pcp", default=True, description="Install artdaq PCP MMV plugin")

    with when("@v3_12_04"):
        depends_on("artdaq@v3_12_04")
        depends_on("artdaq-core@v3_09_12")
        depends_on("artdaq-utilities@v1_08_04")
        depends_on("artdaq-mfextensions@v1_08_04")
        depends_on("trace@v3_17_09")
        depends_on("artdaq-daqinterface@v3_12_04")
        depends_on("artdaq-core-demo@v1_10_04", when="+demo")
        depends_on("artdaq-demo@v3_12_04", when="+demo")
        depends_on("artdaq-database@v1_07_04", when="+db")
        depends_on("artdaq-epics-plugin@v1_05_04", when="+epics")
        depends_on("artdaq-pcp-mmv-plugin@v1_03_04", when="+pcp")
    with when("@v3_12_03"):
        depends_on("artdaq@v3_12_03")
        depends_on("artdaq-core@v3_09_08")
        depends_on("artdaq-utilities@v1_08_03")
        depends_on("artdaq-mfextensions@v1_08_03")
        depends_on("trace@v3_17_09")
        depends_on("artdaq-daqinterface@v3_12_03")
        depends_on("artdaq-core-demo@v1_10_03", when="+demo")
        depends_on("artdaq-demo@v3_12_03", when="+demo")
        depends_on("artdaq-demo-hdf5@v1_04_03", when="+demo")
        depends_on("artdaq-database@v1_07_03", when="+db")
        depends_on("artdaq-epics-plugin@v1_05_03", when="+epics")
        depends_on("artdaq-pcp-mmv-plugin@v1_03_03", when="+pcp")
    with when("@v3_12_02"):
        depends_on("artdaq@v3_12_02")
        depends_on("artdaq-core@v3_09_04")
        depends_on("artdaq-utilities@v1_08_02")
        depends_on("artdaq-mfextensions@v1_08_02")
        depends_on("trace@v3_17_07")
        depends_on("artdaq-daqinterface@v3_12_02")
        depends_on("artdaq-core-demo@v1_10_02", when="+demo")
        depends_on("artdaq-demo@v3_12_02", when="+demo")
        depends_on("artdaq-demo-hdf5@v1_04_02", when="+demo")
        depends_on("artdaq-database@v1_07_02", when="+db")
        depends_on("artdaq-epics-plugin@v1_05_02", when="+epics")
        depends_on("artdaq-pcp-mmv-plugin@v1_03_02", when="+pcp")
