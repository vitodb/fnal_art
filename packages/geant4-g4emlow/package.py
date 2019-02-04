from spack import *
import glob
import sys,os

class Geant4G4emlow(Package):

    url = "http://scisoft.fnal.gov/scisoft/packages/g4emlow/v6_50/g4emlow-6.50-noarch.tar.bz2"

    version('6.50', '44d3317fe4c2e64297d0d57ec8ac9e7f4cd6ed027ca6d5ab3ac9a7b04d16d07a')

    def install(self, spec, prefix):
       install_tree(self.stage.source_path, prefix)

    def url_for_version(self, version):
        """Handle version string."""
        return ("http://scisoft.fnal.gov/scisoft/packages/g4emlow/v%s/g4emlow-%s-noarch.tar.bz2" % (version.underscore,version))

