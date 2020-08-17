# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Trace(CMakePackage):
    """TRACE is yet another logging (time stamp) tool, but it allows 
fast and/or slow logging - dynamically (you choose)."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/trace/wiki"
    git_base = "https://cdcvs.fnal.gov/projects/trace-git/"

    parallel = False 

    depends_on('cetmodules', type='build')

    patch('trace-3.15.05.patch',when='@3.15.05')
    patch('trace-3.15.07.patch',when='@3.15.07')

    def url_for_version(self, version):
        url = 'https://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/{0}.v{1}.tbz2'
        return url.format(self.name + '-git', version.underscored)

    def cmake_args(self):
        args = ['-Dproduct=trace',
                '-Dtrace_include_dir={0}'.
                format(self.spec.prefix.include),
               ]
        return args
