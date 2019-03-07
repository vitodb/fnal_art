# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Pandora(CMakePackage):
    """PandoraPFA Multi-algorithm pattern recognition"""

    homepage = "https://github.com/PandoraPFA"

    version('03.11.01', git='https://github.com/PandoraPFA/PandoraPFA', tag='v03-11-01')
 
    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    depends_on('root')

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.format(self.spec.variants['cxxstd'].value),
                '-DCMAKE_CXX_FLAGS=-std=c++17 -Wno-implicit-fallthrough',
                '-DCMAKE_MODULE_PATH={0}/etc/cmake'.format(self.spec['root'].prefix),
                '-DPANDORA_MONITORING=ON', '-DPANDORA_EXAMPLE_CONTENT=OFF', '-DPANDORA_LAR_CONTENT=OFF' '-DPANDORA_LC_CONTENT=OFF']
        return args
