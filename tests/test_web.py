"""Pruebas del formulario real y de la presentación de sus resultados."""

from html.parser import HTMLParser
import unittest

from app import app


class Inputs(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.fields = {}
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "input" and "name" in attrs:
            self.fields[attrs["name"]] = attrs


class InvestmentPageTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.data = {
            f"{bank}_{year}": str(rate)
            for bank, rates in [
                ("Banco Provincia", [36, 38, 40]),
                ("Banco Nacion", [39, 41, 43]),
                ("Banco Hipotecario", [34, 37, 38.5]),
            ]
            for year, rate in enumerate(rates, 1)
        }

    def test_initial_page_has_nine_empty_labeled_inputs_and_no_results(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        fields = Inputs(html).fields
        self.assertEqual(set(fields), set(self.data))
        self.assertTrue(all(field["value"] == "" for field in fields.values()))
        self.assertNotIn('class="winner-row"', html)
        self.assertIn('lang="es-AR"', html)

    def test_submission_shows_real_winner_and_retains_every_input(self):
        response = self.client.post("/", data=self.data)
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertEqual(html.count('class="period-count"'), 9)
        self.assertEqual(html.count('class="winner-row"'), 1)
        self.assertIn('Capitalización mensual · 1 año', html)
        self.assertIn('$422,053.42', html)
        self.assertIn('$1,272,053.42', html)
        self.assertIn('36.50<span>%</span>', html)
        fields = Inputs(html).fields
        self.assertEqual({name: attrs["value"] for name, attrs in fields.items()}, self.data)

    def test_invalid_rates_show_error_and_preserve_other_inputs(self):
        bad_field = "Banco Nacion_2"
        for bad_value in ["", "texto", "-1", "nan", "inf"]:
            with self.subTest(value=bad_value):
                data = {**self.data, bad_field: bad_value}
                response = self.client.post("/", data=data)
                self.assertEqual(response.status_code, 200)
                html = response.get_data(as_text=True)
                self.assertIn('role="alert"', html)
                self.assertNotIn('class="winner-row"', html)
                fields = Inputs(html).fields
                self.assertEqual(fields[bad_field]["aria-invalid"], "true")
                self.assertEqual(fields["Banco Provincia_1"]["value"], "36")

    def test_missing_rate_is_reported_without_server_error(self):
        self.data.pop("Banco Hipotecario_3")
        response = self.client.post("/", data=self.data)
        self.assertEqual(response.status_code, 200)
        fields = Inputs(response.get_data(as_text=True)).fields
        self.assertEqual(fields["Banco Hipotecario_3"]["aria-invalid"], "true")

    def test_zero_rates_are_accepted_and_render_without_division_by_zero(self):
        response = self.client.post("/", data=dict.fromkeys(self.data, "0"))
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertNotIn('role="alert"', html)
        self.assertEqual(html.count('class="period-count"'), 9)
        self.assertIn('$850,000.00', html)

    def test_local_assets_are_available_without_external_services(self):
        for path in [
            "style.css", "app.js", "favicon.svg",
            "fonts/geist-latin-400-normal.woff2",
            "fonts/geist-mono-latin-500-normal.woff2",
        ]:
            with self.subTest(asset=path):
                response = self.client.get(f"/static/{path}")
                self.assertEqual(response.status_code, 200)
                response.close()


if __name__ == "__main__":
    unittest.main()
