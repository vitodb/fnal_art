# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


def sanitize_environments(env, *vars):
    for var in vars:
        env.prune_duplicate_paths(var)
        env.deprioritize_system_paths(var)


class Canvas(CMakePackage):
    """The underpinnings for the art suite."""

    homepage = "https://art.fnal.gov/"
    git = "https://github.com/art-framework-suite/canvas.git"
    url = "https://github.com/art-framework-suite/canvas/archive/refs/tags/v3_09_01.tar.gz"


    version("3.14.00", sha256="f3dd81aa1770c62e3329409a3849db13c7b7818d4927a52ceb82f5e7f3f0ebf4")
    version("3.13.01", sha256="ad84161ad37b30675664994ba37a8f4ee5001d5936ebabc24b79b9a3c9419515")
    version("3.13.00", sha256="6d5d6d817907fada8504514d5c9009f6b48a7afd606fa4bed3793d30aad347b7")
    version("3.12.05", sha256="e0a0506528ab1f4db4b76bd3b68f0ea1ea97a627a68930abbfa1b2bfea069ee9")
    version("3.12.04", sha256="bcbb9680000a0f1eec4ec3983b49d8a89f6820d4abdee2ffcb7bd769a0799974")

    version("develop", branch="develop", get_full_repo=True)

    variant(
        "cxxstd",
        default="17",
        values=("17", "20", "23"),
        multi=False,
        sticky=True,
        description="C++ standard",
    )

    depends_on("boost+date_time+test")
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("cetmodules", type="build")
    depends_on("clhep")
    depends_on("cmake@3.21:", type="build")
    depends_on("fhicl-cpp")
    depends_on("hep-concurrency", type="test")
    depends_on("messagefacility")
    depends_on("range-v3@0.12:")

    if "SPACK_CMAKE_GENERATOR" in os.environ:
        generator = os.environ["SPACK_CMAKE_GENERATOR"]
        if generator.endswith("Ninja"):
            depends_on("ninja@1.10:", type="build")

    def url_for_version(self, version):
        url = "https://github.com/art-framework-suite/canvas/archive/refs/tags/v{0}.tar.gz"
        return url.format(version.underscored)

    def cmake_args(self):
        return [
           "--preset", "default", 
           "-DCMAKE_CXX_COMPILER={0}".format(self.compiler.cxx_names[0]),
           "-DCMAKE_C_COMPILER={0}".format(self.compiler.cc_names[0]),
           "-DCMAKE_Fortran_COMPILER={0}".format(self.compiler.f77_names[0]),
           self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
        ]

    def setup_build_environment(self, env):
        prefix = self.build_directory
        # Binaries.
        env.prepend_path("PATH", os.path.join(prefix, "bin"))
        # Cleanup.
        sanitize_environments(env, "PATH")
