---
name: odoo-productivity
description: Functional knowledge of Odoo Productivity modules — Documents, Sign, Spreadsheets, Dashboards, Knowledge, Discuss, Calendar, WhatsApp, Phone/VoIP, and AI features. Use whenever the user asks about Odoo document management, digital signatures, spreadsheet analysis, team communication, knowledge base, or AI-powered automation.
---

# Odoo Productivity — Functional Knowledge

You are acting as a functional Odoo productivity consultant. Use this knowledge to guide, configure, troubleshoot, and explain Odoo Productivity modules.

## Module Overview

| Module | Purpose |
|---|---|
| Documents | Centralized file storage and management |
| Sign | Digital signature workflows |
| Spreadsheet | Business intelligence and data analysis |
| Dashboards | KPI and metrics visualization |
| Knowledge | Internal wiki and documentation |
| Discuss | Team messaging and collaboration |
| Calendar | Scheduling and calendar integrations |
| Appointments | Customer-facing booking |
| WhatsApp | WhatsApp Business messaging |
| Phone (VoIP) | Call management and VoIP integration |
| Data Cleaning | Deduplication and data quality |
| AI | AI-powered automation features |

---

## Documents

### Workspace Structure

- Documents → Workspaces (left sidebar) — like top-level folders
- Each workspace has: sub-folders, tags, access rights, linked model (e.g., link to HR for contracts)
- **Access control**: define who can view/edit per workspace

### File Operations

| Action | How |
|---|---|
| Upload | Drag & drop or Upload button |
| Create | New → Spreadsheet / PDF template / blank |
| Link | New → URL link (shortcut to external resource) |
| Split PDF | Open PDF → Split → define page ranges |
| Merge PDFs | Select multiple PDFs → Action → Merge |
| Request file | Documents → New → Request → sends email asking someone to upload |

### Email Alias

- Each workspace can have an email alias
- Emails sent to the alias → attachments auto-saved to that workspace

### Tags & Linked Records

- Tags: freely assigned metadata for filtering
- Linked records: associate a document to a specific Odoo record (e.g., link NDA to a contact)
- Linked model: auto-populate documents workspace from a model (e.g., all employee contracts appear in HR workspace)

### AI Digitization

- Upload a PDF invoice/bill → AI extracts: vendor, date, amount, reference → creates draft vendor bill
- Accounting → Vendors → Bills → Upload → Digitize (uses IAP credits)

### Archiving

- Archived files removed from main view but accessible via filter
- Configure deletion delay: auto-delete X days after archiving

---

## Sign

### Signature Request Workflow

**Prepare → Send → Sign → Complete**

1. Sign → Upload document (PDF)
2. Add signature fields: drag field types onto PDF pages
3. Set signatories: name, email, role, signing order
4. Send → signatories receive email with link
5. Each signer: opens link, fills fields, draws/types signature → submits
6. Certificate of Completion generated → all parties receive final signed PDF

### Field Types on Documents

| Field | Purpose |
|---|---|
| Signature | Draw, type, or upload signature image |
| Initial | Abbreviated signature for each page |
| Text | Free text input |
| Date | Auto-fills with signing date |
| Checkbox | Yes/No toggles |
| Selection | Dropdown choice |

### Templates

- Sign → Templates → New
- Upload base PDF + configure fields once → reuse for repeated document types (employment contracts, NDAs)
- Auto-fill fields from Odoo record data (e.g., pull employee name, salary from contract)

### Document Envelopes

- Send multiple documents to multiple signatories in one batch
- Sign → Envelopes → New → add documents → add signatories → define who signs what

### Security Features

| Feature | Description |
|---|---|
| Signatory hash | Unique cryptographic fingerprint per signer |
| Certificate of Completion | PDF audit trail with timestamps and IP addresses |
| SMS verification | Signer receives unique code by SMS to authenticate |
| Itsme® (EU) | Belgian/Dutch digital identity verification |
| Aadhaar eSign (India) | India government identity verification |
| Digital Certificates | Upload cryptographic signing certificate |

### Validity & Reminders

- Set document expiry date → link expires after date
- Automatic reminder emails to signers who haven't completed

---

## Spreadsheet

### Creating Spreadsheets

- Documents → New → Spreadsheet, OR
- From any pivot/graph view → Insert in Spreadsheet

### Live Odoo Data Integration

| Insert Type | How |
|---|---|
| List | Insert filtered record list → auto-updates when records change |
| Pivot | Cross-tab analysis from any Odoo model |
| Chart | Bar, line, pie from Odoo data |
| Financial data | Accounting figures (P&L, balance sheet) |

- Data stays **live** — changes in Odoo automatically reflect in the spreadsheet

### Pivot Tables

- Add dimensions (rows/columns) and measures
- Group by date hierarchy (year → quarter → month → week)
- **Calculated measures**: write custom formulas on top of pivot data
- **Show as**: % of total, % of row/column, running total

### Global Filters

Apply filters across all pivots/lists/charts in the spreadsheet:

| Filter type | Use case |
|---|---|
| Date | Filter all data by period |
| Relation (Many2one) | Filter by salesperson, project, department |
| Text | Filter by text match |
| Yes/No | Boolean filter |
| Numeric | Greater than / less than |

### Conditional Formatting

- Format cells based on rules: single color, color scale, icon sets, data bars
- Highlight cells exceeding budget, below target, etc.

### Convert to Dashboard

- File → Convert to Dashboard → the spreadsheet becomes a read-only dashboard accessible from the Dashboards app

### Templates

- Save any spreadsheet as a template → reuse for monthly reports, etc.

---

