# -*- coding: utf-8 -*-
from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    sid_regularizado = fields.Boolean(
        string="Regularizado sin Factura",
        default=False,
        help=(
            "Regularizado sin factura. Se utiliza cuando el proveedor no envía una factura "
            "para completar el pedido. Permite ejecutar la revisión de facturación en líneas de compra."
        ),
    )