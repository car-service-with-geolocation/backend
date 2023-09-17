GET /api/v1/core/geoip/my/
{
    "city": "Moscow",
    "continent_code": "EU",
    "continent_name": "Europe",
    "country_code": "RU",
    "country_name": "Russia",
    "dma_code": null,
    "is_in_european_union": false,
    "latitude": 55.7483,
    "longitude": 37.6171,
    "postal_code": "105094",
    "region": "MOW",
    "time_zone": "Europe/Moscow"
}


GET /api/v1/autoservice/service/
[
    {
        "company": {
            "name": "FIT-SERVICE",
            "description": "qwe123",
            "logo": null,
            "slug": "qwe123",
            "legal_address": "qwe123"
        },
        "city": "Москва",
        "address": "qwe",
        "geolocation": {
            "latitude": 52.0,
            "longitude": 48.0
        },
        "rating": 0
    }
]


GET /api/v1/autoservice/service/?latitude=53.2&longitude=46.3
[
    {
        "company": {
            "name": "FIT-SERVICE",
            "description": "qwe123",
            "logo": null,
            "slug": "qwe123",
            "legal_address": "qwe123"
        },
        "city": "Москва",
        "address": "rew",
        "geolocation": {
            "latitude": 53.0,
            "longitude": 47.0
        },
        "geo_size": 51.755790590632074,
        "rating": 0
    }
]
