# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from llnl.util import tty
import sys
import os
import spack.util.spack_json as sjson

def sanitize_environments(*args):
    for env in args:
        for var in ('PATH', 'CET_PLUGIN_PATH',
                    'LD_LIBRARY_PATH', 'DYLD_LIBRARY_PATH', 'LIBRARY_PATH',
                    'CMAKE_PREFIX_PATH', 'ROOT_INCLUDE_PATH'):
            env.prune_duplicate_paths(var)
            env.deprioritize_system_paths(var)

class Larsoftobj(CMakePackage):
    """Larsoftobj"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larsoftobj"
    git_base = 'https://github.com/LArSoft/larsoftobj.git'
    url      = "https://github.com/LArSoft/larsoftobj/archive/v01_02_03.tar.gz"
    list_url = "https://api.github.com/repos/LArSoft/larsoftobj/tags"

    version('09.30.00.rc', branch='v09_30_00_rc_br', git='https://github.com/gartung/larsoftobj.git', get_full_repo=True)
    version('mwm1', tag='mwm1', git='https://github.com/marcmengel/larsoftobj.git', get_full_repo=True)
    version('MVP1a', git=git_base, branch='feature/MVP1a', get_full_repo=True)


    def url_for_version(self, version):
        url = 'https://github.com/LArSoft/{0}/archive/v{1}.tar.gz'
        return url.format(self.name, version.underscored)

    def fetch_remote_versions(self, concurrency=None):
        return dict(map(lambda v: (v.dotted, self.url_for_version(v)),
                        [ Version(d['name'][1:]) for d in
                          sjson.load(
                              spack.util.web.read_from_url(
                                  self.list_url,
                                  accept_content_type='application/json')[2])
                          if d['name'].startswith('v') ]))

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    depends_on('gallery')
    depends_on('lardataobj')
    depends_on('lardataalg')
    depends_on('cetmodules', type='build')

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value)
               ]
        return args

    @run_before('install')
    def install_something(self):
        ''' this pacakge doesn't really contain anything, but
            Spack doesn't like empty products, so put in a README...'''
        f = open(self.prefix + "/README.larsoftobj", "w")
        f.write("larsoftobj is just a bunde with dependencies")
        f.close()

    def setup_dependent_build_environment(self, spack_env, dspec):
        # Ensure we can find plugin libraries.
        spack_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        spack_env.prepend_path('PATH', self.prefix.bin)
        spack_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        spack_env.append_path('FHICL_FILE_PATH','{0}/job'.format(self.prefix))
        spack_env.append_path('FW_SEARCH_PATH','{0}/gdml'.format(self.prefix))
        sanitize_environments(spack_env)

    def setup_dependent_run_environment(self, run_env, dspec):
        # Ensure we can find plugin libraries.
        run_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        run_env.prepend_path('PATH', self.prefix.bin)
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        run_env.append_path('FHICL_FILE_PATH','{0}/job'.format(self.prefix))
        run_env.append_path('FW_SEARCH_PATH','{0}/gdml'.format(self.prefix))
        sanitize_environments(run_env)
