---
name: odoo-services
description: Functional knowledge of Odoo Services modules — Project, Timesheets, Planning, Field Service, and Helpdesk. Use whenever the user asks about Odoo project management, task tracking, timesheet logging, resource planning, field technician workflows, or customer support ticketing.
---

# Odoo Services — Functional Knowledge

You are acting as a functional Odoo services consultant. Use this knowledge to guide, configure, troubleshoot, and explain Odoo Services modules.

## Module Overview

| Module | Purpose |
|---|---|
| Project | Project and task management |
| Timesheets | Time tracking and billing rate management |
| Planning | Employee shift and resource scheduling |
| Field Service | On-site service task management |
| Helpdesk | Customer support ticket management |

---

## Project

### Project Setup

- Project → New Project
- Key settings per project:
  - **Visibility**: internal (employees only), invited users, all users (portal access for customers)
  - **Billable**: links to customer and invoicing method
  - **Stages**: customize kanban columns per project (or use shared stages)
  - **Timesheets**: enable logging on tasks
  - **Task Deadline**: show deadline field on task form

### Project Templates

- Project → Configuration → Project Templates
- Define: default stages, task templates, role assignments, automated task scheduling
- Create new project from template → all structure copied

### Project Dashboard (Smart Buttons)

Each project's top bar shows:
- Total tasks count (by stage/status)
- Milestones reached/total
- Profitability (revenue vs costs, if billing enabled)
- Budget (if budget module active)
- Hours logged vs allocated

### Project Updates

- Project → Update button → write status update (on track, at risk, off track)
- Auto-sends digest email to followers
- Keeps history of all project updates

### Milestones

- Project → Settings tab → enable Milestones
- Milestones: Project → Milestones tab → New Milestone → set date, title
- Tasks can be linked to a milestone → milestone is marked done when all linked tasks are done
- Used for invoicing trigger (billing on milestone)

---

## Tasks

### Task Creation Methods

| Method | How |
|---|---|
| Manual | Project → New Task |
| Email alias | Emails to project alias auto-create tasks |
| Website form | Submit form on website → creates task |
| From SO | Sales order with service product creates project/task automatically |
| From Helpdesk | Ticket can spawn a task |

### Task Fields

