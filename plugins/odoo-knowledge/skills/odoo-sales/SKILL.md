---
name: odoo-sales
description: Functional knowledge of Odoo Sales modules — CRM, Sales, Point of Sale, Subscriptions, and Rental. Use whenever the user asks about Odoo leads, opportunities, quotations, sales orders, POS, pricing, discounts, commissions, or marketplace connectors.
---

# Odoo Sales — Functional Knowledge

You are acting as a functional Odoo sales consultant. Use this knowledge to guide, configure, troubleshoot, and explain Odoo Sales modules.

## Module Overview

| Module | Purpose |
|---|---|
| CRM | Lead and opportunity pipeline management |
| Sales | Quotation-to-invoice workflow and revenue management |
| Point of Sale | Retail and restaurant in-person sales |
| Subscriptions | Recurring revenue management |
| Rental | Physical and service rental orders |

---

## CRM

### Core Concepts

- **Lead**: an unqualified contact/inquiry (optional stage, can be disabled)
- **Opportunity**: a qualified sales opportunity with expected revenue and closing date
- **Pipeline**: kanban view of all opportunities organized by stage

### Pipeline Setup

- Stages: CRM → Configuration → Stages — create/reorder stages, assign to specific sales teams
- **Rotting leads**: flag opportunities inactive past X days — set in stage settings
- **Probability**: manual or predictive (AI-based) win probability per opportunity
- **Sales Teams**: group salespeople; each team can have its own pipeline and stages

### Lead Acquisition

| Source | Setup |
|---|---|
| Email alias | CRM → Configuration → Sales Teams → Email Alias |
| Web contact form | Website module — form auto-creates leads |
| Manual entry | CRM → New |
| Lead Mining | CRM → Leads → Lead Mining Requests (IAP credits) |

### Lead Assignment

- **Manual**: drag in kanban or edit salesperson field
- **Rule-based**: CRM → Configuration → Assignment Rules — assign by country, language, tag, source
- **Predictive lead scoring**: enable in Settings → CRM — AI assigns win probability; route based on score

### Opportunity Workflow

1. Create / Convert lead to opportunity
2. Set: Expected Revenue, Closing Date, Salesperson, Sales Team, Tags
3. Log activities, send emails from chatter
4. Create Quotation directly from opportunity (links SO to opportunity)
5. Mark Won / Lost — add lost reason when lost

### Performance Reporting

- **Pipeline Analysis**: CRM → Reporting → Pipeline — group by salesperson, team, stage, month
- **Win/Loss Report**: filter won/lost opportunities
- **Forecast**: expected revenue grouped by closing month
- **Cohort**: track conversion rates over time

### UTM Tracking

- Add `?utm_source=X&utm_medium=Y&utm_campaign=Z` to links
- Odoo auto-tags leads created from those links — visible in lead's Marketing tab

---

## Sales (Quotations & Orders)

### Quotation Workflow

**Draft Quotation → Sent → Sales Order → Invoiced**

1. Sales → Orders → Quotations → New
2. Set: Customer, Expiration Date, Pricelist, Payment Terms
3. Add order lines: product, quantity, price, discount
4. Optional products: add alternatives customer can choose
5. Send by email (quotation PDF attached)
6. Customer confirms → becomes Sales Order

### Quote Templates

- Sales → Configuration → Quotation Templates
- Pre-fill product lines, optional products, terms & conditions, expiration days
- Assign to individual salespeople as default template

### PDF Quote Builder

- Customize quote PDF layout: add cover page, product images, dynamic blocks, T&C section
- Sales → Configuration → Settings → Quotation Builder

### Online Confirmation

- Customer can: sign online (e-signature), pay online, or both — triggers SO confirmation automatically
- Configure: Sales → Settings → Quotation & Orders → Online Signature / Online Payment

### Invoicing Policies

| Policy | When invoice is created |
|---|---|
| Ordered quantities | Invoice full SO on order confirmation |
| Delivered quantities | Invoice after delivery (most common for goods) |
| Milestones | Invoice on project milestone completion |
| Time & Materials | Invoice based on logged timesheets |

Set per product (Invoicing tab) or as company default (Sales → Settings).

### Down Payments

- On a confirmed SO: Create Invoice → Down Payment
- Choose: fixed amount or percentage of order total
- Deducted from final invoice automatically

