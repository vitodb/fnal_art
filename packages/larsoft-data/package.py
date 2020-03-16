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
from cetmodules_patcher import cetmodules_dir_patcher

def patcher(x):
    cetmodules_dir_patcher(".","larsoft-data","1.02.01")

class LarsoftData(Package):
    """LarsoftData"""

    patch = patcher

    version('1.02.01', '9b3e5d763f4a44f0fae7a2b59d583a8b25054f7f06645fa48e331377cf33baca')

    def url_for_version(self, version):
        url = 'http://scisoft.fnal.gov/scisoft/packages/larsoft_data/v{0}/larsoft_data-{1}-noarch.tar.bz2'
        return url.format(version.underscored, version)

    def install(self, spec, prefix):
        install_tree('{0}/v{1}'.format(self.stage.source_path,self.version.underscored),
                     '{0}'.format(prefix))

    def _add_paths_to_environment(self, env):
        for path_fragment in ('uboone', 'Argoneut', 'Genfit',
                              'ParticleIdentification',
                              os.path.join('pdf', 'Gaisser'),
                              os.path.join('pdf', 'MUSUN'),
                              'SupernovaNeutrinos', ''):
            path = os.path.join(self.prefix, path_fragment)
            env.prepend_path('FW_SEARCH_PATH', path)

    def setup_environment(self, spack_env, run_env):
        self._add_paths_to_environment(run_env)

    def setup_dependent_environment(self, spack_env, run_env, dep_spec):
        self._add_paths_to_environment(spack_env)
        self._add_paths_to_environment(run_env)