## Dashboards

- Dashboards → Build → drag and drop widgets
- Widget types: graph, pivot, metric (KPI number), spreadsheet conversion
- **My Dashboard**: personal dashboard visible on login home screen
- Share dashboards with teams or make public
- Each widget links to the live Odoo data it was built from — click to drill down

---

## Knowledge

### Structure

- Knowledge → Articles (left tree view) — hierarchical document tree
- Articles can be nested under parent articles
- **Workspace**: group related articles by topic (Engineering, HR, Sales Playbook, etc.)

### Writing Articles

- Full rich-text editor with `/` Powerbox commands
- Embed: images, files, links, videos, Odoo views (pivot, list), Kanban boards, templates
- **Article Properties**: custom metadata fields on articles

### Sharing

- **Internal**: visible to all employees
- **Shared**: send link to specific people (portal or external)
- **Article Items**: a structured list inside an article (like a mini-database)

### Linking to Records

- From any Odoo record's chatter → link a Knowledge article
- Search articles from within CRM, Project, Helpdesk without leaving the record

---

## Discuss

### Channels

- Discuss → Channels → create topic-based group channels (#general, #sales, #engineering)
- Public channels: anyone can join
- Private channels: invite only
- Each Odoo module's records have **Chatter** — record-level threaded discussion

### Messaging Features

- **@mentions**: notify specific users
- **Emoji reactions**: react to messages
- **Message pinning**: pin important messages in channel
- **Canned responses**: pre-written reply snippets for common answers — Discuss → Configuration → Canned Responses
- **Direct messages (DM)**: 1:1 or small group private conversations
- **Video/Audio calls**: built-in WebRTC calls from Discuss (configure ICE servers via Twilio for reliability)

### ICE Server Configuration (VoIP Calls)

- Settings → Technical → ICE Servers → add Twilio TURN credentials for stable video calls

---

## Calendar

### Views

- Day, Week, Month, Year views
- **My Events** vs all events toggle

### Integrations

- **Google Calendar**: Settings → General Settings → Google Calendar → authenticate → two-way sync
- **Outlook Calendar**: similar OAuth setup → bi-directional sync

### Attendees & Invitations

- Add internal users and external contacts as attendees
- Attendees receive email invitation with calendar event

---

## Appointments

- Create appointment types: duration, availability slots, assignee rules
- Share booking link → customer picks available slot → auto-creates Calendar event
- **Opportunity creation**: appointment type can auto-create a CRM opportunity on booking
- **Google Reserve**: listed in Google search results for direct booking

---

## WhatsApp

- Connect WhatsApp Business API account: Settings → Technical → WhatsApp
- Send messages from: Chatter of any record, Marketing campaigns
- **Templates**: pre-approved message templates required by WhatsApp API for outbound messaging
- **Automation**: trigger WhatsApp messages via automated actions (e.g., send confirmation when SO is confirmed)

---

## Phone / VoIP

### Providers

| Provider | Features |
|---|---|
| Axivox | Full PBX: voicemail, IVR, call queues, conference, dial plans, dynamic caller ID |
| DIDWW | SIP trunking |
| OnSIP | Cloud PBX |

### Setup (Axivox example)

1. Settings → VoIP → configure provider credentials
2. Assign VoIP extensions to Odoo users
3. Phone widget appears in bottom-left of Odoo interface

### Using Phone in Odoo

- Click phone number on any record → auto-dials via VoIP widget
- **Activity logging**: calls auto-log as activities on the record
- **Sales workflow**: CRM → call from opportunity → logs call result

---

## Data Cleaning

- Data Cleaning → Deduplication — finds records with similar names/emails/phones
- Select duplicates → Merge → choose master record → merged record retains all linked data
- **Field cleaning**: standardize formatting (capitalization, phone format, spaces)
- Bulk corrections across entire database

---

## AI Features

### Capabilities

| Feature | Where available |
|---|---|
| Text improvement | Any rich-text field → AI menu |
| Writing assistance | Draft emails, descriptions, responses |
| Voice transcription | Convert voice recordings to text |
| Document digitization | Upload PDF → AI extracts invoice/bill data |
| Email template generation | Auto-generate email templates |
| Live chat AI | Answer customer questions automatically |
| Document sorting | Auto-classify uploaded documents to correct workspace |
| Field intelligence | Suggest values for specific fields |

### Configuration

- Settings → Technical → Artificial Intelligence → add OpenAI or Odoo AI API key
- Configure: default AI model, allowed features per application
- **AI Agents**: configure automated workflow bots for specific tasks

---

## Key Configuration Checklist

| Setting | Where |
|---|---|
| Document workspaces & access | Documents → Configuration → Workspaces |
| Google Calendar sync | Settings → General Settings → Integrations |
| VoIP provider | Settings → VoIP |
| WhatsApp API connection | Settings → Technical → WhatsApp |
| Canned responses | Discuss → Configuration → Canned Responses |
| ICE servers (video calls) | Settings → Technical → ICE Servers |
| AI API key | Settings → Technical → AI |

---

## Common Troubleshooting

| Issue | Check |
|---|---|
| Spreadsheet data not updating | Check if data source filter changed; refresh data sources |
| Sign document link expired | Check validity date on signing request; resend |
| Google Calendar not syncing | Re-authenticate OAuth; check sync interval in settings |
| WhatsApp message failing | Template must be approved by Meta; check API credentials |
| VoIP calls dropping | Add TURN server credentials (Twilio ICE) to settings |
| Document not auto-filing from email | Check workspace email alias and mail server configuration |
| AI feature not available | Check IAP credits and AI API key configuration |
