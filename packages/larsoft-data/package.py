# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class LarsoftData(Package):
    """LarsoftData"""

    homepage = "http://www.example.com"
    version('1.02.01', '9b3e5d763f4a44f0fae7a2b59d583a8b25054f7f06645fa48e331377cf33baca', extension='bzip2')

    def url_for_version(self, version):
        url = 'http://scisoft.fnal.gov/scisoft/packages/larsoft_data/v{0}/larsoft_data-{1}-noarch.tar.bz2'
        return url.format(version.underscored, version)

    def install(self, spec, prefix):
        install_tree('{0}/v{1}'.format(self.stage.source_path,self.version.underscored),
                     '{0}'.format(prefix.share))


