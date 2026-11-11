def google_location(latitude, longitude):
    coordinates = f'{latitude},{longitude}'

    return {
        'map_url': (
            'https://www.google.com/maps/search/'
            f'?api=1&query={coordinates}'
        ),
        'map_embed_url': (
            'https://maps.google.com/maps'
            f'?q={coordinates}&z=16&hl=ar&output=embed'
        ),
    }


PLACE_EXTRAS = {
    'zallal': {
        **google_location(24.7386, 46.5769),
        'official_url': 'https://www.diriyah.sa/ar/places-to-go/zallal',
        'location_description': 'وجهة الزلّال، الدرعية',
        'gallery': [
            {
                'image': 'zallal-gallery-01.webp',
                'caption': 'مدخل الزلّال',
            },
        ],
    },

    'bab-samhan': {
        **google_location(24.740175, 46.572227),
        'official_url': 'https://www.diriyah.sa/ar/plan-your-visit/hotels/bab-samhan-hotel',
        'booking_url': 'https://www.marriott.com/en-us/hotels/ruhlc-bab-samhan-a-luxury-collection-hotel-diriyah/overview/',
        'booking_label': 'حجز فندق باب سمحان',
        'location_description': 'فندق باب سمحان، الدرعية',
        'gallery': [
            {
                'image': 'bab-samhan-gallery-01.webp',
                'caption': 'بهو استقبال فندق باب سمحان',
            },
        ],
    },

    'at-turaif': {
        **google_location(24.733, 46.5751),
        'official_url': 'https://www.diriyah.sa/ar/places-to-go/at-turaif',
        'booking_url': 'https://tickets.bujairi.sa/ar/d/3552/diriyah-access',
        'booking_label': 'احجز تذاكر الدخول',
        'location_description': 'حي الطريف التاريخي، الدرعية',
        'gallery': [
            {
                'image': 'at-turaif-gallery-01.webp',
                'caption': 'قصور الطريف بين النخيل',
            },
            {
                'image': 'at-turaif-gallery-02.webp',
                'caption': 'إطلالة على مباني الطريف التاريخية',
            },
            {
                'image': 'at-turaif-gallery-03.webp',
                'caption': 'تفاصيل العمارة النجدية',
            },
            {
                'image': 'at-turaif-gallery-04.webp',
                'caption': 'الجدران الطينية التاريخية',
            },
        ],
    },

    'bujairi-terrace': {
        **google_location(24.7364, 46.5749),
        'official_url': 'https://www.diriyah.sa/ar/places-to-go/bujairi-terrace',
        'booking_url': 'https://tickets.bujairi.sa/ar/d/3552/diriyah-access',
        'booking_label': 'احجز تذاكر الدخول',
        'location_description': 'مطل البجيري، الدرعية',
        'gallery': [
            {
                'image': 'bujairi-terrace-gallery-01.webp',
                'caption': 'الممرات والساحات في مطل البجيري',
            },
            {
                'image': 'bujairi-terrace-gallery-02.webp',
                'caption': 'أجواء التسوق والممرات التراثية',
            },
        ],
    },

    'wadi-hanifah': {
        **google_location(24.7309, 46.579),
        'official_url': 'https://www.diriyah.sa/ar/things-to-do/sightseeing/wadi-hanifah',
        'location_description': 'وادي حنيفة بالقرب من الدرعية',
        'gallery': [],
    },
}
