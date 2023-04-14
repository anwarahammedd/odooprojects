{
    'name': 'real estate',
    'description': '',
    'depends': ['base','contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/real_estate.xml',
        'views/estate_property.xml',
        'views/estate_property_tags.xml',
        'views/estate_offer.xml',
        'views/property_types.xml',
        'views/estate_inheritance.xml'

    ],
    'installable': True,

}
