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


class CetlibExcept(CMakePackage):
    """Exception libraries for the art suite."""

    homepage = "https://art.fnal.gov/"
    git = "https://github.com/art-framework-suite/cetlib-except.git"
    url = "https://github.com/art-framework-suite/cetlib-except/archive/refs/tags/v1_07_04.tar.gz"

    version("1.08.00", sha256="2951be7cd7b58c05c09a89fdd8b2b287262447d7e69e13bef7a15a98040d4efd")
    version("1.07.06", sha256="49324dcd254dcd1183715d4bb6ea5ccf394231e717ebb4c08cf0ab0c1d976bdf")
    version("1.07.04", sha256="d021d26fda9f4f57b57850bc6f5ac0a79aed913ef1cde68a96838ad85d332d70")
    version("develop", branch="develop", get_full_repo=True)

    variant(
        "cxxstd",
        default="17",
        values=("17", "20", "23"),
        multi=False,
        sticky=True,
        description="C++ standard",
    )

    depends_on("cmake@3.21:", type="build")
    depends_on("cetmodules@3.19.02:", type="build")
    depends_on("cetpkgsupport", type=("build", "run"))
    depends_on("catch2@:2.99", type="build")


    if "SPACK_CMAKE_GENERATOR" in os.environ:
        generator = os.environ["SPACK_CMAKE_GENERATOR"]
        if generator.endswith("Ninja"):
            depends_on("ninja@1.10:", type="build")

    def url_for_version(self, version):
        url = "https://github.com/art-framework-suite/cetlib-except/archive/refs/tags/v{0}.tar.gz"
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
        # For tests.
        env.prepend_path("PATH", os.path.join(self.build_directory, "bin"))
        # Cleanup.
        sanitize_environments(env, "PATH")
