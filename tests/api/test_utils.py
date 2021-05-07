from django.test import TestCase

from egl_rest.api.helpers import md5_string, get_country, get_geo_coords


class TestUtils(TestCase):

    def test_md5(self):
        str1 = "Y023hAJK#@)(#<><>"
        str2 = "Y023hAJK#@)(#<><>"
        str3 = "Y023"
        self.assertEqual(md5_string(str1), md5_string(str2))
        self.assertNotEqual(md5_string(str1), md5_string(str3))

    def test_get_country(self):
        country = get_country(41.947239, -87.655636)
        self.assertEquals(country.official_name, "United States of America")

    # def test_get_gro_cords(self):
    #     geo_cords = get_geo_coords("CERN")
    #     latitude = geo_cords['latitude']
    #     longitude = geo_cords['longitude']
    #     self.assertEquals(latitude, 46.2338702)
    #     self.assertEquals(longitude, 6.04698691754795)