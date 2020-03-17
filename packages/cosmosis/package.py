# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install cosmosis
#
# You can edit this file again by typing:
#
#     spack edit cosmosis
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *
import os

class Cosmosis(MakefilePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    #url      = "https://bitbucket.org/joezuntz/cosmosis/get/v1.6.2.tar.bz2"
    git      = 'https://bitbucket.org/joezuntz/cosmosis.git'

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    #version('1.6.2', sha256='b4e5edb9c144b8bf404a3af554f526f52494c48e81c47c53d61d172d27b823b1')
    version('1.6.2', tag='v1.6.2', submodules='True')

    # FIXME: Add dependencies if required.
    # depends_on('foo')
    depends_on('python@3.8.1:')
    #depends_on('gcc@8.3.0:')
    depends_on('py-configparser')
    depends_on('py-future')
    depends_on('py-ipython')
    depends_on('py-python-dateutil')
    depends_on('py-tornado')
    depends_on('py-astropy')
    depends_on('py-matplotlib@2.0.0:')
    depends_on('py-mpi4py')
    depends_on('py-emcee')
    depends_on('py-numpy')
    depends_on('py-pyyaml')
    depends_on('py-cython')
    depends_on('py-scipy')
    depends_on('mpich')
    depends_on('openblas')
    depends_on('gsl')
    depends_on('fftw')
    depends_on('minuit')
    depends_on('sqlite')
    depends_on('cfitsio')
    depends_on('cosmosis-standard-library')
    #depends_on('')


    #phases = ['build', 'install']
    #phases = ['build']

    def setup_build_environment(self, env):
        """Set up the build environment for this package."""
        env.set('COSMOSIS_SRC_DIR', self.prefix)
        env.set('LAPACK_LINK','-lopenblas')
        env.set('GSL_INC', self.spec['gsl'].prefix+'/include')
        env.set('GSL_LIB', self.spec['gsl'].prefix+'/lib')
        env.set('MINUIT2_INC', self.spec['minuit'].prefix+'/include')
        env.set('MINUIT2_LIB', self.spec['minuit'].prefix+'/lib')
        env.set('CFITSIO_INC', self.spec['cfitsio'].prefix+'/include')
        env.set('CFITSIO_LIB', self.spec['cfitsio'].prefix+'/lib')

    #def build(self, spec, prefix):
    #    os.symlink(self.spec['cosmosis-standard-library'].prefix, self.build_directory+'/cosmosis-standard-library')
    #    make()

    #def install(self, spec, prefix):
    #    install_tree('.', prefix)

    def build(self, spec, prefix):
        import inspect
        install_tree('.',prefix)
        os.symlink(self.spec['cosmosis-standard-library'].prefix, prefix+'/cosmosis-standard-library')
        print('prefix', prefix) 
        with working_dir(prefix):
            inspect.getmodule(self).make(*self.build_targets)

    def install(self, spec, prefix):
        # it is already there..
        pass

    def setup_run_environment(self, env):
        env.prepend_path('PATH', self.prefix+'/bin')
        env.prepend_path('PYTHONPATH', self.prefix)
        env.prepend_path('LD_LIBRARY_PATH',self.prefix+'/cosmosis/datablock')
        env.prepend_path('LD_LIBRARY_PATH',self.prefix+'/cosmosis-standard-library/likelihood/planck/plc-1.0/lib')
        env.prepend_path('LD_LIBRARY_PATH',self.prefix+'/cosmosis-standard-library/likelihood/planck2015/plc-2.0/lib')
        env.set('COSMOSIS_SRC_DIR', self.prefix)

#    def edit(self, spec, prefix):
        # FIXME: Edit the Makefile if necessary
        # FIXME: If not needed delete this function
        # makefile = FileFilter('Makefile')
        # makefile.filter('CC = .*', 'CC = cc')
