# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import os
import sys
libdir="%s/var/spack/repos/fnal_art/lib" % os.environ["SPACK_ROOT"]
if not libdir in sys.path:
    sys.path.append(libdir)


def patcher(x):
    cetmodules_20_migrator(".","larpandoracontent","3.15.15")

class Larpandoracontent(CMakePackage):
    """Larpandoracontent"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larpandoracontent/wiki"
    url      = "https://github.com/LArSoft/larpandoracontent.git"
    version('03.22.11.01', tag='v03_22_11_01', git='https://github.com/LArSoft/larpandoracontent.git', get_full_repo=True)

    version('3.22.09', git='https://github.com/LArSoft/larpandoracontent.git', branch='v03_22_09')
    version('3.22.01', git='https://github.com/LArSoft/larpandoracontent.git', branch='v03_22_01')
    version('3.14.05', git='https://github.com/LArSoft/larpandoracontent.git', branch='v03_14_05')
    version('03.15.09', tag='v03_15_09', git='https://github.com/LArSoft/larpandoracontent.git', get_full_repo=True)
    version('03.15.10', tag='v03_15_10', git='https://github.com/LArSoft/larpandoracontent.git', get_full_repo=True)
    version('03.15.11', tag='v03_15_11', git='https://github.com/LArSoft/larpandoracontent.git', get_full_repo=True)
    version('03.15.12', tag='v03_15_12', git='https://github.com/LArSoft/larpandoracontent.git', get_full_repo=True)
    version('03.15.13', tag='v03_15_13', git='https://github.com/LArSoft/larpandoracontent.git', get_full_repo=True)
    version('03.15.14', tag='v03_15_14', git='https://github.com/LArSoft/larpandoracontent.git', get_full_repo=True)
    version('03.15.15', tag='v03_15_15', git='https://github.com/LArSoft/larpandoracontent.git', get_full_repo=True)
    version('03.15.16', tag='v03_15_16', git='https://github.com/LArSoft/larpandoracontent.git', get_full_repo=True)

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')



    depends_on('cetmodules', type='build')
    depends_on('eigen')
    depends_on('pandora')
    depends_on('py-torch')


    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value),
                '-DCMAKE_MODULE_PATH={0}/cmakemodules'.format(self.spec['pandora'].prefix),
                '-DPANDORA_MONITORING=ON',
                '-DLAR_CONTENT_LIBRARY_NAME=LArPandoraContent',
                '-DPandoraSDK_DIR={0}/cmakemodules'.format(self.spec['pandora'].prefix),
                '-DPandoraMonitoring_DIR={0}/cmakemodules'.format(self.spec['pandora'].prefix),
               ]
        return args
