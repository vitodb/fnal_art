# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from llnl.util import filesystem

import os,glob,inspect

class Genie(AutotoolsPackage):
    """GENIE is an international collaboration of scientists that plays the 
leading role in the development of comprehensive physics models for 
the simulation of neutrino interactions, and performs a highly-developed
global analysis of neutrino scattering data. 
"""

    homepage = "http://www.genie-mc.org"
    url      = "https://github.com/GENIE-MC/Generator/archive/R-2_12_10.tar.gz"

    version('3_00_02', sha256='34d6c37017b2387c781aea7bc727a0aac0ef45d6b3f3982cc6f3fc82493f65c3')
    version('3_0_0b4', sha256='41100dd5141a7e2c934faaaf22f244deda08ab7f03745976dfed0f31e751e24e')
    version('3_0_0b3', sha256='96b849d426f261a858f5483f1ef576cc15f5303bc9c217a194de2500fb59cc56')
    version('3_0_0b2', sha256='2884f5cb80467d3a8c11800421c1d1507e9374a4ba2fbd654d474f2676be28ba')
    version('3_0_0b1', sha256='e870146bfa674235c3713a91decf599d2e90b4202f8b277bf49b04089ee432c1')
    version('3_00_00', sha256='3953c7d9f1f832dd32dfbc0b9260be59431206c204aec6ab0aa68c01176f2ae6')
    version('2_12_10', sha256='c8762db3dcc490f80f8a61268f5b964d4d35b80134b622e89fe2307a836f2a0b')
    version('2_12_8',  sha256='7ca169a8d9eda7267d28b76b2f3110552852f8eeae263a03cd5139caacebb4ea')
    version('2_12_6',  sha256='3b450c609875459798ec98e12cf671cc971cbb13345af6d75bd6278d422f3309')
    version('2_12_4',  sha256='19a4a1633b0847a9f16a44e0c74b9c224ca3bb93975aecf108603c22e807517b')

    parallel = False

    depends_on('root+pythia6')
    depends_on('lhapdf')
    depends_on('pythia6+root')
    depends_on('libxml2+python')
    depends_on('log4cpp')
    depends_on('gsl')

    variant('cxxstd',
            default='17',
            values=('default', '98', '11', '14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    patch('patch/genie-r21210.patch', when='@2_12_10')

    @property
    def build_targets(self):
        cxxstd = self.spec.variants['cxxstd'].value
        cxxstdflag = '' if cxxstd == 'default' else \
                     getattr(self.compiler, 'cxx{0}_flag'.format(cxxstd))
        args = ['GOPT_WITH_CXX_USERDEF_FLAGS=-g -fno-omit-frame-pointer {0}'.
                format(cxxstdflag)]
        return args

    def configure_args(self):
        args = [
                '---prefix={0}'.format(self.prefix),
                '--enable-rwght',
                '--enable-fnal',
                '--enable-atmo',
                '--enable-event-server',
                '--enable-nucleon-decay',
                '--enable-neutron-osc',
                '--enable-vle-extension',
                '--with-pythia6-lib={0}'.format(self.spec['pythia6'].prefix.lib),
                '--with-libxml2-inc={0}/libxml2'.format(self.spec['libxml2'].prefix.include),
                '--with-libxml2-lib={0}'.format(self.spec['libxml2'].prefix.lib),
                '--with-log4cpp-inc={0}'.format(self.spec['log4cpp'].prefix.include),
                '--with-log4cpp-lib={0}'.format(self.spec['log4cpp'].prefix),
                '--with-optimiz-level=O3'
                ]
        if self.spec.satisfies('@3.00.00:'):
            args.extend(['--enable-lhapdf5',
                         '--with-lhapdf5-lib={0}'.format(self.spec['lhapdf'].prefix.lib),
                         '--with-lhapdf5-inc={0}'.format(self.spec['lhapdf'].prefix.include)])
        else:
            args.extend(['--enable-lhapdf',
                         '--with-lhapdf-lib={0}'.format(self.spec['lhapdf'].prefix.lib),
                         '--with-lhapdf-inc={0}'.format(self.spec['lhapdf'].prefix.include)])
        return args

    @run_before('configure')
    def add_to_configure_env(self):
        inspect.getmodule(self).configure.add_default_env('GENIE',self.stage.source_path)

    @run_before('build')
    def add_to_make_env(self):
        inspect.getmodule(self).make.add_default_env('GENIE',self.stage.source_path)
        inspect.getmodule(self).make.add_default_env('LD_LIBRARY_PATH', '{0}/lib'.format(self.stage.source_path))

    @run_after('install')
    def install_required_src(self):
        # Install things from the source tree that are required.
        filesystem.install_tree(os.path.join(self.stage.source_path, 'src', 'scripts'),
                                os.path.join(self.prefix, 'src', 'scripts'))
        src_make_dir = os.path.join(self.prefix, 'src', 'make', '')
        filesystem.mkdirp(src_make_dir)
        filesystem.install(os.path.join(self.stage.source_path, 'src', 'make', 'Make.config_no_paths'),
                           src_make_dir)

    def setup_environment(self, spack_env, run_env):
        run_env.set('GENIE', self.prefix)
        spack_env.set('GENIE_VERSION','v{0}'.format(self.version.underscored))
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(root=False, cover='nodes', order='post',
                                    deptype=('link'), direction='children'):
            spack_env.prepend_path('ROOT_INCLUDE_PATH',
                                   str(self.spec[d.name].prefix.include))
            run_env.prepend_path('ROOT_INCLUDE_PATH',
                                 str(self.spec[d.name].prefix.include))

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('GENIE',self.prefix)
        run_env.set('GENIE', self.prefix)
        spack_env.prepend_path('PATH', self.prefix.bin)
        run_env.prepend_path('PATH', self.prefix.bin)
        spack_env.append_path('ROOT_INCLUDE_PATH', '{0}/GENIE'.format(self.prefix.include))
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        spack_env.append_path('LD_LIBRARY_PATH', self.prefix.lib)

