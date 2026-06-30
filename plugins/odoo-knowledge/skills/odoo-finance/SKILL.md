---
name: odoo-finance
description: Functional knowledge of Odoo Finance modules — Accounting, Invoicing, Expenses, Online Payments, and fiscal localizations. Use whenever the user asks about Odoo accounting, invoices, vendor bills, bank reconciliation, taxes, payments, or expense management.
---

# Odoo Finance — Functional Knowledge

You are acting as a functional Odoo finance consultant. Use this knowledge to guide, configure, troubleshoot, and explain Odoo Accounting & Finance features.

## Module Overview

| Module | Purpose |
|---|---|
| Accounting & Invoicing | Double-entry bookkeeping, AR/AP, bank reconciliation, financial reporting |
| Expenses | Employee expense claims and reimbursement |
| Online Payments | Payment gateway integrations for eCommerce and invoices |
| Fiscal Localizations | Country-specific tax and compliance configurations |

---

## Accounting & Invoicing

### Core Concepts

- **Double-entry bookkeeping**: every journal entry debits one account and credits another — always balanced
- **Accrual vs Cash basis**: accrual recognizes revenue/expense when earned/incurred; cash basis on actual payment
- **Chart of Accounts (CoA)**: the full list of accounts — Assets, Liabilities, Equity, Revenue, Expense
- **Journal**: groups of accounting entries by type (Sales, Purchase, Bank, Cash, Miscellaneous)
- **Fiscal Year**: configurable; year-end closing locks prior periods

### Customer Invoices

**Workflow**: Draft → Confirmed → Posted (journal entry created) → Paid

1. Create from: Accounting → Customers → Invoices → New
2. Key fields: Customer, Invoice Date, Payment Terms, Journal, Product lines
3. **Payment Terms**: control when payment is due (immediate, net 30, installments)
4. **Incoterms**: shipping terms for international invoices
5. **Delivery address**: can differ from invoice address
6. Confirm (Post) → sends to accounting; creates journal entry
7. Register Payment → matches against the invoice → marks as paid

**Credit Notes**: create from the invoice via Credit Note button — reverses the original entry

**Electronic Invoicing (EDI)**: configure per company; sends invoices in structured XML format (e-invoice standards vary by country)

**Deferred Revenue**: spread revenue recognition over time — configure on the product or invoice line

### Vendor Bills

**Workflow**: Draft → Confirmed → Posted → Paid

- Create manually or via document digitization (upload PDF → AI extracts fields)
- Match with Purchase Orders via the Bills smart button on POs
- **Fixed Assets**: link a vendor bill to create/update an asset record automatically
- **Deferred Expenses**: spread expense recognition over time

### Taxes

| Tax type | Use case |
|---|---|
| Sales tax | Applied on customer invoices |
| Purchase tax | Applied on vendor bills |
| Withholding tax | Deducted from payment (common in Indonesia, etc.) |
| Cash basis tax | Recognized on payment date, not invoice date |

- Configure: Accounting → Configuration → Taxes
- **Tax Groups**: group taxes for reporting (e.g., VAT group)
- **Fiscal Positions**: automatically remap taxes and accounts based on customer/vendor country or B2B/B2C status
- **AvaTax**: external tax engine integration for US automated sales tax

### Payments

**Outbound (paying vendors)**:
- Accounting → Vendors → Payments → New
- Or: open bill → Register Payment
- **Batch payments**: group multiple bills into one bank transfer

**Inbound (receiving from customers)**:
- Accounting → Customers → Payments
- Or: open invoice → Register Payment
- **SEPA Direct Debit**: automated collection from customer bank accounts (EU)

**Payment Methods**: manual, check, SEPA, electronic (per bank journal configuration)

### Bank Management

- **Bank Synchronization**: connect bank via Ponto (EU), Basiq (AU), or direct bank sync — auto-imports transactions
- **Manual import**: upload OFX/QIF/CSV bank statement
- **Bank Reconciliation**:
  1. Match bank transaction line ↔ accounting entry (invoice payment, bill payment)
  2. Create new journal entry for unmatched bank fees, interest
  3. Reconciliation models: auto-match rules to speed up the process
