---
name: odoo-supply-chain
description: Functional knowledge of Odoo Supply Chain modules — Inventory, Manufacturing, Purchase, Barcode, Quality, Maintenance, and Repairs. Use whenever the user asks about Odoo stock management, warehouse operations, purchase orders, bills of materials, production orders, quality checks, or barcode scanning.
---

# Odoo Supply Chain — Functional Knowledge

You are acting as a functional Odoo supply chain consultant. Use this knowledge to guide, configure, troubleshoot, and explain Odoo supply chain modules.

## Module Overview

| Module | Purpose |
|---|---|
| Inventory | Stock management, warehousing, receipts, deliveries, transfers |
| Manufacturing | Production orders, BoM, work centers, shop floor |
| Purchase | Procurement, RFQs, purchase orders, vendor management |
| Barcode | Mobile barcode scanning for warehouse operations |
| Quality | Inspection points, quality checks, alerts |
| Maintenance | Equipment tracking and preventive maintenance |
| PLM | Engineering change orders and product versioning |
| Repairs | Repair order management |

---

## Inventory

### Product Configuration

| Field | Notes |
|---|---|
| Product Type | Storable (tracked), Consumable (not tracked), Service |
| Tracking | None / By Lot / By Serial Number |
| Unit of Measure | UoM and Purchase UoM can differ (auto-converted) |
| Routes | Determines replenishment/delivery logic |
| Packaging | Define case/pallet pack sizes |

- **Storable**: stock levels tracked; triggers replenishment rules
- **Consumable**: assumed always in stock; no stock valuation
- **Service**: no stock movement; used in BoM as a cost component

### Warehouses & Locations

- **Warehouse**: a physical location with its own stock, receipts journal, and delivery journal
- **Location types**: Vendor, Customer, Internal, Transit, Virtual (e.g., Production)
- Multi-warehouse: each warehouse has its own routes, operations, and replenishment rules
- **Inter-warehouse transfers**: configure routes between warehouses

### Warehouse Operations (Routes)

| Route | Steps |
|---|---|
| Receive in 1 step | Vendor → Stock (direct) |
| Receive in 2 steps | Vendor → Input → Stock (with QC opportunity) |
| Receive in 3 steps | Vendor → Input → Quality → Stock |
| Deliver in 1 step | Stock → Customer |
| Deliver in 2 steps | Stock → Output → Customer |
| Deliver in 3 steps | Stock → Pack → Output → Customer |

Configure per warehouse: Inventory → Configuration → Warehouses → Edit.

### Stock Moves & Transfers

- **Receipt**: incoming shipment from vendor
- **Delivery**: outgoing shipment to customer
- **Internal Transfer**: stock movement between internal locations
- **Backorder**: when quantity received/delivered is less than expected — Odoo asks to create a backorder for the remainder

### Inventory Adjustments

- Inventory → Operations → Physical Inventory
- Set counted quantities → Apply All — creates inventory adjustment journal entry
- **Cycle Counting**: set locations or product categories for periodic count schedules (rather than full inventory)

### Traceability

- **Lot**: batch tracking — one lot number = many units produced/received together
- **Serial Number**: unit-level tracking — one serial = one unit
- Traceability report: Inventory → Products → Lots/Serial Numbers → select → Traceability

### Reordering Rules

- Automatic reorder when stock hits minimum:
  - **Min/Max rules**: reorder when on-hand < min; order up to max
  - **Make to Order (MTO)**: trigger purchase/production immediately on sale
- Inventory → Operations → Replenishment → New Rule

### Stock Valuation

| Method | How it works |
|---|---|
| FIFO | First unit in is first unit valued out |
| Average Cost (AVCO) | Running weighted average |
| Standard Price | Fixed cost set manually on product |

- Configure per product category (Inventory → Configuration → Product Categories)
- **Landed Costs**: add freight, customs, duties to incoming shipment cost — Inventory → Operations → Landed Costs

### Putaway Rules

- Automatically route products to specific sub-locations on receipt
- Inventory → Configuration → Putaway Rules → define: location, product/category → destination sub-location

---

## Manufacturing

### Bill of Materials (BoM)

| Field | Notes |
|---|---|
| Product | The finished good being produced |
| BoM Type | Manufacture, Kit, Subcontracting |
| Components | Raw materials with quantities |
| Operations | Work center steps (if Work Orders enabled) |
| By-Products | Secondary outputs produced alongside the main product |

- **Kit BoM**: explodes on sale/delivery — no production order created; components shipped directly
- **Phantom BoM**: used for product bundling in manufacturing context

### Manufacturing Orders (MO)

**Workflow**: Draft → Confirmed → In Progress → Done

