from django.http import Http404
from django.shortcuts import render

from .content_loader import load_json


def industries(request):
    data = load_json("industries.json")
    all_industries = data["industries"]

    search_query = request.GET.get("q", "").strip()
    selected_category = request.GET.get("category", "").strip()

    categories = sorted({
        industry["category"]
        for industry in all_industries
    })

    filtered_industries = all_industries

    if search_query:
        query = search_query.casefold()

        filtered_industries = [
            industry
            for industry in filtered_industries
            if query in industry["name"].casefold()
            or query in industry["description"].casefold()
            or query in industry["category"].casefold()
        ]

    if selected_category:
        filtered_industries = [
            industry
            for industry in filtered_industries
            if industry["category"] == selected_category
        ]

    context = {
        "industries": filtered_industries,
        "categories": categories,
        "search_query": search_query,
        "selected_category": selected_category,
        "total_industries": len(all_industries),
    }

    return render(request, "catalog/industries.html", context)


def industry_detail(request, slug):
    data = load_json("industries.json")

    industry = next(
        (
            item
            for item in data["industries"]
            if item["slug"] == slug
        ),
        None
    )

    if industry is None:
        raise Http404("Industry not found")

    return render(
        request,
        "catalog/industry_detail.html",
        {"industry": industry}
    )

def load_companies():
    companies_data = load_json("companies.json")
    industries_data = load_json("industries.json")

    industry_lookup = {
        industry["slug"]: industry
        for industry in industries_data["industries"]
    }

    return [
        {
            **company,
            "industry": industry_lookup[company["industry_slug"]]
        }
        for company in companies_data["companies"]
    ]


def companies(request):
    all_companies = load_companies()

    search_query = request.GET.get("q", "").strip()
    selected_industry = request.GET.get("industry", "").strip()
    selected_location = request.GET.get("location", "").strip()

    industry_options = sorted(
        {
            company["industry_slug"]: company["industry"]
            for company in all_companies
        }.values(),
        key=lambda industry: industry["name"]
    )

    locations = sorted({
        company["location"]
        for company in all_companies
    })

    filtered_companies = all_companies

    if search_query:
        query = search_query.casefold()

        filtered_companies = [
            company
            for company in filtered_companies
            if query in " ".join([
                company["name"],
                company["description"],
                company["industry"]["name"],
                company["location"],
            ]).casefold()
        ]

    if selected_industry:
        filtered_companies = [
            company
            for company in filtered_companies
            if company["industry_slug"] == selected_industry
        ]

    if selected_location:
        filtered_companies = [
            company
            for company in filtered_companies
            if company["location"] == selected_location
        ]

    context = {
        "companies": filtered_companies,
        "industry_options": industry_options,
        "locations": locations,
        "search_query": search_query,
        "selected_industry": selected_industry,
        "selected_location": selected_location,
        "total_companies": len(all_companies),
    }

    return render(request, "catalog/companies.html", context)


def company_detail(request, slug):
    all_companies = load_companies()

    company = next(
        (
            item
            for item in all_companies
            if item["slug"] == slug
        ),
        None
    )

    if company is None:
        raise Http404("Company not found")

    return render(
        request,
        "catalog/company_detail.html",
        {"company": company}
    )

def load_industrial_cities():
    cities_data = load_json("industrial_cities.json")
    industries_data = load_json("industries.json")

    industry_lookup = {
        industry["slug"]: industry
        for industry in industries_data["industries"]
    }

    return [
        {
            **city,
            "industries": [
                industry_lookup[slug]
                for slug in city["industry_slugs"]
                if slug in industry_lookup
            ]
        }
        for city in cities_data["industrial_cities"]
    ]


def industrial_cities(request):
    all_cities = load_industrial_cities()

    search_query = request.GET.get("q", "").strip()
    selected_region = request.GET.get("region", "").strip()
    selected_type = request.GET.get("type", "").strip()

    regions = sorted({
        city["region"]
        for city in all_cities
    })

    city_types = sorted({
        city["type"]
        for city in all_cities
    })

    filtered_cities = all_cities

    if search_query:
        query = search_query.casefold()

        filtered_cities = [
            city
            for city in filtered_cities
            if query in " ".join([
                city["name"],
                city["description"],
                city["location"],
                city["region"],
                city["type"],
                " ".join(city["key_features"]),
                " ".join(
                    industry["name"]
                    for industry in city["industries"]
                ),
            ]).casefold()
        ]

    if selected_region:
        filtered_cities = [
            city
            for city in filtered_cities
            if city["region"] == selected_region
        ]

    if selected_type:
        filtered_cities = [
            city
            for city in filtered_cities
            if city["type"] == selected_type
        ]

    context = {
        "industrial_cities": filtered_cities,
        "regions": regions,
        "city_types": city_types,
        "search_query": search_query,
        "selected_region": selected_region,
        "selected_type": selected_type,
        "total_cities": len(all_cities),
    }

    return render(
        request,
        "catalog/industrial_cities.html",
        context
    )


def industrial_city_detail(request, slug):
    all_cities = load_industrial_cities()

    city = next(
        (
            item
            for item in all_cities
            if item["slug"] == slug
        ),
        None
    )

    if city is None:
        raise Http404("Industrial city not found")

    return render(
        request,
        "catalog/industrial_city_detail.html",
        {"city": city}
    )


def load_products():
    products_data = load_json("products.json")
    industries_data = load_json("industries.json")
    companies_data = load_json("companies.json")

    industry_lookup = {
        industry["slug"]: industry
        for industry in industries_data["industries"]
    }

    company_lookup = {
        company["slug"]: company
        for company in companies_data["companies"]
    }

    return [
        {
            **product,
            "industry": industry_lookup[product["industry_slug"]],
            "company": company_lookup[product["company_slug"]]
        }
        for product in products_data["products"]
    ]


def made_in_saudi(request):
    all_products = load_products()

    search_query = request.GET.get("q", "").strip()
    selected_industry = request.GET.get("industry", "").strip()
    selected_category = request.GET.get("category", "").strip()

    industry_options = sorted(
        {
            product["industry_slug"]: product["industry"]
            for product in all_products
        }.values(),
        key=lambda industry: industry["name"]
    )

    categories = sorted({
        product["category"]
        for product in all_products
    })

    filtered_products = all_products

    if search_query:
        query = search_query.casefold()

        filtered_products = [
            product
            for product in filtered_products
            if query in " ".join([
                product["name"],
                product["description"],
                product["category"],
                product["industry"]["name"],
                product["company"]["name"],
                product["production_location"],
            ]).casefold()
        ]

    if selected_industry:
        filtered_products = [
            product
            for product in filtered_products
            if product["industry_slug"] == selected_industry
        ]

    if selected_category:
        filtered_products = [
            product
            for product in filtered_products
            if product["category"] == selected_category
        ]

    context = {
        "products": filtered_products,
        "industry_options": industry_options,
        "categories": categories,
        "search_query": search_query,
        "selected_industry": selected_industry,
        "selected_category": selected_category,
        "total_products": len(all_products),
    }

    return render(
        request,
        "catalog/made_in_saudi.html",
        context
    )


def product_detail(request, slug):
    all_products = load_products()

    product = next(
        (
            item
            for item in all_products
            if item["slug"] == slug
        ),
        None
    )

    if product is None:
        raise Http404("Product not found")

    return render(
        request,
        "catalog/product_detail.html",
        {"product": product}
    )
