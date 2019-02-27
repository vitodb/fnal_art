# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os,glob

class Genie(Package):
    """GENIE is an international collaboration of scientists that plays the 
leading role in the development of comprehensive physics models for 
the simulation of neutrino interactions, and performs a highly-developed
global analysis of neutrino scattering data. 
"""

    homepage = "http://www.genie-mc.org"
    url      = "https://github.com/GENIE-MC/Generator/archive/R-2_12_10.tar.gz"

    #version('3_00_02', sha256='34d6c37017b2387c781aea7bc727a0aac0ef45d6b3f3982cc6f3fc82493f65c3')
    #version('3_0_0b4', sha256='41100dd5141a7e2c934faaaf22f244deda08ab7f03745976dfed0f31e751e24e')
    #version('3_0_0b3', sha256='96b849d426f261a858f5483f1ef576cc15f5303bc9c217a194de2500fb59cc56')
    #version('3_0_0b2', sha256='2884f5cb80467d3a8c11800421c1d1507e9374a4ba2fbd654d474f2676be28ba')
    #version('3_0_0b1', sha256='e870146bfa674235c3713a91decf599d2e90b4202f8b277bf49b04089ee432c1')
    #version('3_00_00', sha256='3953c7d9f1f832dd32dfbc0b9260be59431206c204aec6ab0aa68c01176f2ae6')
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

    variant('cxxstd',
            default='17',
            values=('default', '98', '11', '14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    patch('patch/genie-r21210.patch', when='@2_12_10')

    def set_cxxstdflag(self):
        cxxstd = self.spec.variants['cxxstd'].value
        cxxstdflag = ''
        if cxxstd == '98':
            cxxstdflag = self.compiler.cxx98_flag
        elif cxxstd == '11':
            cxxstdflag = self.compiler.cxx11_flag
        elif cxxstd == '14':
            cxxstdflag = self.compiler.cxx14_flag
        elif cxxstd == '17':
            cxxstdflag = self.compiler.cxx17_flag
        elif cxxstd == 'default':
            pass
        else:
            # The user has selected a (new?) legal value that we've
            # forgotten to deal with here.
            tty.die(
                "INTERNAL ERROR: cannot accommodate unexpected variant ",
                "cxxstd={0}".format(spec.variants['cxxstd'].value))
        return cxxstdflag

    def setup_environment(self, spack_env, run_env):
        spack_env.append_flags('CXXFLAGS', self.set_cxxstdflag())
        spack_env.set('GENIE',self.stage.source_path)
        spack_env.set('GENIE_VERSION','v{0}'.format(self.version.underscored))
        spack_env.set('GENIE_INC', '{0}/src'.format(self.stage.source_path))
        spack_env.append_path('ROOT_INCLUDE_PATH', '{0}/src'.format(self.stage.source_path))
        spack_env.append_path('LD_LIBRARY_PATH', '{0}/lib'.format(self.stage.source_path))
        spack_env.append_path('PATH', '{0}/bin'.format(self.stage.source_path))

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.append_flags('CXXFLAGS', self.set_cxxstdflag())
        spack_env.set('GENIE',dspec['genie'].prefix)
        spack_env.set('GENIE_VERSION','v{0}'.format(dspec['genie'].version.underscored))
        spack_env.set('GENIE_DIR', '{0}'.format(dspec['genie'].prefix))
        spack_env.set('GENIE_INC', '{0}'.format(dspec['genie'].prefix.include))
        spack_env.set('GENIE_LIB', '{0}'.format(dspec['genie'].prefix.lib))
        spack_env.append_path('ROOT_INCLUDE_PATH', '{0}/GENIE'.format(dspec['genie'].prefix.include))
        spack_env.append_path('LD_LIBRARY_PATH', '{0}'.format(dspec['genie'].prefix.lib))
        spack_env.append_path('PATH', '{0}'.format(dspec['genie'].prefix.bin))

    @run_before('install')
    def create_ver_text(self):
        with open('%s/VERSION'%self.prefix,'w') as f:
          f.write('%s\n'%self.version)

    def install(self, spec, prefix):
        args = [ 
                '---prefix={0}'.format(prefix),
                '--enable-rwght',
                '--enable-fnal',
                '--enable-atmo',
                '--enable-event-server',
                '--enable-nucleon-decay',
                '--enable-neutron-osc',
                '--enable-vle-extension',
                '--with-pythia6-lib={0}'.format(self.spec['pythia6'].prefix.lib),
                '--with-libxml2-inc={0}'.format(self.spec['libxml2'].prefix.include),
                '--with-libxml2-lib={0}'.format(self.spec['libxml2'].prefix.lib),
                '--with-log4cpp-inc={0}'.format(self.spec['log4cpp'].prefix.include),
                '--with-log4cpp-lib={0}'.format(self.spec['log4cpp'].prefix)
                ]
        extargs=['--enable-lhapdf',
                 '--with-lhapdf-lib={0}'.format(self.spec['lhapdf'].prefix.lib),
                 '--with-lhapdf-inc={0}'.format(self.spec['lhapdf'].prefix.include)]
        if spec.satisfies('@3.00.00:'):
            extargs=['--enable-lhapdf5',
                     '--with-lhapdf5-lib={0}'.format(self.spec['lhapdf'].prefix.lib),
                     '--with-lhapdf5-inc={0}'.format(self.spec['lhapdf'].prefix.include)]
        args.extend(extargs)

        configure=Executable('./configure')
        configure.add_default_env('GENIE',self.stage.source_path)
        configure.add_default_env('ROOTSYS',self.spec['root'].prefix)
        configure(*args)
        make.add_default_env('GENIE',self.stage.source_path)
        make.add_default_env('LD_LIBRARY_PATH', '{0}/lib'.format(self.stage.source_path))
        make('GOPT_WITH_CXX_USERDEF_FLAGS={0}'.format(os.environ['CXXFLAGS']))
        make('install')
