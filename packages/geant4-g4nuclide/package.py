from spack import *
import glob
import sys,os

class Geant4G4nuclide(Package):

    url = "http://scisoft.fnal.gov/scisoft/packages/g4nuclide/v2_2/g4nuclide-2.2-noarch.tar.bz2"

    version('2.1', 'b3331cc1f685781de8208e05a0e376ac174d08fd1b04385029521993fcb33b2d')

    def install(self, spec, prefix):
        install_tree(self.stage.source_path, prefix)

    def url_for_version(self, version):
        """Handle version string."""
        return "http://scisoft.fnal.gov/scisoft/packages/g4nuclide/v%s/g4nuclide-%s-noarch.tar.bz2" % (version.underscore,version)
