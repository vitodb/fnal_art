# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Marley(Package):

    homepage = "http://www.example.com"
    url      = "http://www.example.com/example-1.2.3.tar.gz"

    version('0.0', '')

    def install(self, spec, prefix):
        make()
        make('install')
