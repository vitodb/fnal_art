from spack import *
import glob
import sys,os

class Geant4G4abla(Package):

    url = "http://scisoft.fnal.gov/scisoft/packages/g4abla/v3_0/g4abla-3.0-noarch.tar.bz2"

    version('3.0', 'ca49a3e9f4ed1ad9d66611818a9a228a4bd1c2043b8934784fe741aa1e00bf1d')

    def install(self, spec, prefix):
        install_tree(self.stage.source_path, prefix)

    def url_for_version(self, version):
        """Handle version string."""
        return ("http://scisoft.fnal.gov/scisoft/packages/g4abla/v%s/g4abla-%s-noarch.tar.bz2" % (version.underscore,version))
