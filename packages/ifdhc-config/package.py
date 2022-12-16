# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import llnl.util.tty as tty

from spack import *


class IfdhcConfig(Package):
    """Config package for Data handling client code for intensity frontier experiments"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/ifdhc"
    git_base = "https://cdcvs.fnal.gov/projects/ifdhc/ifdhc.git"
    url = "https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/ifdhc.v2_5_4.tbz2"


    version("2.6.11", sha256="988eb6bd2124174e0956b4415edcc3671ac87896a64852e9e99d8628c4fa1334")
    version("2.6.10", sha256="44ee19429ec3c55be54582fb9411b68ebba9c90ae3ee8b770faa702f599a3f49")
    version("2.6.9", sha256="46dadbba0acdf19644496fd7c3eff2a046f745e9fe9fe68f42b7c499df293596")
    version("2.6.8", sha256="9a60403d06463f34c988d45a3049b1e09409c4a44ac08f45da920dc2eab26ff5")
    version("2.6.7", sha256="365949d19faf14200b4fa0f80dd881fbd4bbcf7f4699bab5e43358119d4109b8")
    version("2.6.6", sha256="fc04576e5ae82740f6a1797ebeeac6855338eb028a43b178f3f66183f4bb583e")
    version("2.5.16", sha256="5455f58042c7b84826fc72e77d21e9f0a5ec7efe5f40435571c52fb4c0e226fd")
    version("2.3.10", sha256="4da290f5fc3c9d4344792176e19e1d3278f87a634ebc1535bbd9a91aae2bbf9b")
    version("2.3.9", sha256="1acdff224f32c3eb5780aed13cf0f23b431623a0ebc8a74210271b75b9f2f574")
    version("2.5.4", sha256="48bf6807cb8b3092677768f763c1f18940d852d685424a1ea386acf7f1606608")
    version("2.5.12", sha256="e8a8af62e5e9917e51c88b2cda889c2a195dfb7911e09c28aeaf10f54e8abf49")
    version("2.5.14", sha256="66ab9126bb3cb1f8d8dafb69568569d8856ab6770322efc7c5064252f27a8fda")
    version("2.5.2", git=git_base, tag="v2_5_2", get_full_repo=True)
    version("develop", git=git_base, branch="develop", get_full_repo=True)

    parallel = False

    def url_for_version(self, version):
        print("in url_for_version...")
        url = "https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/ifdhc.v{0}.tbz2"
        return url.format(version.underscored)

    def install(self, a, b):
        cplist=[
                ['ifdh.cfg', 'ifdh.cfg'], 
                ['ifdh/www_cp.sh', 'bin/www_cp.sh'],
                ['ifdh/auth_session.sh', 'bin/auth_session.sh'], 
                ['ifdh/decode_token.sh', 'bin/decode_token.sh'],
               ]
        for fnpair in cplist:
            cmd = "cp {0}/{2} {1}/{3}".format(
                 self.stage.source_path, self.spec.prefix, fnpair[0],fnpair[1]
            )
            tty.warn("installing {0}: {1} ".format(fnpair[0], cmd))
            os.system(cmd)

    def setup_build_environment(self, spack_env):
        spack_env.set("IFDHC_CONFIG_DIR", self.spec.prefix)

    def setup_run_environment(self, run_env):
        run_env.prepend_path("PATH", self.spec.prefix.bin)
        run_env.set("IFDHC_CONFIG_DIR", self.spec.prefix)
