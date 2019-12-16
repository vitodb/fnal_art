# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Nucondb(MakefilePackage):
    """Data handling client code for intensity frontier experiments"""

    homepage = "http://cdcvs.fnal.gov/redmine/projects/nucondb"

    version('2.3.0',
            sha256='e2e30acc10cabd4e6fc0784c41dfcf2b372dfbf003a42bd80210ebb8c81d057f')
    version('2.2.10',
            sha256='d90d471ee1db823260035986284623eea0e84944039e69d9fd95bf8749d2a736')

    parallel = False

    build_directory = 'src'

    variant('cxxstd',
            default='17',
            values=('default', '98', '11', '14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    depends_on('ifdhc')
    depends_on('libwda')
 
    def url_for_version(self, version):
        url = 'http://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/{0}.v{1}.tbz2'
        return url.format('ifdhc-' + self.name, version.underscored)

    @property
    def build_targets(self):
        cxxstd = self.spec.variants['cxxstd'].value
        cxxstdflag =  '' if cxxstd == 'default' else \
                      getattr(self.compiler, 'cxx{0}_flag'.format(cxxstd))        
        return ('LIBWDA_FQ_DIR=' + self.spec['libwda'].prefix,
                'LIBWDA_LIB=' + self.spec['libwda'].prefix.lib,
                'IFDHC_FQ_DIR=' + self.spec['ifdhc'].prefix,
                'IFDHC_LIB=' + self.spec['ifdhc'].prefix.lib,
                'ARCH=' + cxxstdflag)

    @property
    def install_targets(self):
        return ('DESTDIR={0}/'.format(self.prefix), 'install')
