# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from re import A
import sys

from spack.package import *

def sanitize_environments(env, *vars):
    for var in vars:
        env.prune_duplicate_paths(var)
        env.deprioritize_system_paths(var)


class Xdaq(MakefilePackage):
    """Programming library for writing an XML-RPC server or client in
    C or C++."""

    homepage = "https://gitlab.cern.ch/cmsos/core"
    url = "https://gitlab.cern.ch/cmsos/core/-/archive/release_16_21_0_2/core-release_16_21_0_2.tar.gz"
    git = "https://gitlab.cern.ch/cmsos/core.git"
    
    version("16_21_0_2", commit="d9864267e19543240e655e0c61a376e2e689354d", get_full_repo=True)
    version("16_26_0_3", sha256="cd425bfde654f108f6634b1a8f7f2af8549fd2386b8ea5f0e47d3d8042c9519e")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("numactl")
    depends_on("libtirpc")
    depends_on("libelf")

    patch("mfDefs.core.patch")
    patch("build.Makefile.rules.patch")
    patch("build.mfDefs.linux.patch")
    patch("build.mfDefs.linux.2.patch")
    patch("extern.asyncresolv.configure.patch.patch")
    patch("extern.i2o.Makefile.patch")
    patch("extern.log4cplus.Makefile.patch")
    patch("extern.mimetic.patch")
    patch("extern.xalan.Makefile.patch")
    patch("toolbox.includes.patch")
    patch("toolbox.Makefile.patch")
    patch("toolbox.src.GNUC.patch")

    #depends_on("xerces-c")
    depends_on("nlohmann-json")
    depends_on("log4cplus")
    #depends_on("xalan-c")
    depends_on("jansson")


    def build(self, spec, prefix):
        # Removed "extern/nlohmannjson", "extern/log4cplus", "extern/jansson"
        externPackages=["extern/xerces", "extern/asyncresolv", "extern/i2o", "extern/cgicc",  "extern/xalan", "extern/mimetic"]

        Packages=["config", "xcept", "log/udpappender", "log/xmlappender", "toolbox",
 "xoap", "xoap/filter", "xdata", "pt", "xgi", "i2o", "xdaq", "i2o/utils", "pt/http", 
"pt/fifo", "executive", "hyperdaq", "xrelay", "b2in/nub", "b2in/utils", "b2in/eventing"]

        for extpackage in externPackages:
            make("Packages=" + extpackage, "CC="+env['CC'], "CXX="+env['CXX'], "install")
        for package in Packages:
            make("Packages="+package, "CC="+env['CC'], "CXX="+env['CXX'], "LD="+env['CXX'])
            make("-C" + package, "CC="+env['CC'], "CXX="+env['CXX'], "LD="+env['CXX'], "install")

    def install(self, spec, prefix):
        install_tree("./x86_64_slc6", prefix)
        install_tree("./x86_64_slc6/include/linux", os.path.join(prefix,"include"))

    def setup_build_environment(self, env):
        prefix = self.build_directory
        # Binaries.
        env.prepend_path("PATH", os.path.join(prefix, "bin"))

        # XDAQ Variables
        env.set("XDAQ_ROOT", prefix)
        env.set("XDAQ_DOCUMENT_ROOT", os.path.join(prefix, "htdocs"))
        env.set("XDAQ_OS", "linux")
        env.set("XDAQ_PLATFORM", "x86_64_slc6")
        env.set("XDAQ_SETUP_ROOT", os.path.join(prefix, "share"))
        env.set("BUILD_HOME", prefix)
        env.set("PROJECT_NAME", "core")
        env.set("BUILD_SUPPORT", "build")


        # Cleaup.
        sanitize_environments(env, "PATH")

    def setup_run_environment(self, env):
        prefix = self.prefix
        # Binaries.
        env.prepend_path("PATH", os.path.join(prefix, "bin"))

        # XDAQ Variables
        env.set("XDAQ_ROOT", prefix)
        env.set("XDAQ_DOCUMENT_ROOT", os.path.join(prefix, "htdocs"))
        env.set("XDAQ_OS", "linux")
        env.set("XDAQ_PLATFORM", "x86_64_slc6")
        env.set("XDAQ_SETUP_ROOT", os.path.join(prefix, "share"))

        # Cleaup.
        sanitize_environments(env, "PATH")

    def setup_dependent_build_environment(self, env, dependent_spec):
        prefix = self.prefix
        # Binaries.
        env.prepend_path("PATH", os.path.join(prefix, "bin"))

        # XDAQ Variables
        env.set("XDAQ_ROOT", prefix)
        env.set("XDAQ_DOCUMENT_ROOT", os.path.join(prefix, "htdocs"))
        env.set("XDAQ_OS", "linux")
        env.set("XDAQ_PLATFORM", "x86_64_slc6")
        env.set("XDAQ_SETUP_ROOT", os.path.join(prefix, "share"))
        env.set("BUILD_HOME", prefix)
        env.set("PROJECT_NAME", "core")
        env.set("BUILD_SUPPORT", "build")

        # Cleaup.
        sanitize_environments(env, "PATH")

    def setup_dependent_run_environment(self, env, dependent_spec):
        prefix = self.prefix
        # Binaries.
        env.prepend_path("PATH", os.path.join(prefix, "bin"))

        # XDAQ Variables
        env.set("XDAQ_ROOT", prefix)
        env.set("XDAQ_DOCUMENT_ROOT", os.path.join(prefix, "htdocs"))
        env.set("XDAQ_OS", "linux")
        env.set("XDAQ_PLATFORM", "x86_64_slc6")
        env.set("XDAQ_SETUP_ROOT", os.path.join(prefix, "share"))

        # Cleaup.
        sanitize_environments(env, "PATH")
