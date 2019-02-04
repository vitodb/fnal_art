from spack import *
import glob
import sys,os

class Geant4G4neutron(Package):

    url = "http://scisoft.fnal.gov/scisoft/packages/g4neutron/v4_5/g4neutron-4.5-noarch.tar.bz2"

    version('4.5', '51c741b501eea6306f03200ed0d5fedde5786f3abcf159ec740f748343849c9d')

    def install(self, spec, prefix):
        install_tree(self.stage.source_path, prefix)

    def url_for_version(self, version):
        """Handle version string."""
        return ("http://scisoft.fnal.gov/scisoft/packages/g4neutron/v%s/g4neutron-%s-noarch.tar.bz2" % (version.underscore,version))
