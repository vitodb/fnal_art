##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *
import os
try:
    from pipes import quote as cmd_quote
except ImportError:
    from shlex import quote as cmd_quote


def sanitize_environments(*args):
    for env in args:
        for var in ('PATH', 'CET_PLUGIN_PATH',
                    'LD_LIBRARY_PATH', 'DYLD_LIBRARY_PATH', 'LIBRARY_PATH',
                    'CMAKE_PREFIX_PATH', 'ROOT_INCLUDE_PATH'):
            env.prune_duplicate_paths(var)
            env.deprioritize_system_paths(var)


class Messagefacility(CMakePackage):
    homepage = 'https://cdcvs.fnal.gov/projects/messagefacility'

    version('develop', branch='feature/for_spack',
            git=homepage, preferred=True)

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    # Build-only dependencies.
    depends_on('cmake@3.4:', type='build')
    depends_on('cetmodules', type='build')
    depends_on('catch@2:~single_header', type='build')

    # Build / link dependencies.
    depends_on('hep_concurrency')
    depends_on('cetlib_except')
    depends_on('cetlib')
    depends_on('fhicl-cpp')
    depends_on('boost')
    depends_on('sqlite')
    depends_on('perl')
    depends_on('tbb')

    if 'SPACKDEV_GENERATOR' in os.environ:
        generator = os.environ['SPACKDEV_GENERATOR']
        if generator.endswith('Ninja'):
            depends_on('ninja', type='build')

    def url_for_version(self, version):
        url = 'https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/{0}.v{1}.tbz2'
        return url.format(self.name, version.underscored)

    def cmake_args(self):
        # Set CMake args.
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value)]
        return args

    def setup_environment(self, spack_env, run_env):
        # Binaries.
        spack_env.prepend_path('PATH',
                               join_path(self.build_directory, 'bin'))
        # Ensure we can find plugin libraries.
        spack_env.prepend_path('CET_PLUGIN_PATH',
                               join_path(self.build_directory, 'lib'))
        run_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        # Perl modules.
        spack_env.prepend_path('PERL5LIB',
                               join_path(self.build_directory, 'perllib'))
        run_env.prepend_path('PERL5LIB', join_path(self.prefix, 'perllib'))
        # Cleaup.
        sanitize_environments(spack_env, run_env)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        # Binaries.
        spack_env.prepend_path('PATH',
                               join_path(self.build_directory, 'bin'))
        # Ensure we can find plugin libraries.
        spack_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        run_env.prepend_path('CET_PLUGIN_PATH', self.prefix.lib)
        # Perl modules.
        spack_env.prepend_path('PERL5LIB', join_path(self.prefix, 'perllib'))
        run_env.prepend_path('PERL5LIB', join_path(self.prefix, 'perllib'))
        # Cleanup.
        sanitize_environments(spack_env, run_env)

    def do_fake_install(self):
        cargs = self.std_cmake_args + self.cmake_args()
        print('\n'.join(['[cmake-args {0}]'.format(self.name)] + cargs +
                        ['[/cmake-args]']))
