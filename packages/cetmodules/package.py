# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Cetmodules(CMakePackage):
    """CMake glue modules and scripts required by packages originating at
    Fermilab and associated experiments and other collaborations.
    """

    homepage = "https://fnalssi.github.io/cetmodules/"
    git = "https://github.com/FNALssi/cetmodules.git"
    url = "https://github.com/FNALssi/cetmodules/archive/refs/tags/3.21.01.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]

    version("develop", branch="develop", get_full_repo=True)
    version("3.19.02", sha256="214172a59f4c3875a5d7c2617b9f50ed471c86404d85e2e5c72cadf5b499cdc6")
    version("3.21.00", sha256="429ddecf2e905a6a3156c267005d17cd6e160533f28bcef0be40a9d0057e95e4")
    version("3.21.01", sha256="9f4b845f9ed09fb3a8ee7864ac487afd08a5b3e64abf394831ee927f91b08ebc")
    version("3.21.02", sha256="255d6d6c2455217734b208fc90919b90bc7c0f9a59a4706d329c642bff51f004")
    version("3.22.01", sha256="c72c47328adc0c95f905aae119c76d35513a0677f20163f0ef25a82bd0f72082")

    variant(
        "versioned-docs", default=False, description="build versioned docs with a landing page"
    )
    variant("docs", default=False, when="~versioned-docs", description="build documentation")

    depends_on("cmake@3.21:", type="build")

    docs_deps = (
        "git@2.22:",
        "py-sphinxcontrib-moderncmakedomain",
        "py-sphinx-design@0.2.0:",
        "py-sphinx@5:5.999",
    )
    for dep in docs_deps:
        depends_on(dep, type="build", when="+docs")
        depends_on(dep, type="build", when="+versioned-docs")

    perl_deps = {
        "perl-data-dumper": ("build", "run"),
        "perl-json": ("build", "run"),
        "perl-list-moreutils": ("build", "run"),
        "perl-metacpan-client": ("build", "run"),
        "perl-path-tiny": ("build", "run"),
        "perl-readonly": ("build", "test", "run"),
        "perl-perl-tidy": ("build", "test", "run"),
        "perl-task-perl-critic": ("build", "test"),
    }

#    for pkg, types in perl_deps.items():
#        depends_on(pkg, type=types)

    conflicts("@:3.19.01", when="^cmake@3.24.0:")

    if "SPACK_CMAKE_GENERATOR" in os.environ:
        generator = os.environ["SPACK_CMAKE_GENERATOR"]
        if generator.endswith("Ninja"):
            depends_on("ninja@1.10:", type="build")

    @run_before("cmake")
    def fix_fix_man(self):
        filter_file(r"exit \$status", "exit 0", "%s/libexec/fix-man-dirs" % self.stage.source_path)

    def cmake_args(self):
        spec = self.spec
        define = self.define
        options = ["--preset", "default"]
        if not any(
            [
                spec.variants[doc_opt].value
                for doc_opt in ("docs", "versioned-docs")
                if doc_opt in spec.variants
            ]
        ):
            options.append(define("BUILD_DOCS", False))
        elif spec.variants["versioned-docs"].value:
            options += [
                define(
                    f"{self.name}_SPHINX_DOC_PUBLISH_VERSION_BRANCH", spec.version
                ),
                define(
                    f"{self.name}_SPHINX_DOC_PUBLISH_ROOT",
                    join_path(self.stage.path, "doc_root"),
                ),
            ]
        return options
