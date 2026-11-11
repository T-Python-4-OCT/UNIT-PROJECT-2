from django.urls import reverse
from .data import PLACES, PROJECTS


def get_search_context(params):
    query = params.get('q', '').strip()[:100]
    category = params.get('type', 'all')

    if category not in ('all', 'places', 'projects'):
        category = 'all'

    results = []

    sources = [
        ('places', PLACES, 'أماكن الزيارة', 'main:place_detail'),
        ('projects', PROJECTS, 'مشاريع الدرعية', 'main:project_detail'),
    ]

    if query:
        search_term = query.casefold()

        for source_type, items, category_name, url_name in sources:
            if category not in ('all', source_type):
                continue

            for item in items:
                fields = [
                    item.get('title', ''),
                    item.get('subtitle', ''),
                    item.get('tag', ''),
                    item.get('category', ''),
                    item.get('description', ''),
                    item.get('summary', ''),
                ]

                searchable_text = ' '.join(
                    str(field) for field in fields
                ).casefold()

                if search_term in searchable_text:
                    results.append({
                        'category': category_name,
                        'title': item.get('title', ''),
                        'subtitle': item.get('subtitle', ''),
                        'description': (
                            item.get('description')
                            or item.get('summary', '')
                        ),
                        'image': item.get('image', ''),
                        'url': reverse(
                            url_name,
                            args=[item['slug']]
                        ),
                    })

    return {
        'query': query,
        'category': category,
        'results': results,
        'result_count': len(results),
    }
