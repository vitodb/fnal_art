# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class Jsonnet(Package):
    "A data templating language looking like JSON that produces JSON."

    homepage = "http://jsonnet.org"
    url      = "https://github.com/google/jsonnet/archive/v0.9.3.tar.gz"

    version('0.12.1', sha256='257c6de988f746cc90486d9d0fbd49826832b7a2f0dbdb60a515cc8a2596c950')
    version('0.12.0', sha256='9285f44f73a61fbfb61b3447a622e8aff0c61580c61c4a92f69d463ea7f1624a')
    version('0.11.2', sha256='c7c33f159a9391e90ab646b3b5fd671dab356d8563dc447ee824ecd77f4609f8')

    #depends_on('bazel', type='build')

    def install(self, spec, prefix):
        'Install JSonnet'
        # This can use bazel but we fall back to the crude Makefile in order to
        # avoid the dependency on bazel which brings in JDK.
        make()
        make("libjsonnet.so")
        make("libjsonnet++.so")
        mkdirp(prefix.bin)
        install("jsonnet", prefix.bin)
        mkdirp(prefix.lib)
        install("libjsonnet.so", prefix.lib)
        install("libjsonnet++.so", prefix.lib)
        mkdirp(prefix.include)
        install("include/libjsonnet.h", prefix.include)
        install("include/libjsonnet++.h", prefix.include)
