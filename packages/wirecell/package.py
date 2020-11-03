# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import os
import sys
libdir="%s/var/spack/repos/fnal_art/lib" % os.environ["SPACK_ROOT"]
if not libdir in sys.path:
    sys.path.append(libdir)
from cetmodules_patcher import cetmodules_20_migrator

def patcher(x):
    cetmodules_20_migrator(".","wirecell","0.13.1")

def sanitize_environments(*args):
    for env in args:
        for var in ('PATH', 'CET_PLUGIN_PATH',
                    'LD_LIBRARY_PATH', 'DYLD_LIBRARY_PATH', 'LIBRARY_PATH',
                    'CMAKE_INSTALL_RPATH', 'CMAKE_PREFIX_PATH', 'ROOT_INCLUDE_PATH'):
            env.prune_duplicate_paths(var)
            env.deprioritize_system_paths(var)


class Wirecell(Package):
    """Wire Cell Toolkit provides simulation, signal processing and reconstruction for LArTPC
    Borrowed from 
    https://github.com/WireCell/wire-cell-spack/blob/master/repo/packages/wirecell-toolkit/package.py"""

    homepage = "https://wirecell.github.io"
    url = "https://github.com/WireCell/wire-cell-toolkit/archive/0.13.1.tar.gz"

    version('0.13.1', sha256='d9ce092f9ebae91607213b62bf015ac6ac08c33ce97b6fbd67494d42c1f75bdb')
    version('0.13.0', sha256='eedc7db7ce75d2f7ef1b23461d1a2d780fd8409187eb851ced1e8ab4b7a10d8e')
    version('0.12.2', sha256='83387ebe6a517353daae69b05e86dd274f66ba80e6b120fb219b5c260c383e21')
    version('0.11.2', sha256='56b46cad781948e21c36660032de3ca54d5d5fd6b7aa47cdc3d3d4a67770f831')
    version('0.10.9', sha256='a5a7f2d45c78c18e098f3afc10e6df06b0e94e062870535c927c0fab51e43bd8')

    variant('cxxstd',
            default='17',
            values=('11', '14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    depends_on("jsoncpp")
    depends_on("jsonnet")

    depends_on("fftw")
    depends_on("eigen+fftw")


    # Do not currently make use of TBB.  When we get back to this,
    # probably best to build ROOT with TBB support as well.
    # depends_on("tbb")
    depends_on("root@6:")

    # match what is listed in wire-cell-build/wscript
    depends_on("boost")


    def install(self, spec, prefix):

        cfg = "wcb"
        cfg += " --prefix=%s" % prefix
        cfg += " --boost-mt"
        cfg += " --boost-libs=%s --boost-includes=%s" % \
               (spec["boost"].prefix.lib, spec["boost"].prefix.include)
        cfg += " --with-root=%s" % spec["root"].prefix
        cfg += " --with-eigen=%s" % spec["eigen"].prefix
        cfg += " --with-eigen-include=%s" % spec["eigen"].prefix.include.eigen3
        cfg += " --with-jsoncpp=%s" % spec["jsoncpp"].prefix
        cfg += " --with-jsonnet=%s" % spec["jsonnet"].prefix
#        cfg += " --with-tbb=%s" % spec["tbb"].prefix
        cfg += " --with-tbb=false" # for now
        cfg += " --with-fftw=%s" % spec["fftw"].prefix
        cfg += " --build-debug=-std=c++17"

        cfg += " configure"
        python(*cfg.split())
        python("wcb","-vv")
        python("wcb", "install")
        return

    def setup_environment(self, spack_env, run_env):
        cxxstd = self.spec.variants['cxxstd'].value
        cxxstdflag = '' if cxxstd == 'default' else \
                     getattr(self.compiler, 'cxx{0}_flag'.format(cxxstd))
        spack_env.append_flags('CXXFLAGS', cxxstdflag)
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(root=False, cover='nodes', order='post',
                                    deptype=('link'), direction='children'):
            spack_env.prepend_path('ROOT_INCLUDE_PATH',
                                   str(self.spec[d.name].prefix.include))
            run_env.prepend_path('ROOT_INCLUDE_PATH',
                                 str(self.spec[d.name].prefix.include))
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        # Cleanup.
        sanitize_environments(spack_env, run_env)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        # Cleanup.
        sanitize_environments(spack_env, run_env)
