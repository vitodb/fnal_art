from spack import *
import glob
import sys,os

class Geant4G4neutronxs(Package):

    url = "http://scisoft.fnal.gov/scisoft/packages/g4neutronxs/v1_4/g4neutronxs-1.4-noarch.tar.bz2"

    version('1.4', '1d59d52bf91d9df70b71e8d9c823bf69c709f9ff264d2771308568628783a413')

    def install(self, spec, prefix):
        mkdirp(join_path(prefix.share, 'data'))
        install_path = join_path(prefix.share, 'data',
                                 os.path.basename(self.stage.source_path))
        install_tree(self.stage.source_path, install_path)

    def url_for_version(self, version):
        """Handle version string."""
        return "http://scisoft.fnal.gov/scisoft/packages/g4neutronxs/v%s/g4neutronxs-%s-noarch.tar.bz2" % (version.underscored,version)
