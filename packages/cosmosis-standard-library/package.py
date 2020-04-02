# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class CosmosisStandardLibrary(MakefilePackage):

    homepage = "https://www.example.com"
    url      = "https://bitbucket.org/joezuntz/cosmosis-standard-library/get/v1.6.2.tar.bz2"

    version('1.6.2', sha256='830dda7c4bbd54ebb7b9806d563982d5a180094824213fb74543b21c5f74dc44')

    phases = ['install']
    def install(self, spec, prefix):
        install_tree('.', prefix)
