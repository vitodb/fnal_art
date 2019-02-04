from spack import *
import glob
import sys,os

class Geant4G4nucleonxs(Package):

    url = "http://scisoft.fnal.gov/scisoft/packages/g4nucleonxs/v1_1/g4nucleonxs-1.1-noarch.tar.bz2"

    version('1.1', 'adda2e6d1102dfbe2502116edaa03fc736394099bf9027fa732a77d2551b4234')

    def install(self, spec, prefix):
        mkdirp(join_path(prefix.share, 'data'))
        install_path = join_path(prefix.share, 'data',
                                 os.path.basename(self.stage.source_path))
        install_tree(self.stage.source_path, install_path)

    def url_for_version(self, version):
        """Handle version string."""
        return "http://scisoft.fnal.gov/scisoft/packages/g4nucleonxs/v1_1/g4nucleonxs-1.1-noarch.tar.bz2" % (version,version)
