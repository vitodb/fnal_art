# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class Ifdhc(MakefilePackage):
    """Data handling client code for intensity frontier experiments"""

    homepage = "http://cdcvs.fnal.gov/redmine/projects/ifdhc"
    git_base = "http://cdcvs.fnal.gov/projects/ifdhc/ifdhc.git"

    version('develop', git=git_base, branch='develop')
    version('2.3.10',
            sha256='4da290f5fc3c9d4344792176e19e1d3278f87a634ebc1535bbd9a91aae2bbf9b',
            extension='tbz2')
    version('2.3.9',
            sha256='1acdff224f32c3eb5780aed13cf0f23b431623a0ebc8a74210271b75b9f2f574',
            extension='tbz2')

    depends_on('python')
    depends_on('swig', type='build')
    depends_on('zlib')
    depends_on('libuuid')

    variant('cxxstd',
            default='17',
            values=('default', '98', '11', '14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    patch('version.patch', level=1, when='@:2.4.5')

    parallel = False

    def url_for_version(self, version):
        url = 'http://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/{0}.v{1}.tbz2'
        return url.format(self.name, version.underscored)

    @property
    def build_targets(self):
        cxxstd = self.spec.variants['cxxstd'].value
        cxxstdflag =  '' if cxxstd == 'default' else \
                      getattr(self.compiler, 'cxx{0}_flag'.format(cxxstd))
        return ('ARCH=' + '-g -O3 -DNDEBUG ' + cxxstdflag,)

    @property
    def install_targets(self):
        return ('DESTDIR={0}/'.format(self.prefix), 'install')

    def setup_environment(self, spack_env, run_env):
        spack_env.set('PYTHON_INCLUDE', self.spec['python'].prefix.include)
        spack_env.set('PYTHON_LIB', self.spec['python'].prefix.lib)
        run_env.prepend_path('PATH', self.prefix.bin)

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.prepend_path('PATH', self.prefix.bin)
        run_env.prepend_path('PATH', self.prefix.bin)
        # Non-standard, therefore we have to do it ourselves.
        spack_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.inc)
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.inc)
