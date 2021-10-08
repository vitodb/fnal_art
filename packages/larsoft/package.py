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


class Larsoft(CMakePackage):
    """Larsoft"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larsoft"
    git_base = 'https://github.com/LArSoft/larsoft.git'
    url      = "https://github.com/LArSoft/larsoft/archive/v01_02_03.tar.gz"
    list_url = 'https://github.com/LArSoft/larsoft.git'

    version('09.30.00.rc', branch='v09_30_00_rc_br', git='https://github.com/gartung/larsoft.git', get_full_repo=True)
    version('mwm1', tag='mwm1', git='https://github.com/marcmengel/larsoft.git', get_full_repo=True)
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


    depends_on('cetmodules', type='build')
    depends_on('ifdh-art')
    depends_on('larana')
    depends_on('lareventdisplay')
    depends_on('larexamples')
    depends_on('larg4')
    depends_on('larpandora')
    depends_on('larreco')
    depends_on('larrecodnn')
    depends_on('larsimrad')
    depends_on('larsoft-data')
    depends_on('larsoftobj')
    depends_on('larwirecell')

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value)
               ]
        return args


    def setup_dependent_build_environment(self, spack_env, dspec):
        spack_env.set('LARSOFT_INC',self.prefix.include)
        spack_env.set('LARSOFT_LIB', self.prefix.lib)
        spack_env.prepend_path('PATH', self.prefix.bin)
        spack_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        spack_env.prepend_path('PATH', self.prefix.bin)
        spack_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        spack_env.append_path('FHICL_FILE_PATH','{0}/job'.format(self.prefix))
        spack_env.append_path('FW_SEARCH_PATH','{0}/gdml'.format(self.prefix))
        sanitize_environments(spack_env)

    def setup_dependent_run_environment(self, run_env, dspec):
        run_env.prepend_path('PATH', self.prefix.bin)
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        run_env.prepend_path('PATH', self.prefix.bin)
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        run_env.append_path('FHICL_FILE_PATH','{0}/job'.format(self.prefix))
        run_env.append_path('FW_SEARCH_PATH','{0}/gdml'.format(self.prefix))
        sanitize_environments(spack_env)


    @run_after('install')
    def rename_bin_python(self):
        import os
        os.rename( join_path(self.spec.prefix, "bin/python"),
                   join_path(self.spec.prefix, "bin/python-scripts"))

