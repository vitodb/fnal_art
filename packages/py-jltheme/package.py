# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class PyJltheme(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/CGCFAD/jltheme"
    pypi     = "jltheme/jltheme-0.1.2.tar.gz"

    version('0.1.2', sha256='75361cbd59c835d7d71b8c9c23dd9ddf4644bf67d7e2a42afa260de7c39aa028')

    depends_on('jupyter', type=('run'))

    def build_args(self, spec, prefix):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
