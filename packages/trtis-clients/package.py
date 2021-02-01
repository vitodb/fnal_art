# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os

class TrtisClients(CMakePackage):
    """C++ client code for Triton Inference Server."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/triton-inference-server/server"
    url      = "https://github.com/triton-inference-server/server/archive/v2.6.0.tar.gz"

    # maintainers = ['github_user1', 'github_user2']

    version('2.6.0',                    sha256='c4fad25c212a0b5522c7d65c78b2f25ab0916ccf584ec0295643fec863cb403e')

    depends_on('cmake@3.18:', type='build')
    depends_on('py-grpcio', type='build')
    depends_on('rapidjson')
    depends_on('opencv')
    depends_on('protobuf')
    depends_on('grpc')
    depends_on('googletest')
    depends_on('c-ares')
    depends_on('libevent')
    
    patch('fix_compile_flags.patch')
    patch('use_existing.patch')

    root_cmakelists_dir = 'build'
  
    def setup_environment(self, spack_env, run_env):
        spack_env.append_path('CMAKE_PREFIX_PATH', self.build_directory)

    def cmake_args(self):
        args = [
            '-DCMAKE_BUILD_TYPE=Release',
            '-DCMAKE_C_COMPILER=cc',
            '-DCMAKE_CXX_COMPILER=c++',
            '-DCMAKE_CXX_FLAGS=-Wno-deprecated-declarations',
            '-DCMAKE_PREFIX_PATH=%s/share/OpenCV' % self.spec['opencv'].prefix,
            '-DTRITON_ENABLE_GPU:BOOL=OFF',
            '-DTRITON_ENABLE_METRICS_GPU:BOOL=OFF',
        ]
        return args

    def install(self, spec, prefix):
        install_tree(self.stage.source_path+'/install/include', prefix+'/include/trts_clients')
        install_tree(self.stage.source_path+'/install/lib', prefix+'/lib')

