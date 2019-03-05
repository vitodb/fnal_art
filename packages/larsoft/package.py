# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Larsoft(CMakePackage):
    """Larsoft"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larsoft"
    url      = "http://cdcvs.fnal.gov/projects/larsoft"

    version('develop', git='http://cdcvs.fnal.gov/projects/larsoft', branch='develop')

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    patch('patch')

    depends_on('lareventdisplay')
    depends_on('larexamples')
    depends_on('larana')
    depends_on('larreco')
    depends_on('larg4')
    depends_on('larpandora')
    depends_on('larwirecell')
    depends_on('larsoftobj')
    depends_on('larsoft-data')
    depends_on('ifdh-art')
    depends_on('cetmodules', type='build')

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value),
                '-DROOT_BASIC_LIB_LIST=Core;RIO;Net;Imt;Hist;Graf;Graf3d;Gpad;Tree;Rint;Postscript;Matrix;Physics;MathCore;Thread'
               ]
        return args

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('LARSOFT_INC',dspec['larsoft'].prefix.include)
        spack_env.set('LARSOFT_LIB', dspec['larsoft'].prefix.lib)