- **Foreign currency accounts**: transactions recorded in foreign currency; exchange difference calculated on reconciliation
- **Loans**: track loan disbursement and repayment schedule

### Financial Reporting

| Report | Purpose |
|---|---|
| Profit & Loss | Revenue vs Expenses |
| Balance Sheet | Assets, Liabilities, Equity snapshot |
| Cash Flow | Cash movements (indirect method) |
| Tax Report | VAT/tax return by period |
| Aged Receivable / Payable | Outstanding invoice aging |
| General Ledger | Full transaction detail by account |
| Intrastat | EU intra-community trade reporting |
| Audit Report | Detailed entry trail |

- Access: Accounting → Reporting
- **Lock date**: prevent editing entries before a certain date (period close)
- **Year-end closing**: run wizard to close income/expense accounts into retained earnings

### Analytic Accounting

- **Analytic Accounts**: cost centers / projects for expense allocation beyond the CoA
- **Analytic Plans**: organize analytic accounts hierarchically
- Assign on invoice/bill lines, expenses, timesheets
- Reports: Analytic P&L by plan/account

### Budgets

- Define budgets by analytic account + GL account
- Track actual vs budgeted amounts in real time
- Alerts when budget is exceeded

---

## Expenses

**Workflow**: Employee logs expense → Submits expense report → Manager approves → Accountant posts → Reimbursed

### Setup
- Expense Categories: Products configured as expense types (Meals, Travel, etc.) with default account
- Configure per-category: vendor bill vs. expense, cost limit, re-invoice to customer option

### Employee Flow
1. Expenses → New Expense → fill category, amount, date, description, attach receipt
2. Add to Expense Report (group multiple expenses) → Submit to Manager
3. Manager: Approve or Refuse
4. Accountant: Post Journal Entries → Register Payment (reimbursement)

### Company Cards
- Expenses paid with company credit card: mark "Company pays" — no reimbursement needed
- Reconcile card statement against logged expenses

### Reinvoicing
- Expenses can be linked to a sales order/project — automatically added to customer invoice as a billable line

### Analysis
- Expenses → Reporting → Expense Analysis — pivot/graph by employee, category, date, project

---

## Online Payments

Payment providers that integrate with Odoo invoices and eCommerce checkout:

| Provider | Region |
|---|---|
| Stripe | Global |
| PayPal | Global |
| Adyen | Global |
| Mollie | EU |
| Mercado Pago | LATAM |
| Razorpay | India |
| Flutterwave | Africa |
| DPO Pay | Africa |
| + 15 more | Various |

- Configure: Accounting → Configuration → Payment Providers
- Each provider has sandbox (test) and production modes
- Payment links can be sent on invoices — customer pays online; invoice auto-reconciles

---

## Fiscal Localizations

- Install via: Accounting → Configuration → Fiscal Localizations → Install Localization
- Sets up: CoA, taxes, tax reports, fiscal positions per country
- **Indonesia (ID)**: includes VAT (PPN 11%), PPh withholding taxes, e-faktur export
- After install, review and adjust CoA mapping to match your business structure
- Localizations are cumulative — you can have multiple if operating in multiple countries

---

## Key Configuration Checklist

| Setting | Where |
|---|---|
| Company fiscal data | Settings → Companies |
| Default journals | Accounting → Configuration → Journals |
| Payment terms | Accounting → Configuration → Payment Terms |
| Fiscal positions | Accounting → Configuration → Fiscal Positions |
| Bank accounts | Accounting → Configuration → Bank Accounts |
| Tax rounding | Accounting → Settings → Tax rounding method |
| Lock date | Accounting → Accounting → Lock Dates |

---

## Common Troubleshooting

| Issue | Check |
|---|---|
| Invoice not reconciling | Payment currency vs invoice currency mismatch |
| Wrong tax on invoice | Fiscal position not applied; check customer's country |
| Bank sync not working | Re-authenticate provider; check consent expiry |
| Exchange difference journal entry missing | Enable "Automatic Currency Rate" in settings |
| Invoice stuck in Draft | User may lack "Billing / Invoicing" access right |
