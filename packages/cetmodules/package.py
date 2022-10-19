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
    url = "https://github.com/FNALssi/cetmodules/archive/refs/tags/3.19.02.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]

    version("develop", branch="develop", get_full_repo=True)
    version("3.19.02", sha256="214172a59f4c3875a5d7c2617b9f50ed471c86404d85e2e5c72cadf5b499cdc6")

    variant(
        "versioned-docs", default=False, description="build versioned docs with a landing page"
    )
    variant("docs", default=False, when="~versioned-docs", description="build documentation")

    depends_on("cmake@3.21:", type="build")

    docs_deps = (
        "git@2.22:",
        "py-sphinxcontrib-moderncmakedomain",
        "py-sphinx-rtd-theme",
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

    for pkg, types in perl_deps.items():
        depends_on(pkg, type=types)

    conflicts("@:3.19.01", when="^cmake@3.24.0:")

    if "SPACK_CMAKE_GENERATOR" in os.environ:
        generator = os.environ["SPACK_CMAKE_GENERATOR"]
        if generator.endswith("Ninja"):
            depends_on("ninja@1.10:", type="build")

    @run_before("cmake")
    def fix_fix_man(self):
        filter_file(r"exit \$status", "exit 0", "%s/libexec/fix-man-dirs" % self.stage.source_path)

    def cmake_args(self):
        options = ["--preset", "default"]
        if not any(
            [
                self.spec.variants[doc_opt].value
                for doc_opt in ("docs", "versioned-docs")
                if doc_opt in self.spec.variants
            ]
        ):
            options.append(self.define("BUILD_DOCS", False))
        elif self.spec.variants["versioned-docs"].value:
            options += [
                self.define(
                    "{0}_SPHINX_DOC_PUBLISH_VERSION_BRANCH".format(self.name), self.spec.version
                ),
                self.define(
                    "{0}_SPHINX_DOC_PUBLISH_ROOT".format(self.name),
                    join_path(self.stage.path, "doc_root"),
                ),
            ]
        return options
