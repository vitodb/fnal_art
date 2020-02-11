# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Larpandoracontent(CMakePackage):
    """Larpandoracontent"""

    homepage = "http://cdcvs.fnal.gov/redmine/projects/larpandoracontent/wiki"
    url      = "http://cdcvs.fnal.gov/projects/larpandoracontent"

    version('3.14.05', git='http://cdcvs.fnal.gov/projects/larpandoracontent', branch='v03_14_05')
    version('03.15.09', tag='v03_15_09', git='http://cdcvs.fnal.gov/projects/larpandoracontent')
    version('03.15.10', tag='v03_15_10', git='http://cdcvs.fnal.gov/projects/larpandoracontent')
    version('03.15.11', tag='v03_15_11', git='http://cdcvs.fnal.gov/projects/larpandoracontent')
    version('03.15.12', tag='v03_15_12', git='http://cdcvs.fnal.gov/projects/larpandoracontent')

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    depends_on('cetmodules', type='build')
    depends_on('eigen+fftw')
    depends_on('pandora')


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
    patch('larpandoracontent.unups.patch')
