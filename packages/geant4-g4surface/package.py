from spack import *
import sys,os

class Geant4G4surface(Package):

    url = "http://scisoft.fnal.gov/scisoft/packages/g4surface/v1_0/g4surface-1.0-noarch.tar.bz2"

    version('1.0', 'dc16393faee6ecb6dc0c22d8a1b12e8bb38f959e5c3d02b9cc78bb2072280401')

    def install(self, spec, prefix):
        install_tree(self.stage.source_path, prefix)

    def url_for_version(self, version):
        """Handle version string."""
        return ("http://scisoft.fnal.gov/scisoft/packages/g4surface/v%s/g4surface-%s-noarch.tar.bz2" % (version.underscored,version))

