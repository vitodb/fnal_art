from spack import *
import glob
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))



class Geant4G4tendl(Package):

    url = "http://scisoft.fnal.gov/scisoft/packages/g4tendl/v1_3/g4tendl-1.3-noarch.tar.bz2"

    version('1.3', 'fd29c45fe2de432f1f67232707b654c0')

    def install(self, spec, prefix):
        install_tree(self.stage.source_path, prefix)

    def url_for_version(self, version):
        """Handle version string."""
        return ("http://scisoft.fnal.gov/scisoft/packages/g4tendl/v%s/g4tendl-%s-noarch.tar.bz2" % (version.underscored,version))