1. Manufacturing → Operations → Manufacturing Orders → New
2. Select product, BoM, quantity, scheduled date
3. Confirm → reserve components
4. Produce (enter actual qty, scrap if needed) → Mark as Done
5. Finished goods added to stock; components consumed

### Work Centers & Work Orders

- **Work Centers**: physical production stations (machines, assembly lines) with capacity, efficiency, cost per hour
- **Work Orders**: individual operations on a MO (e.g., cut, weld, paint) assigned to work centers
- **Shop Floor** (tablet view): workers log work orders in real time from the factory floor

### Subcontracting

- BoM Type = Subcontracting — assign a subcontractor vendor
- Send components to subcontractor → receive finished goods
- Odoo auto-creates the component delivery and finished goods receipt

### Scrap

- From any MO or transfer: Scrap button → select product, quantity, location
- Removes stock from inventory with a scrap move; can track scrap reason

---

## Purchase

### Procurement Workflow

**RFQ → Purchase Order → Receipt → Vendor Bill**

1. Purchase → Orders → Requests for Quotation → New
2. Set: Vendor, Currency, Delivery Date, Order lines
3. Send to Vendor (email) or confirm directly → becomes Purchase Order
4. When goods arrive: Receive Products button → validate receipt
5. Create Bill: on PO → Create Bill → matches PO lines

### Vendor Pricelists

- Purchase → Configuration → Vendor Pricelists (or set on product's Purchase tab)
- Define price breaks by quantity, validity period, currency per vendor

### Reordering & Procurement

- **Reordering rules**: when stock drops below minimum, Odoo auto-creates RFQs for the assigned vendor
- **Lead times**: set vendor lead time on product's Purchase tab → used in scheduled delivery date calculation
- Run replenishment: Inventory → Operations → Replenishment → Run Scheduler

### Purchase Agreements

- **Blanket Orders**: long-term agreement with vendor for recurring purchases at fixed price — create POs against the blanket
- **Call for Tenders**: send same RFQ to multiple vendors → compare responses → select winner

### Approval Workflows

- Purchase → Settings → Purchase Order Approval
- Set amount threshold — orders above threshold require manager approval before sending

### Analysis

- Purchase → Reporting → Purchase Analysis — pivot/graph by vendor, product, date

---

## Barcode

- Requires the Barcode module to be installed
- Access: dedicated Barcode app or scan from any stock operation
- **Operations from Barcode app**:
  - Receipts: scan vendor barcode → scan product → validate
  - Delivery: scan delivery order → scan products → validate
  - Internal Transfers: scan source location → products → destination
  - Inventory Count: scan location → count products
- **Product barcodes**: set on product form (EAN-13, QR, custom)
- **Location barcodes**: print from Inventory → Configuration → Locations

---

## Quality

### Quality Control Points (QCP)

- Trigger inspections at specific operation steps (receipt, delivery, manufacturing)
- Define: product/category, operation type, test type, team responsible
- Quality → Configuration → Quality Control Points

### Quality Check Types

| Type | Use case |
|---|---|
| Instructions | Show SOP text to operator |
| Pass / Fail | Binary check |
| Measure | Numeric value within tolerance (min/max) |
| Take a Photo | Visual documentation |
| Worksheet | Multi-step checklist |

### Workflow

1. Stock operation or MO triggers quality check automatically
2. Operator opens check, records result
3. Pass → process continues; Fail → creates Quality Alert
4. **Quality Alert**: Quality → Quality Alerts — assign to team, add corrective/preventive action, set deadline

---

## Maintenance

- **Equipment**: register machines, vehicles, tools — set responsible person, maintenance team, location
- **Preventive Maintenance**: schedule recurring maintenance requests (by date or by usage)
- **Corrective Maintenance**: log breakdown → create maintenance request → assign technician → mark done
- **Maintenance Requests**: Maintenance → Maintenance Requests — kanban by stage

---

## Key Configuration Checklist

| Setting | Where |
|---|---|
| Warehouse steps | Inventory → Configuration → Warehouses |
| Lot/serial tracking on product | Product form → Inventory tab |
| Valuation method | Inventory → Configuration → Product Categories |
| Reordering rules | Inventory → Operations → Replenishment |
| Purchase approval threshold | Purchase → Settings |
| Quality control points | Quality → Configuration → Control Points |
| Work centers | Manufacturing → Configuration → Work Centers |

---

## Common Troubleshooting

| Issue | Check |
|---|---|
| Product can't be received | Check if PO is in "Purchase Order" status (not RFQ) |
| Stock not updating after delivery | Delivery must be Validated, not just Saved |
| Negative stock | Enable negative stock in settings or check if product is consumable |
| BoM not found on MO | BoM must exist for the correct product variant and UoM |
| Reordering rule not triggering | Run Scheduler manually; check min qty vs current on-hand |
| Quality check not appearing | Verify QCP is set to the correct operation type and product |
