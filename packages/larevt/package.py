# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Larevt(CMakePackage):
    """Larevt"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larevt"
    url      = "http://cdcvs.fnal.gov/projects/larevt"

    version('develop', git='http://cdcvs.fnal.gov/projects/larevt', branch='develop')

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    patch('patch')

    depends_on('libwda')
    depends_on('lardata')
    depends_on('cetmodules', type='build')

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value),
                '-DROOT_BASIC_LIB_LIST=Core;RIO;Net;Imt;Hist;Graf;Graf3d;Gpad;Tree;Rint;Postscript;Matrix;Physics;MathCore;Thread'
               ]
        return args

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('LAREVT_INC',dspec['larevt'].prefix.include)
        spack_env.set('LAREVT_LIB', dspec['larevt'].prefix.lib)
