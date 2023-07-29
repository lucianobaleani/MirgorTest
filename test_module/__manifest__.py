{
    "name": "Test Module",
    "summary": """
        Module app for Test""",
    "author": "Luciano Baleani",
    "website": "",
    "license": "AGPL-3",
    "category": "Test",
    "version": "15.0.1.0.0",
    "application": False,
    "installable": True,
    "depends": ["sale_management", "product", "contacts"],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_menuitems.xml",
        "views/sale_channel_views.xml",
        "views/sale_quota_views.xml",
        "views/sale_order_inherited_views.xml",
    ],
}
