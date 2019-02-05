from spack import *
import glob
import sys,os

class Geant4G4radiative(Package):

    url = "http://scisoft.fnal.gov/scisoft/packages/g4radiative/v5_1_1/g4radiative-5.1.1-noarch.tar.bz2"

    version('5.1.1', 'b0fb3ba718e490b79a92c923ec804e00f20cb034fa833386063cacc9f5d96170')

    def install(self, spec, prefix):
        install_tree(self.stage.source_path, prefix)

    def url_for_version(self, version):
        """Handle version string."""
        return ("http://scisoft.fnal.gov/scisoft/packages/g4radiative/v%s/g4radiative-%s-noarch.tar.bz2" % (version.underscored,version))
