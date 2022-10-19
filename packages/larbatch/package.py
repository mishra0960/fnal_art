# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Larbatch(Package):
    """package for batch job submission featuring project.py"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larbatch-web-client/wiki"
    url = "https://github.com/LArSoft/larbatch/archive/refs/tags/v01_51_15.tar.gz"

    version("01_51_15", sha256="f99dc422785286841260a168ec0681b0a3898fb5fad535cb3638837a6b6a988f")

    depends_on("sam-web-client", type=("run"))
    depends_on("python", type=("run"))

    def install(self, spec, prefix):
        install_tree(self.stage.source_path, prefix)

    def setup_run_environment(self, run_env):
        run_env.prepend_path("PYTHONPATH", self.prefix.bin)
        run_env.prepend_path("PYTHONPATH", self.prefix + "/python")
