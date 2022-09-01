{
    'name': 'Soporte Tecnico',
    'description': 'Crea Tickets y reporta los problemas tecnicos que tengas...',
    'category': 'Technical Support',
    'depends': ['base','mail'],
    'data': [
        'security/ca_support_security.xml',
        'security/ir.model.access.csv',
        'views/ca_support_issue_views.xml',
        'views/ca_support_menus.xml'
    ],
    'application': True
}