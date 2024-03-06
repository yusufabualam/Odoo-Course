{
    'name': "HMS App",
    'summary': """ """,
    'author': "Yusuf Abu Alam",
    'category': 'Productivity',
    'version': '17.0.0.1.0',
    'depends': ['base',
                ],
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/base_menus.xml',
        'views/patient.xml',
        'views/department.xml',
        'views/doctor.xml',
    ],
}