# sid_purchase_revisa_facturacion

Módulo Odoo para gestionar casos de compra **regularizada sin factura** mediante una acción en líneas de pedido que ajusta cantidades facturadas y deja trazabilidad en el chatter.

---

## 📌 Objetivo

Este módulo agrega una funcionalidad específica para escenarios donde:

- el proveedor **no envía factura**,
- la compra ya tiene cantidades recibidas,
- y se requiere regularizar la facturación de líneas pendientes.

La acción **Revisar Facturación** permite actualizar automáticamente:

- `qty_invoiced = qty_received`
- `qty_to_invoice = 0`

y publicar un resumen de los cambios en el pedido de compra.

---

## ⚙️ Dependencias

- `sid_purchase_core`
- Dependencias transitivas de compra/mail incluidas por módulos base del proyecto.

---

## 📁 Estructura del módulo

```text
sid_purchase_revisa_facturacion/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── purchase_order.py
│   └── purchase_order_line.py
└── views/
    └── purchase_order_review_invoicing.xml