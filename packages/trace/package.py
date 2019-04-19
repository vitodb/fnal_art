# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Trace(CMakePackage):
    """TRACE is yet another logging (time stamp) tool, but it allows 
fast and/or slow logging - dynamically (you choose)."""

    homepage = "http://cdcvs.fnal.gov/redmine/projects/trace/wiki"
    git_base = "http://cdcvs.fnal.gov/projects/trace-git/"

    parallel = False 

    version('3.14.00', git=git_base, branch='feature/cetmodules', preferred=True)

    depends_on('cetmodules', type='build')

    def url_for_version(self, version):
        url = 'http://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/{0}.v{1}.tbz2'
        return url.format(self.name, version.underscored)

    def cmake_args(self):
        args = ['-Dproduct=trace',
                '-Dtrace_include_dir={0}'.
                format(self.spec.prefix.include),
               ]
        return args
