# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class Larbatch(Package):
    """package for batch job submission featuring project.py """

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larbatch-web-client/wiki"
    url      = "http://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/larbatch.v01_51_12.tar"

    version('1.51.12')
    version('1.51.11')
    version('1.51.10')

    depends_on('sam_web_client', type=('run'))
    depends_on('python',         type=('run'))

    def install(self, spec, prefix):
        install_tree(self.stage.source_path, prefix.bin)
