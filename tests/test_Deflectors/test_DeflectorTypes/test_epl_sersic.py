from slsim.Deflectors.DeflectorTypes.epl_sersic import EPLSersic
from astropy.cosmology import FlatLambdaCDM
from lenstronomy.Cosmo.lens_cosmo import LensCosmo


class TestEPLSersic(object):
    """
    required quantities in dictionary:
    - 'velocity_dispersion': SIS equivalent velocity dispersion of the deflector
    - 'e1_mass': eccentricity of NFW profile
    - 'e2_mass': eccentricity of NFW profile
    - 'angular_size': half-light radius of stellar/light profile in radian
    - 'e1_light': eccentricity of light
    - 'e2_light': eccentricity of light
    - 'z': redshift of deflector
    """

    def setup_method(self):
        self.deflector_dict = {
            "vel_disp": 200,
            "e1_mass": 0.1,
            "e2_mass": -0.1,
            "angular_size": 0.001,
            "n_sersic": 1,
            "e1_light": -0.1,
            "e2_light": 0.1,
            "z": 0.5,
        }
        self.epl_sersic = EPLSersic(deflector_dict=self.deflector_dict)

    def test_redshift(self):
        z = self.epl_sersic.redshift
        assert self.deflector_dict["z"] == z

    def test_velocity_dispersion(self):
        vel_disp = self.epl_sersic.velocity_dispersion()
        assert vel_disp == self.deflector_dict["vel_disp"]

    def test_mass_model_lenstronomy(self):
        cosmo = FlatLambdaCDM(H0=70, Om0=0.3)
        lens_cosmo = LensCosmo(
            cosmo=cosmo, z_lens=self.deflector_dict["z"], z_source=2.0
        )
        lens_mass_model_list, kwargs_lens_mass = self.epl_sersic.mass_model_lenstronomy(
            lens_cosmo=lens_cosmo
        )
        assert len(lens_mass_model_list) == 1

    def test_halo_porperties(self):
        gamma = self.epl_sersic.halo_properties
        assert gamma == 2
