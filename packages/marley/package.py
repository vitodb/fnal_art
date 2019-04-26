# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Marley(Package):
    """A Monte Carlo event generator for tens-of-MeV neutrino-nucleus
       interactions in liquid argon"""

    homepage = "httpd://github.com/sjgardiner/marley"
    url      = "https://github.com/sjgardiner/marley/archive/v1.0.0.tar.gz"

    version('1.0.0', sha256='4dea9918cff0aed3b9c38f74351c373c32235496ca6e321078f2c7b56bce719e')

    depends_on('root')

    patch('marley-1.0.0.patch', when='@1.0.0')

    def install(self, spec, prefix):
        with working_dir('build'):
            make('CXXFLAGS=-std=c++17 -I../include')
            make('prefix={0}'.format(prefix), 'install')
