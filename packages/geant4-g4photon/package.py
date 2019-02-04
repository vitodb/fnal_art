from spack import *
import glob
import sys,os

class Geant4G4photon(Package):

    url = "http://scisoft.fnal.gov/scisoft/packages/g4photon/v4_3_2/g4photon-4.3.2-noarch.tar.bz2"

    version('4.3.2', '15e249b54a210b812c9827c3f4a66dad1521afe3028f979b74fcb1c4e6c6974d')

    def install(self, spec, prefix):

        install_tree(self.stage.source_path, prefix)

    def url_for_version(self, version):
        """Handle version string."""
        return ("http://scisoft.fnal.gov/scisoft/packages/g4photon/v%s/g4photon-%s-noarch.tar.bz2" % (version.underscore,version))

