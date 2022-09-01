{
    "name":"Actualizar Costos",
    "application": True,
    "depends": ["base","stock", "ca_costo_stock"],
    "data": [
        "security/ir.model.access.csv",
        "views/ca_costo_freight_views.xml",
        "views/ca_costo_nationalization_views.xml",
        "wizard/ca_costo_freight_compute_views.xml",
        "views/ca_costo_menus.xml"
    ]
}