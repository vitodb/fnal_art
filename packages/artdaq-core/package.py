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



def patcher(x):
    cetmodules_20_migrator(".","artg4tk","9.07.01")



class ArtdaqCore(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
 event building, event reconstruction and analysis (using the art analysis
 framework), process management, system and process state behavior, control
 messaging, local message logging (status and error messages), DAQ process 
 and art module configuration, and the writing of event data to disk in ROOT
 format."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/artdaq/wiki"
    url      = "https://cdcvs.fnal.gov/cvs/projects/artdaq-core"
    version('develop', git = 'http://cdcvs.fnal.gov/projects/artdaq-core', branch="develop", git_full_repo=True)

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')



    def url_for_version(self, version):
        url = 'https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/{0}.v{1}.tbz2'
        return url.format( version.underscored)


    depends_on('art')
    depends_on('boost')
    depends_on('canvas')
    depends_on('canvas-root-io')
    depends_on('art-root-io')
    depends_on('cetmodules', type='build')
    depends_on('cetbuildtools', type='build')
    depends_on('clhep')
    depends_on('fhicl-cpp')
    depends_on('messagefacility')
    depends_on('root')
    depends_on('sqlite')
    depends_on('tbb')
    depends_on('trace')

    patch('cetmodules2.patch')

    def patch(self):
        filter_file(r'add_subdirectory\(ups\)','if(WANT_UPS)\nadd_subdirectory(ups)\nendif()','CMakeLists.txt')

    def setup_build_environment(self, spack_env):
        spack_env.set('MESSAGEFACILITY_VERSION', self.spec['messagefacility'].version)
        spack_env.set('CANVAS_VERSION', self.spec['canvas'].version)
        spack_env.set('FHICLCPP_VERSION', self.spec['fhicl-cpp'].version)
        spack_env.set('CETBUILDTOOLS_VERSION', self.spec['cetmodules'].version)
        spack_env.set('CETBUILDTOOLS_DIR', self.spec['cetmodules'].prefix) 
        spack_env.set('LD_LIBRARY_PATH', self.spec['root'].prefix.lib)
        spack_env.set('DISABLE_DOXYGEN', '1')
 
    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value),
                '-DCANVAS_VERSION=v%s' % self.spec['canvas'].version.underscored,
                '-DMESSAGEFACILITY_VERSION=v%s' % self.spec['messagefacility'].version.underscored,
                '-DBoost_SYSTEM_LIBRARY=-lboost_system-mt',
                '-DBoost_DATE_TIME_LIBRARY=-lboost_date_time',
                '-DBoost_FILESYSTEM_LIBRARY=-lboost_filesystem',
                '-DBoost_THREAD_LIBRARY=-lboost_thread',
               ]
        return args

    @run_after('install')
    def rename_README(self):
        import os
        os.rename( join_path(self.spec.prefix, "README"),
                   join_path(self.spec.prefix, "README_%s"%self.spec.name))
