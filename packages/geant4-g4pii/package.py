from spack import *
import glob
import sys,os

class Geant4G4pii(Package):

    url = "http://scisoft.fnal.gov/scisoft/packages/g4pii/v1_3/g4pii-1.3-noarch.tar.bz2"

    version('1.3', '2d1c88798bbea00f003bc38f5c7222865eb5c679ebf02b611ce8e7644bec02ec')

    def install(self, spec, prefix):
        install_tree(self.stage.source_path, prefix)

    def url_for_version(self, version):
        """Handle version string."""
        return ("http://scisoft.fnal.gov/scisoft/packages/g4pii/v%s/g4pii-%s-noarch.tar.bz2" % (version.underscored,version))
