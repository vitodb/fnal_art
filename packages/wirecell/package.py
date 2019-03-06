# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Wirecell(Package):
    """Wire Cell Toolkit provides simulation, signal processing and reconstruction for LArTPC
    Borrowed from 
    https://github.com/WireCell/wire-cell-spack/blob/master/repo/packages/wirecell-toolkit/package.py"""

    homepage = "http://wirecell.github.io"

    version('0.10.9', git="https://github.com/WireCell/wire-cell-build.git", tag="0.10.9", submodules=True)

    depends_on("jsoncpp")
    depends_on("jsonnet")

    depends_on("fftw")
    depends_on("eigen+fftw@3.3.4")


    # Do not currently make use of TBB.  When we get back to this,
    # probably best to build ROOT with TBB support as well.
    # depends_on("tbb")
    depends_on("root@6:")

    # match what is listed in wire-cell-build/wscript
    depends_on("boost+graph+iostreams+filesystem+system+thread+program_options")


    def install(self, spec, prefix):

        cfg = "wcb"
        cfg += " --prefix=%s" % prefix
        cfg += " --boost-mt"
        cfg += " --boost-libs=%s --boost-includes=%s" % \
               (spec["boost"].prefix.lib, spec["boost"].prefix.include)
        cfg += " --with-root=%s" % spec["root"].prefix
        cfg += " --with-eigen=%s" % spec["eigen"].prefix
        cfg += " --with-eigen-include=%s" % spec["eigen"].prefix.include.eigen3
        cfg += " --with-jsoncpp=%s" % spec["jsoncpp"].prefix
        cfg += " --with-jsonnet=%s" % spec["jsonnet"].prefix
#        cfg += " --with-tbb=%s" % spec["tbb"].prefix
        cfg += " --with-tbb=false" # for now
        cfg += " --with-fftw=%s" % spec["fftw"].prefix
        cfg += " --build-debug=-std=c++17"

        cfg += " configure"
        python(*cfg.split())
        python("wcb","-vv")
        python("wcb", "install")
        return
