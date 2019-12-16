# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cetmodules(CMakePackage):
    """CMake glue modules and scripts required by packages originating at
    Fermilab and associated experiments and other collaborations.
    """

    homepage = 'http://cdcvs.fnal.gov/projects/cetmodules'

    version('develop', branch='develop', git=homepage)
    version('1.04.00', sha256='4ba077e7146e19a805476f2fcf2a537a2cd24dbd602f5f5c348431b5018379da')
    version('1.03.00', sha256='40b0f8fa88f9522d14cae87a4242a494aa724b13505b6b740a0007153cc85e18')
    version('1.02.04', sha256='4e5063748aa8821b34a2a3ae150927afcd890beade83ad98e03f93e5d93d8ee7')
    version('1.02.03', sha256='04cf68a443e7701985e9e72fcc26e5fdfa46304b01c9295a4f0b526eeafa1b63')
    version('1.02.02', sha256='b7bd22219afe34942d29287df4d864eb1a6114eed0ebf2c5d3912884d6c2594a')
    version('1.02.01', sha256='6357771a5dd56dc25f0211d491d30cea6fe48114a18ef82e17f848a04d0cbc88')
    version('1.02.00', sha256='1a72b77730efd5efff56218f950917c3c3b6b4f157d4b16c1d1bb4e40cbd760f')
    version('1.01.03', sha256='6f9168e7f638aa6e7b7798fac384a38f825518e7599e24daeaf0551b6dc3f0fd')
    version('1.01.02', sha256='dddc8992f011fec77d152990dc89ac1027b280bb31c3e5ac093b2945847d74c7')
    version('1.01.01', sha256='0b7e28d4c29c9941a6960609e8ab4aa33f90736ef1dc81fc7b1b520e99ee0ae7')
    version('1.01.00', sha256='80bf9a77852751f90b1446e5d5966bea9b73d5b35e024195b35c851dc93a5443')
    version('1.00.00', sha256='67438bb1ee9acdaadb6e245ff670463c4603c3283c69b3c9d1a04d6ee9a3fd16')
    version('0.07.00', '60fb6f9ff26605ea4c0648fa43d0a516')

    depends_on('cmake@3.11:', type='build', when='@:1.01.99')
    depends_on('cmake@3.12:', type='build', when='@1.02.00:')

    def url_for_version(self, version):
        url = 'http://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/{0}.v{1}.tbz2'
        return url.format(self.name, version.underscored)
