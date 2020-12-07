# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install srproxy
#
# You can edit this file again by typing:
#
#     spack edit srproxy
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *

class PySrproxy(Package):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://github.com/CAFAnaFramework/SRProxy/"
    url      = "https://github.com/CAFAnaFramework/SRProxy/archive/v00.16.tar.gz"

    version('00.16', sha256='98507bf7adfe7b7ddfbfb043ef40c5c3eed55b3818be0c62766b759f06fc0b59')
    version('00.15', sha256='90bed72a1a2924132171d108799698602a28a4143ca2234d0ee988d80bd60d83')
    version('00.14', sha256='fc8c12331e2dcaaa0d5063dd86ae8b65f1221d1505ddb14a4490e6f23019d510')

    # FIXME: Add dependencies if required.
    depends_on('castxml')
    depends_on('pygccxml')

    def install(self, spec, prefix):
        # FIXME: Unknown build system
        os.system("perl -pi.bak -e 's;^dest=.*;dest=%s;' make_ups_product.sh" % self.prefix)
        os.system("sh make_ups_product.sh")
