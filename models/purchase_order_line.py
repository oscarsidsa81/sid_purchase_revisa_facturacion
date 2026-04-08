# -*- coding: utf-8 -*-
from collections import defaultdict
from html import escape

from odoo import _, models
from odoo.exceptions import UserError


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    def action_revisar_facturacion_regularizado(self):
        """Regulariza cantidades facturadas para líneas recibidas sin factura del proveedor."""
        if not self:
            return

        items_by_order = defaultdict(list)
        invalid_lines = self.browse()
        lines_to_update = self.browse()

        for line in self:
            is_valid = (
                (line.product_qty or 0.0) > 0.0
                and (line.qty_received or 0.0) > 0.0
                and bool(line.order_id.sid_regularizado)
                and (line.qty_to_invoice or 0.0) > (line.qty_invoiced or 0.0)
            )
            if not is_valid:
                invalid_lines |= line
                continue

            lines_to_update |= line
            items_by_order[line.order_id.id].append(
                {
                    "item": line.sequence or "-",
                    "description": line.name or "",
                    "qty_orig": line.qty_invoiced or 0.0,
                    "qty_new": line.qty_received or 0.0,
                    "comment": _("No se recibe factura por parte del proveedor"),
                }
            )

        if invalid_lines:
            invalid_names = ", ".join(invalid_lines.mapped("display_name")[:5])
            raise UserError(
                _(
                    "Revisa si el caso es correcto para aplicar esta acción; "
                    "debes marcar 'Regularizado sin Factura' en la compra y tener cantidades válidas.\n"
                    "Líneas no válidas (máx. 5): %s"
                )
                % invalid_names
            )

        for line in lines_to_update:
            line.write(
                {
                    "qty_invoiced": line.qty_received,
                    "qty_to_invoice": 0.0,
                }
            )

        orders = self.env["purchase.order"].browse(items_by_order.keys())
        for order in orders:
            items = items_by_order.get(order.id, [])
            body = (
                "<table border='3' style='background-color: #B4D2B2; font-weight:bold;"
                "text-align: center;border-color:#2B4289;'>"
                "<tr><th style='width: 30px;'>Item</th><th style='width: 200px;'>Descripción</th>"
                "<th>Qty <br> Orig</th><th>Qty <br> New</th><th style='width: 200px;'>Comentario</th></tr>"
            )
            for item in items:
                body += (
                    "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
                        item["item"],
                        escape(item["description"]),
                        item["qty_orig"],
                        item["qty_new"],
                        escape(item["comment"]),
                    )
                )
            body += "</table>"
            order.message_post(
                body=body,
                subject=_("Resumen modificación facturación"),
                subtype_xmlid="mail.mt_note",
            )