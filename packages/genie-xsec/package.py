# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class GenieXsec(Package):
    """Data files used by genie."""

    homepage = "https://www.example.com"
    url = "file://" + os.path.dirname(__file__) + "/../../config/junk.xml"
    version(
        "2.12.10", "2cae8b754a9f824ddd27964d11732941fd88f52f0880d7f685017caba7fea6b7", expand=False
    )

    variant(
        "xsec_name",
        default="DefaultPlusMECWithNC",
        multi=False,
        values=(
            "AltPion",
            "DefaultPlusMECWithNC",
            "DefaultPlusValenciaMEC",
            "EffSFTEM",
            "LocalFGNievesQEAndMEC",
            "ValenciaQEBergerSehgalCOHRES",
        ),
        description="Name of genie xsec set to install.",
    )

    urlbase = (
        "https://scisoft.fnal.gov/scisoft/packages/genie_xsec/v2_12_10/genie_xsec-2.12.10-noarch-"
    )
    resource(
        name="AltPion",
        placement="AltPion",
        when="xsec_name=AltPion",
        url=urlbase + "AltPion.tar.bz2",
        sha256="49c4c5332c96edc4147e8cacd5b68e8dd89737e205741a21bc75a5ba18b967c4",
    )
    resource(
        name="DefaultPlusMECWithNC",
        placement="DefaultPlusMECWithNC",
        when="xsec_name=DefaultPlusMECWithNC",
        url=urlbase + "DefaultPlusMECWithNC.tar.bz2",
        sha256="7c57caa96c319ad8007253e2a81c6ffcc4dcc6d0923dabbf7b8938d8363ac621",
    )
    resource(
        name="DefaultPlusValenciaMEC",
        placement="DefaultPlusValenciaMEC",
        when="xsec_name=DefaultPlusValenciaMEC",
        url=urlbase + "DefaultPlusValenciaMEC.tar.bz2",
        sha256="fe1b584e7014bba6c4cba5646e1031f344e9efbf799a2aa26b706e28c40a4481",
    )
    resource(
        name="EffSFTEM",
        placement="EffSFTEM",
        when="xsec_name=EffSFTEM",
        url=urlbase + "EffSFTEM.tar.bz2",
        sha256="b6365f1a150b90b79788f51b084a1dce7432d8ba10b7faa03ade3f6d558c82f6",
    )
    resource(
        name="LocalFGNievesQEAndMEC",
        placement="LocalFGNievesQEAndMEC",
        when="xsec_name=LocalFGNievesQEAndMEC",
        url=urlbase + "LocalFGNievesQEAndMEC.tar.bz2",
        sha256="5f02d7efa46ef42052834d80b6923b41e502994daaf6037dad9793799ad4b346",
    )
    resource(
        name="ValenciaQEBergerSehgalCOHRES",
        placement="ValenciaQEBergerSehgalCOHRES",
        when="xsec_name=ValenciaQEBergerSehgalCOHRES",
        url=urlbase + "ValenciaQEBergerSehgalCOHRES.tar.bz2",
        sha256="3e7c117777cb0da6232df1e1fe481fdb2afbfe55639b0d7b4ddf8027954ed1fa",
    )

    def install(self, spec, prefix):
        val = spec.variants["xsec_name"].value
        install_tree(
            "{0}/{2}/v{1}/NULL/{2}".format(self.stage.source_path, self.version.underscored, val),
            "{0}/{1}".format(prefix, val),
        )