### Pricing & Pricelists

- Sales → Configuration → Settings → enable Pricelists
- **Pricelist types**: multiple prices per product, discounts, fixed price per segment
- Apply per customer, sales team, or manually on quotation
- **Foreign currency pricelists**: set prices in customer's currency

### Discounts & Promotions

- **Line discount**: enable in Sales → Settings → Discounts
- **Pricelists with discount**: show original price + discount % on quote
- **Promotion programs**: Sales → Catalog → Promotions — coupon codes, automatic discounts, loyalty points, eWallet, gift cards

### Margins

- Enable: Sales → Settings → Margins
- Shows margin % and amount per line and order total
- Based on product cost price

### Commissions

- Sales → Configuration → Sales Commissions
- Define commission plans per salesperson or team
- Auto-calculates based on invoiced amounts

### Marketplace Connectors

| Connector | Features |
|---|---|
| Amazon | Sync orders, FBA stock, lot/serial tracking |
| Shopee | Order import, stock sync |
| Lazada | Order import, status sync |
| Gelato | Print-on-demand fulfillment |

Configure: Sales → Configuration → Settings → Connectors section.

---

## Point of Sale (POS)

### Setup

1. Point of Sale → Configuration → Point of Sale → New or Configure existing
2. Set: Journal (cash/bank), allowed payment methods, receipt printer, fiscal position
3. **IoT integration**: connect receipt printer, barcode scanner, scales via IoT Box

### Opening a Session

- POS → Open → select POS → Open Session
- Enter opening cash balance → start selling

### POS Workflow

1. Search/scan product → add to order
2. Apply discount (if enabled)
3. Select payment method (cash, card, split)
4. Validate → print/email receipt

### Business Modes

| Mode | Use case |
|---|---|
| Standard (Shop) | Retail — product grid layout |
| Restaurant | Table management, floor plans, kitchen display |
| Self-ordering | Customer-facing kiosk for self-service |

### Payment Methods

- Cash, Bank (card), Customer Account (credit)
- **Payment terminals**: Adyen, Stripe, Ingenico, Mollie, DPO, Razorpay
- **Cash machines**: Cashdro, Cashmatic, Glory
- **QR code payment**: generate QR at checkout

### Invoicing from POS

- At payment screen → Invoice toggle → assign customer → generates official invoice linked to POS order

### Session Close

- Close Session → count cash → validate → session report generated (sales by product, payment method)

### Offline Mode

- POS works on local network without internet — transactions sync to server when connection restored

---

## Subscriptions

- Attach a Subscription Plan to a product (Sales → Configuration → Subscription Plans)
- Plans define: billing period (monthly/yearly), auto-renewal, pricing
- **eCommerce**: customers subscribe online — auto-creates recurring sales order
- **Renewal**: automatic (charged on renewal date) or manual (send renewal quote)
- **Upselling**: add products to active subscription mid-term
- **Closing**: record reason for churn — feeds analytics
- **Reporting**: MRR (Monthly Recurring Revenue), churn rate, subscription health

---

## Rental

- Mark a product as "Can be Rented" (Product → Sales tab)
- Set rental pricing: daily, weekly, monthly rates
- Rental Order: Sales → Orders → Rental Orders → New
- Set pickup and return dates, quantity, customer
- Security deposit: collected at pickup, returned on return
- Rental status tracks: Reserved → Picked up → Returned

---

## Key Configuration Checklist

| Setting | Where |
|---|---|
| Sales teams | Sales → Configuration → Sales Teams |
| Pricelists on/off | Sales → Settings → Pricing |
| Default invoicing policy | Sales → Settings → Invoicing |
| Quotation validity days | Sales → Settings → Quotations & Orders |
| Lead scoring | Sales → Settings → CRM |
| Commission plans | Sales → Configuration → Commissions |

---

## Common Troubleshooting

| Issue | Check |
|---|---|
| Can't invoice SO | Check invoicing policy; delivery must be validated first for "delivered qty" policy |
| Pricelist not applying | Check if pricelist is assigned to customer or manually on quotation |
| Lost opportunity not visible | Toggle "Lost" filter in CRM pipeline |
| POS won't open | Check if another session is already open; only one session per POS per user |
| Subscription not renewing | Check if auto-renewal is enabled on the subscription plan |
