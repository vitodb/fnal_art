# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class H5cpp(Package):
    """Hierarchical Data Format C++ templates for Serial and Paralell HDF5"""

    homepage = "https://h5cpp.org/"
    url      = "http://h5cpp.org/download/h5cpp-full_1.10.4.1.tar.gz"

    version('1.10.4.1')

    def install(self, spec, prefix):
        install_tree(self.stage.source_path + "/usr/include", prefix+"/include")

