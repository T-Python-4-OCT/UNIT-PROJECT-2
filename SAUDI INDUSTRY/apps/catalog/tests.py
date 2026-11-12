from django.test import SimpleTestCase
from django.urls import reverse


class IndustryTests(SimpleTestCase):

    def test_industries_page(self):
        response = self.client.get(
            reverse("catalog:industries")
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["industries"]),
            6
        )

    def test_search(self):
        response = self.client.get(
            reverse("catalog:industries"),
            {"q": "pharma"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["industries"][0]["slug"],
            "pharmaceuticals"
        )
        self.assertEqual(
            len(response.context["industries"]),
            1
        )

    def test_category_filter(self):
        response = self.client.get(
            reverse("catalog:industries"),
            {"category": "Vehicle Manufacturing"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["industries"]),
            1
        )

    def test_industry_detail(self):
        response = self.client.get(
            reverse(
                "catalog:industry_detail",
                args=["petrochemicals"]
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Petrochemicals")

    def test_invalid_industry(self):
        response = self.client.get(
            reverse(
                "catalog:industry_detail",
                args=["unknown-industry"]
            )
        )

        self.assertEqual(response.status_code, 404)

class CompanyTests(SimpleTestCase):

    def test_companies_page(self):
        response = self.client.get(
            reverse("catalog:companies")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "catalog/companies.html"
        )
        self.assertEqual(
            len(response.context["companies"]),
            6
        )

    def test_external_company_image_url(self):
        image_url = (
            "https://res.cloudinary.com/ew4jvlxr/image/upload/"
            "v1794407447/sabic.jpg"
        )

        response = self.client.get(
            reverse("catalog:companies")
        )

        self.assertContains(response, f'src="{image_url}"')

        response = self.client.get(
            reverse(
                "catalog:company_detail",
                args=["sabic"]
            )
        )

        self.assertContains(response, f'src="{image_url}"')

    def test_company_search(self):
        response = self.client.get(
            reverse("catalog:companies"),
            {"q": "SABIC"}
        )

        self.assertEqual(response.status_code, 200)

        companies = response.context["companies"]

        self.assertEqual(len(companies), 1)
        self.assertEqual(
            companies[0]["slug"],
            "sabic"
        )

    def test_industry_filter(self):
        response = self.client.get(
            reverse("catalog:companies"),
            {"industry": "automotive"}
        )

        self.assertEqual(response.status_code, 200)

        companies = response.context["companies"]

        self.assertEqual(len(companies), 1)
        self.assertEqual(
            companies[0]["name"],
            "Ceer"
        )

    def test_location_filter(self):
        response = self.client.get(
            reverse("catalog:companies"),
            {"location": "Riyadh"}
        )

        self.assertEqual(response.status_code, 200)

        companies = response.context["companies"]

        self.assertGreater(len(companies), 0)

        for company in companies:
            self.assertEqual(
                company["location"],
                "Riyadh"
            )

    def test_combined_filters(self):
        response = self.client.get(
            reverse("catalog:companies"),
            {
                "q": "alfanar",
                "industry": "energy-technologies",
                "location": "Riyadh"
            }
        )

        self.assertEqual(response.status_code, 200)

        companies = response.context["companies"]

        self.assertEqual(len(companies), 1)
        self.assertEqual(
            companies[0]["slug"],
            "alfanar"
        )

    def test_company_detail(self):
        response = self.client.get(
            reverse(
                "catalog:company_detail",
                args=["ceer"]
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "catalog/company_detail.html"
        )
        self.assertEqual(
            response.context["company"]["slug"],
            "ceer"
        )
        self.assertContains(
            response,
            "King Abdullah Economic City"
        )
        self.assertContains(
            response,
            "Automotive"
        )

    def test_invalid_company(self):
        response = self.client.get(
            reverse(
                "catalog:company_detail",
                args=["unknown-company"]
            )
        )

        self.assertEqual(
            response.status_code,
            404
        )

    def test_empty_search_results(self):
        response = self.client.get(
            reverse("catalog:companies"),
            {"q": "nonexistent-company-xyz"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["companies"]),
            0
        )
        self.assertContains(
            response,
            "No Companies Found"
        )

    def test_company_industry_relationships(self):
        from .content_loader import load_json

        companies = load_json("companies.json")["companies"]
        industries = load_json("industries.json")["industries"]

        industry_slugs = {
            industry["slug"]
            for industry in industries
        }

        for company in companies:
            self.assertIn(
                company["industry_slug"],
                industry_slugs
            )

class IndustrialCityTests(SimpleTestCase):

    def test_industrial_cities_page(self):
        response = self.client.get(
            reverse("catalog:industrial_cities")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "catalog/industrial_cities.html"
        )
        self.assertEqual(
            len(response.context["industrial_cities"]),
            6
        )

    def test_external_industrial_city_image_url(self):
        image_url = (
            "https://res.cloudinary.com/ew4jvlxr/image/upload/"
            "v1794414334/%D9%81%D9%86%D8%AF%D9%82_%D8%A7%D9%84"
            "%D9%85%D9%88%D9%81%D9%86%D8%A8%D9%8A%D9%83_%D8%A8"
            "%D9%8A%D9%86%D8%A8%D8%B9_%D8%A7%D9%84%D8%B5%D9%86"
            "%D8%A7%D8%B9%D9%8A%D8%A9.png"
        )

        response = self.client.get(
            reverse("catalog:industrial_cities")
        )

        self.assertContains(response, f'src="{image_url}"')

        response = self.client.get(
            reverse(
                "catalog:industrial_city_detail",
                args=["yanbu-industrial-city"]
            )
        )

        self.assertContains(response, f'src="{image_url}"')

    def test_city_search(self):
        response = self.client.get(
            reverse("catalog:industrial_cities"),
            {"q": "jUbAiL"}
        )

        self.assertEqual(response.status_code, 200)

        cities = response.context["industrial_cities"]

        self.assertEqual(len(cities), 2)
        city_slugs = {
            city["slug"]
            for city in cities
        }
        self.assertEqual(
            city_slugs,
            {
                "jubail-industrial-city",
                "ras-al-khair"
            }
        )

    def test_search_related_industry(self):
        response = self.client.get(
            reverse("catalog:industrial_cities"),
            {"q": "automotive"}
        )

        self.assertEqual(response.status_code, 200)

        cities = response.context["industrial_cities"]

        self.assertEqual(len(cities), 1)
        self.assertEqual(
            cities[0]["slug"],
            "kaec-industrial-valley"
        )

    def test_region_filter(self):
        response = self.client.get(
            reverse("catalog:industrial_cities"),
            {"region": "Eastern Province"}
        )

        self.assertEqual(response.status_code, 200)

        cities = response.context["industrial_cities"]

        self.assertEqual(len(cities), 2)

        for city in cities:
            self.assertEqual(
                city["region"],
                "Eastern Province"
            )

    def test_type_filter(self):
        response = self.client.get(
            reverse("catalog:industrial_cities"),
            {"type": "Industrial Valley"}
        )

        self.assertEqual(response.status_code, 200)

        cities = response.context["industrial_cities"]

        self.assertEqual(len(cities), 1)
        self.assertEqual(
            cities[0]["slug"],
            "kaec-industrial-valley"
        )

    def test_combined_filters(self):
        response = self.client.get(
            reverse("catalog:industrial_cities"),
            {
                "q": "automotive",
                "region": "Makkah Region",
                "type": "Industrial Valley"
            }
        )

        self.assertEqual(response.status_code, 200)

        cities = response.context["industrial_cities"]

        self.assertEqual(len(cities), 1)
        self.assertEqual(
            cities[0]["slug"],
            "kaec-industrial-valley"
        )

    def test_industrial_city_detail(self):
        response = self.client.get(
            reverse(
                "catalog:industrial_city_detail",
                args=["kaec-industrial-valley"]
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "catalog/industrial_city_detail.html"
        )
        self.assertEqual(
            response.context["city"]["slug"],
            "kaec-industrial-valley"
        )
        self.assertContains(
            response,
            "King Abdullah Economic City"
        )
        self.assertContains(
            response,
            "Automotive"
        )

    def test_invalid_industrial_city(self):
        response = self.client.get(
            reverse(
                "catalog:industrial_city_detail",
                args=["unknown-industrial-city"]
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_empty_search_results(self):
        response = self.client.get(
            reverse("catalog:industrial_cities"),
            {"q": "nonexistent-city-xyz"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["industrial_cities"]),
            0
        )
        self.assertContains(
            response,
            "No Industrial Locations Found"
        )

    def test_city_industry_relationships(self):
        from .content_loader import load_json

        cities = load_json(
            "industrial_cities.json"
        )["industrial_cities"]

        industries = load_json(
            "industries.json"
        )["industries"]

        industry_slugs = {
            industry["slug"]
            for industry in industries
        }

        for city in cities:
            for slug in city["industry_slugs"]:
                self.assertIn(slug, industry_slugs)

    def test_city_without_related_industries(self):
        response = self.client.get(
            reverse(
                "catalog:industrial_city_detail",
                args=["riyadh-second-industrial-city"]
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["city"]["industries"],
            []
        )
        self.assertContains(
            response,
            "Specific industry categories have not"
        )

class ProductTests(SimpleTestCase):

    def test_products_page(self):
        response = self.client.get(
            reverse("catalog:made_in_saudi")
        )

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(
            response,
            "catalog/made_in_saudi.html"
        )

        self.assertEqual(
            len(response.context["products"]),
            6
        )

    def test_external_product_image_url(self):
        image_url = (
            "https://res.cloudinary.com/ew4jvlxr/image/upload/"
            "v1794414893/images_1.jpg"
        )

        response = self.client.get(
            reverse("catalog:made_in_saudi")
        )

        self.assertContains(response, f'src="{image_url}"')

        response = self.client.get(
            reverse(
                "catalog:product_detail",
                args=["polyethylene-resin"]
            )
        )

        self.assertContains(response, f'src="{image_url}"')

    def test_product_search(self):
        response = self.client.get(
            reverse("catalog:made_in_saudi"),
            {"q": "mIlK"}
        )

        self.assertEqual(response.status_code, 200)

        products = response.context["products"]

        self.assertEqual(len(products), 1)
        self.assertEqual(
            products[0]["slug"],
            "fresh-milk"
        )

    def test_search_by_manufacturer(self):
        response = self.client.get(
            reverse("catalog:made_in_saudi"),
            {"q": "SABIC"}
        )

        self.assertEqual(response.status_code, 200)

        products = response.context["products"]

        self.assertEqual(len(products), 1)
        self.assertEqual(
            products[0]["slug"],
            "polyethylene-resin"
        )

    def test_industry_filter(self):
        response = self.client.get(
            reverse("catalog:made_in_saudi"),
            {"industry": "mining-metals"}
        )

        self.assertEqual(response.status_code, 200)

        products = response.context["products"]

        self.assertEqual(len(products), 2)

        product_slugs = {
            product["slug"]
            for product in products
        }

        self.assertEqual(
            product_slugs,
            {
                "rolled-aluminium",
                "phosphate-fertilizer"
            }
        )

    def test_category_filter(self):
        response = self.client.get(
            reverse("catalog:made_in_saudi"),
            {"category": "Medicines"}
        )

        self.assertEqual(response.status_code, 200)

        products = response.context["products"]

        self.assertEqual(len(products), 1)
        self.assertEqual(
            products[0]["slug"],
            "pharmaceutical-tablets"
        )

    def test_combined_filters(self):
        response = self.client.get(
            reverse("catalog:made_in_saudi"),
            {
                "q": "Almarai",
                "industry": "food-manufacturing",
                "category": "Dairy Products"
            }
        )

        self.assertEqual(response.status_code, 200)

        products = response.context["products"]

        self.assertEqual(len(products), 1)
        self.assertEqual(
            products[0]["slug"],
            "fresh-milk"
        )

    def test_search_by_production_location(self):
        response = self.client.get(
            reverse("catalog:made_in_saudi"),
            {"q": "Al-Kharj"}
        )

        self.assertEqual(response.status_code, 200)

        products = response.context["products"]

        self.assertEqual(len(products), 1)
        self.assertEqual(
            products[0]["slug"],
            "fresh-milk"
        )

    def test_product_detail(self):
        response = self.client.get(
            reverse(
                "catalog:product_detail",
                args=["fresh-milk"]
            )
        )

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(
            response,
            "catalog/product_detail.html"
        )

        self.assertEqual(
            response.context["product"]["slug"],
            "fresh-milk"
        )

        self.assertContains(response, "Almarai")
        self.assertContains(response, "Raw Materials")
        self.assertContains(response, "Manufacturing Process")
        self.assertContains(
            response,
            "Where Is This Product Used?"
        )
        self.assertContains(
            response,
            "Direct consumption"
        )

    def test_all_product_detail_pages(self):
        from .content_loader import load_json

        products = load_json("products.json")["products"]

        for product in products:
            with self.subTest(product=product["slug"]):
                response = self.client.get(
                    reverse(
                        "catalog:product_detail",
                        args=[product["slug"]]
                    )
                )

                self.assertEqual(
                    response.status_code,
                    200
                )

                self.assertContains(
                    response,
                    product["name"]
                )

    def test_invalid_product(self):
        response = self.client.get(
            reverse(
                "catalog:product_detail",
                args=["unknown-product"]
            )
        )

        self.assertEqual(
            response.status_code,
            404
        )

    def test_empty_search_results(self):
        response = self.client.get(
            reverse("catalog:made_in_saudi"),
            {"q": "nonexistent-product-xyz"}
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            len(response.context["products"]),
            0
        )

        self.assertContains(
            response,
            "No Products Found"
        )

    def test_product_relationships(self):
        from .content_loader import load_json

        products = load_json("products.json")["products"]
        industries = load_json("industries.json")["industries"]
        companies = load_json("companies.json")["companies"]

        industry_slugs = {
            industry["slug"]
            for industry in industries
        }

        company_slugs = {
            company["slug"]
            for company in companies
        }

        for product in products:
            self.assertIn(
                product["industry_slug"],
                industry_slugs
            )

            self.assertIn(
                product["company_slug"],
                company_slugs
            )

    def test_manufacturing_information(self):
        from .content_loader import load_json

        products = load_json("products.json")["products"]

        for product in products:
            with self.subTest(product=product["slug"]):
                self.assertTrue(
                    product["raw_materials"]
                )

                self.assertTrue(
                    product["production_steps"]
                )

                self.assertTrue(
                    product["applications"]
                )
