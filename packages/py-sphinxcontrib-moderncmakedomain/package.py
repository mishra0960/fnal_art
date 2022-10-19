# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySphinxcontribModerncmakedomain(PythonPackage):
    """This sphinx extension helps you document Python code that uses
    async/await, or abstract methods, or context managers, or generators,
    or ... you get the idea."""

    homepage = "https://github.com/python-moderncmakedomain/sphinxcontrib-moderncmakedomain"
    # url = "https://pypi.io/packages/source/s/sphinxcontrib-moderncmakedomain/sphinxcontrib-moderncmakedomain-3.19.tar.gz"
    url = "https://files.pythonhosted.org/packages/9a/10/cfdd388a0894d17ae270178e348ee3063e3f3700b78ff9c1389621d0fe2a/sphinxcontrib-moderncmakedomain-3.19.tar.gz"
    version("3.19", sha256="b2900cc170b94ad53c59ae50a01961dc4c3ae9c12a8ec582d017b17abd69cea1")

    depends_on("py-sphinx@1.7:")

    def install_args(self, spec, prefix):
        return [
            "--prefix=%s" % prefix,
            "--root=/",
            "--single-version-externally-managed",
        ]

    # patch('sphinxcontrib-moderncmakedomain.patch', when='@1.1.0')
