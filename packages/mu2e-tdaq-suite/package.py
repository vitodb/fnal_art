# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *

class Mu2eTdaqSuite(BundlePackage):
    """The Mu2e TDAQ Suite, the software used for Mu2e trigger and data acquisition
    """

    version("develop")
    version("v1_02_03")
    version("v1_02_02")
    
    squals = ("112", "117", "118", "122", "123")
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

    variant(
        "artdaq",
        default="0",
        values = ("0","31202","31203"),
        multi=False,
        description="Artdaq suite version to use",
    )   
    depends_on("artdaq-suite@v3_12_03", when="artdaq=31203")
    depends_on("artdaq-suite@v3_12_02", when="artdaq=31202")
    depends_on("artdaq-suite+db+epics~demo~pcp")

    variant("otsdaq",
            default="0",
            values = ("0", "20608", "20609"),
            multi=False,
            description="Otsdaq version to use",
    )
    depends_on("otsdaq-suite@v2_06_09", when="otsdaq=20609")
    depends_on("otsdaq-suite@v2_06_08", when="otsdaq=20608")
    depends_on("otsdaq-suite")

    with when("@v1_02_02"):
        depends_on("mu2e-pcie-utils@v2_08_00")
        depends_on("artdaq-core-mu2e@v1_08_04")
        depends_on("artdaq-mu2e@v1_05_02")
        depends_on("otsdaq-mu2e@v1_02_02")
        
    with when("@develop"):
        depends_on("mu2e-pcie-utils")
        depends_on("artdaq-core-mu2e")
        depends_on("artdaq-mu2e")
        depends_on("otsdaq-mu2e")
