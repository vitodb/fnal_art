# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os 

class GenieXsec(Package):
    """Data files used by genie."""

    homepage = "http://www.example.com"
    url = 'file://' + os.path.dirname(__file__) + '/../../config/junk.xml'
    version('1.0', '2cae8b754a9f824ddd27964d11732941fd88f52f0880d7f685017caba7fea6b7', expand=False)

    urlbase='http://scisoft.fnal.gov/scisoft/packages/genie_xsec/v2_12_10/genie_xsec-2.12.10-noarch-'
    resource(name='AltPion', placement='.',
             url=urlbase+'AltPion.tar.bz2',
             sha256='49c4c5332c96edc4147e8cacd5b68e8dd89737e205741a21bc75a5ba18b967c4')
    resource(name='DefaultPlusMECWithNC', placement='.',
             url=urlbase+'DefaultPlusMECWithNC.tar.bz2',
             sha256='7c57caa96c319ad8007253e2a81c6ffcc4dcc6d0923dabbf7b8938d8363ac621')
    resource(name='DefaultPlusValenciaMEC', placement='.',
             url=urlbase+'DefaultPlusValenciaMEC.tar.bz2',
             sha256='fe1b584e7014bba6c4cba5646e1031f344e9efbf799a2aa26b706e28c40a4481')
    resource(name='EffSFTEM', placement='.',
             url=urlbase+'EffSFTEM.tar.bz2',
             sha256='b6365f1a150b90b79788f51b084a1dce7432d8ba10b7faa03ade3f6d558c82f6')
    resource(name='LocalFGNievesQEAndMEC', placement='.',
             url=urlbase+'LocalFGNievesQEAndMEC.tar.bz2',
             sha256='5f02d7efa46ef42052834d80b6923b41e502994daaf6037dad9793799ad4b346')
    resource(name='ValenciaQEBergerSehgalCOHRES', placement='.',
             url=urlbase+'ValenciaQEBergerSehgalCOHRES.tar.bz2',
             sha256='3e7c117777cb0da6232df1e1fe481fdb2afbfe55639b0d7b4ddf8027954ed1fa')

    def install(self, spec, prefix):
        install_tree(self.stage.source_path,prefix)

