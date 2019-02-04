# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import platform


class Geant4(CMakePackage):
    """Geant4 is a toolkit for the simulation of the passage of particles
    through matter. Its areas of application include high energy, nuclear
    and accelerator physics, as well as studies in medical and space
    science."""

    homepage = "http://geant4.cern.ch/"
    url = "http://geant4.cern.ch/support/source/geant4.10.01.p03.tar.gz"

    version('10.03.p03', 'ccae9fd18e3908be78784dc207f2d73b')

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    variant('qt', default=False, description='Enable Qt support')
    variant('vecgeom', default=False, description='Enable Vecgeom support')

    depends_on('cmake@3.5:', type='build')

    depends_on("clhep")
    depends_on("expat")
    depends_on("xerces-c")
    depends_on("qt@4.8:4.9999", when="+qt")
    # G4 data
    depends_on("geant4-g4abla")
    depends_on("geant4-g4emlow")
    depends_on("geant4-g4neutron")
    depends_on("geant4-g4neutronxs")
    depends_on("geant4-g4nuclide")
    depends_on("geant4-g4photon")
    depends_on("geant4-g4pii")
    depends_on("geant4-g4radiative")
    depends_on("geant4-g4surface")
    depends_on("geant4-g4tendl")


    patch('cxx17.patch', when='cxxstd=17')

    def cmake_args(self):
        spec = self.spec

        options = [	'-DGEANT4_USE_SYSTEM_CLHEP=ON',
			     '-DCLHEP_ROOT_DIR:STRING="%s"' % self.spec['clhep'].prefix,
			     '-DBUILD_STATIC_LIBS=ON',
			     '-DGEANT4_USE_OPENGL_X11=ON',
			     '-DGEANT4_USE_GDML=ON',
			     '-DXERCESC_ROOT_DIR:STRING="%s"' % self.spec['xerces-c'].prefix 
                  ]

        options.append('-DGEANT4_BUILD_CXXSTD=%s' % self.spec.variants['cxxstd'].value)


        if '+qt' in spec:
            options.append('-DGEANT4_USE_QT=ON')
            options.append(
                '-DQT_QMAKE_EXECUTABLE=%s' %
                spec['qt'].prefix + '/bin/qmake'
            )

        if '+vecgeom' in spec:
            options.append('-DGEANT4_USE_USOLIDS=ON')
            options.append('-DUSolids_DIR=%s' %
                           join_path(spec['vecgeom'].prefix, 'lib/CMake/USolids'))

 
        return options

    def url_for_version(self, version):
        """Handle Geant4's unusual version string."""
        return ("http://geant4.cern.ch/support/source/geant4.%s.tar.gz" % version)