- **Stage**: current workflow step
- **Assignees**: multiple allowed
- **Deadline / Date**: start and end date
- **Tags**: categorization labels
- **Priority**: star (normal/urgent)
- **Time Spent**: total logged timesheets
- **Sub-tasks**: hierarchical breakdown
- **Blocked by**: dependency mapping (task can't start until blocker is done)

### Task Stages vs Status

- **Stage**: the kanban column — represents workflow step (To Do, In Progress, Done)
- **Status**: in-stage progress indicator (Normal, Blocked, Ready for Next Stage) — shown as colored dot
- Both are configurable per project

### Recurring Tasks

- Task form → Recurrence tab → set frequency (daily/weekly/monthly/yearly)
- When recurring task is done, a new copy is auto-created for the next period

### Sub-tasks

- Task → Sub-tasks tab → Add a sub-task
- Sub-tasks appear nested under parent
- Parent task completion can be gated on all sub-tasks being done (optional)

---

## Timesheets

### Access & Configuration

- Timesheets → Configuration → Settings
- **Who can log**: set if only assigned employees or all employees can log on tasks
- **Billing rates**: configure encoding (timesheet activity captures the billing rate at time of entry)

### Logging Methods

1. **Manual**: Timesheets → New → select employee, date, project, task, description, hours
2. **From Task**: open task → Timesheets tab → log directly
3. **Timer**: start timer on a task → stop when done → auto-fills duration
4. **From Helpdesk Ticket**: log time on tickets → syncs to project timesheets

### Timesheet Views

- **Daily**: grid showing hours per day per project
- **Weekly**: totals by week
- **My Timesheets**: personal log
- **All Timesheets**: manager view (all employees)

### Billing

- **Non-billable**: logged for cost tracking only
- **Billable (at cost)**: invoice at timesheet rate
- **Billable (at sales price)**: invoice at product sales price regardless of actual cost

### Leaderboard

- Timesheets → Reporting → Leaderboard — gamification showing top contributors
- Configure billing rate targets per employee

### Time-off Integration

- Approved time off auto-creates a "time off" timesheet entry so capacity is visible in project planning

---

## Planning

### Setup

- Planning → Configuration → Settings
- Define roles (matching employee job positions) as properties on shift templates

### Scheduling

1. Planning → Schedule → New Shift
2. Assign: Employee, Role, Project/Task (optional), Start/End date-time
3. **Open Shifts**: shifts not yet assigned to a specific employee — visible to relevant employees who can self-assign

### Shift Templates

- Save a shift configuration as a template for repeated use
- Planning → Configuration → Shift Templates

### Auto-Planning

- Select a date range → Plan button → Odoo auto-assigns open shifts to available employees based on role and working hours

### Shift Management

- Employees can be reassigned by dragging shifts in Gantt view
- Unassign: remove employee from shift (becomes open shift again)
- Publish shifts → employees receive notification

---

## Field Service

### Setup

- Install Field Service module
- Field Service → Configuration → Settings → enable worksheets, product tracking, time tracking

### Task Creation for Field Service

- From Sales Order: service product with "Create Task" policy → task created in Field Service project
- From Helpdesk Ticket: escalate to field service task
- Manually: Field Service → Tasks → New

### Task Workflow

**New → Scheduled → In Progress → Done → Invoiced**

1. Schedule task: assign technician, set date/time
2. Technician travels: map view shows itinerary with optimized route
3. On site: fill worksheet (checklist, notes, photos)
4. Log time spent (timer or manual)
5. Add products used (parts, materials) — deducted from warehouse
6. Mark task as Done → triggers invoicing if billing is enabled

### Worksheets

- Field Service → Configuration → Worksheet Templates
- Design custom worksheets: text fields, checkboxes, measurements, photo capture
- Assign template to task type or project

### Product Management

- Technicians can consume products from a configured warehouse
- Products logged on task → appear on customer invoice
- Track which warehouse products come from (useful for field van stock)

### Map / Itinerary

- Field Service → Map view — shows all scheduled tasks on a map
- Route optimization: plan technician's daily route by proximity

---

## Helpdesk

### Setup

- Helpdesk → Configuration → Helpdesk Teams → New
- Per team, configure:
  - **Ticket receiving channels**: Email, Website Form, Live Chat, API
  - **Assignment**: manual, randomly, by workload (balanced), by expertise
  - **SLA policies**: enable and configure
  - **Customer ratings**: enable satisfaction survey

### Ticket Channels

| Channel | How |
|---|---|
| Email | Incoming email to team alias → creates ticket automatically |
| Website Form | Customer submits form on Help Center page |
| Live Chat | Chat conversation escalated to ticket |
| Manual | Helpdesk → New Ticket |
| Phone | Agent creates ticket during call |

### Ticket Workflow

**New → In Progress → Pending (waiting on customer) → Solved → Closed**

- Stages are configurable per team
- **Merge tickets**: combine duplicates into one
- **Escalate**: move ticket to a different team

### Assignment

| Mode | How it works |
|---|---|
| Manual | Agent picks up ticket |
| Random | Auto-assigned round-robin |
| Balanced | Assigned to agent with fewest open tickets |
| Expertise | Matched to agent's tagged expertise |

### SLA (Service Level Agreements)

- Helpdesk → Configuration → SLA Policies
- Define: Ticket Priority + Stage → Target response time
- SLA status shows on ticket: met (green), failed (red), at risk (orange)
- SLA reporting: Helpdesk → Reporting → SLA Status Analysis

### Help Center (Self-Service)

- Connect Knowledge articles → customers find answers without creating tickets
- Connect Forum → community Q&A
- Connect eLearning courses → training resources

### Customer Ratings

- After ticket is solved, customer receives satisfaction survey (Great / OK / Bad)
- Ratings visible on ticket and in Reporting → Customer Ratings

### After-Sales Actions from Tickets

| Action | What it does |
|---|---|
| Refund | Creates credit note in Accounting |
| Coupon | Generates promo code for customer |
| Return | Creates return picking in Inventory |
| Repair | Creates repair order |
| Field Service | Spawns Field Service task |

---

## Cross-Module Integration

| Integration | How it works |
|---|---|
| Project ↔ Sales | SO with service products creates project/task; timesheet costs flow to invoice |
| Project ↔ Accounting | Analytic accounts link project costs to financial reporting |
| Helpdesk ↔ Field Service | Ticket can spawn a field service task for on-site resolution |
| Field Service ↔ Inventory | Products used in field tasks are consumed from warehouse stock |
| Timesheets ↔ Payroll | Logged hours can feed into payroll computation |
| Planning ↔ Timesheets | Planned shifts vs actual hours comparison |

---

## Key Configuration Checklist

| Setting | Where |
|---|---|
| Project billing type | Project → Settings tab |
| Task stages | Project → Configuration → Stages (or per-project) |
| Timesheet access | Timesheets → Configuration → Settings |
| Helpdesk team channels | Helpdesk → Configuration → Teams |
| SLA policies | Helpdesk → Configuration → SLA |
| Worksheet templates | Field Service → Configuration → Worksheets |
| Shift templates | Planning → Configuration → Shift Templates |

---

## Common Troubleshooting

| Issue | Check |
|---|---|
| Timesheets not showing on invoice | Check project billing type and invoicing method on SO |
| Task not created from SO | Product must have "Create Task" policy and be linked to a project |
| Helpdesk ticket not auto-created from email | Check team email alias and incoming mail server configuration |
| SLA not triggering | Ticket priority must match SLA policy priority and team assignment |
| Field service task not showing on map | Task must have a scheduled date and customer address |
| Planning shifts not visible to employee | Shifts must be published; check employee's role matches shift role |
