
from spack import *

class IcarusData(Package):
    """Bundle of data files for icarus"""

    homepage = "https://icarus.fnal.gov/"
    url      = "https://scisoft.fnal.gov/scisoft/packages/icarus_data/v09_26_00/icarus_data-09.26.00-noarch.tar.bz2"

    version('09.26.00')

    def install(self, spec, prefix):
        copy_files(self.build_dir, prefix)

    def setup_run_environment(self, env):
        env.set('ICARUS_DATA_VERSION', 'v%' % self.version.underscored )
        env.prepend_path('WIRECELL_PATH', '%s/icarus_data/WirecellData'  % self.prefix )
        env.prepend_path('FW_SEARCH_PATH', '%s/icarus_data'  % self.prefix )
        env.prepend_path('FW_SEARCH_PATH', '%s/icarus_data/NoiseHistos'  % self.prefix )
        env.prepend_path('FW_SEARCH_PATH', '%s/icarus_data/Responses'  % self.prefix )
        env.prepend_path('FW_SEARCH_PATH', '%s/icarus_data/PhotonLibrary'  % self.prefix )
        env.prepend_path('FW_SEARCH_PATH', '%s/icarus_data/CRT'  % self.prefix )
        env.prepend_path('FW_SEARCH_PATH', '%s/icarus_data/PandoraMVAs'  % self.prefix )
        env.prepend_path('FW_SEARCH_PATH', '%s/icarus_data/database'  % self.prefix )
        env.prepend_path('CMAKE_PREFIX_PATH', '%s'  % self.prefix )
        env.prepend_path('PKG_CONFIG_PATH', '%s'  % self.prefix )

