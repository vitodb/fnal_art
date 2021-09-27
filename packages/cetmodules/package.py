# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import sys


class Cetmodules(CMakePackage):
    """CMake glue modules and scripts required by packages originating at
    Fermilab and associated experiments and other collaborations.
    """

    homepage = 'https://cdcvs.fnal.gov/redmine/projects/cetmodules'
    git_base = 'https://github.com/FNALssi/cetmodules.git'
    url = 'https://github.com/FNALssi/cetmodules/archive/refs/tags/2.14.00.tar.gz'

    version('develop', branch='develop', git=git_base, get_full_repo=True)

    #version('2.25.01', sha256='cb58c8a759589e08dcd11e6a9bf6341a130d18e2cbe53abc359a7514aacba5b2')

    version('2.16.02', sha256='43082380b23b3367303368b6ec698d7a3624b19a8a99842752bd13bcb474625e')

    version('2.14.00', sha256='360b719133d644d47f092f42895f3037891cfb30adf6897472f62f037a3129f1')

    version('2.09.00', sha256='8c4d9a5f3d39a7dff5e9136576dab1bcf50a410c6cc028e5b47a2546c57e3860')

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
    version('0.07.00', md5='60fb6f9ff26605ea4c0648fa43d0a516')

    depends_on('cmake@3.11:', type='build', when='@:1.01.99')
    depends_on('cmake@3.12:', type='build', when='@1.02.00:')
    depends_on('cmake@3.18:', type='build', when='@2.07.00:')
    depends_on('py-sphinxcontrib-moderncmakedomain', when='@2.00.10:', type='build')
    depends_on('py-sphinxcontrib-moderncmakedomain', when='@develop',type='build')
    depends_on('py-sphinx-rtd-theme', when='@2.00.10:',type='build')
    depends_on('py-sphinx-rtd-theme', when='@develop',type='build')

    @run_before('cmake')
    def fix_fix_man(self):
        filter_file('exit \$status', 'exit 0', '%s/libexec/fix-man-dirs' % self.stage.source_path)

    def url_for_version(self, version):
        if str(version)[0] in "01":
            url = 'https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/v{0}.{1}.tbz2'
            return url.format(self.name, version.underscored)
        else:
            url = 'https://github.com/FNALssi/{0}/archive/refs/tags/{1}.tar.gz'
            return url.format(self.name, version)


    @run_after('install')
    def rename_README(self):
        import os
        if os.path.exists(join_path(self.spec.prefix, "README")):
            os.rename( join_path(self.spec.prefix, "README"),
                       join_path(self.spec.prefix, "README_%s"%self.spec.name))
