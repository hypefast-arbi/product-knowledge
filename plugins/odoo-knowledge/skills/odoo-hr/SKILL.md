---
name: odoo-hr
description: Functional knowledge of Odoo HR (Human Resources) modules — Employees, Attendances, Payroll, Time Off, Recruitment, Appraisals, Fleet, and related HR features. Use whenever the user asks about Odoo employee records, attendance tracking, payroll processing, leave management, recruitment pipeline, or performance appraisals.
---

# Odoo HR — Functional Knowledge

You are acting as a functional Odoo HR consultant. Use this knowledge to guide, configure, troubleshoot, and explain Odoo Human Resources modules.

## Module Overview

| Module | Purpose |
|---|---|
| Employees | Employee master data and lifecycle management |
| Attendances | Check-in/out tracking and overtime management |
| Time Off | Leave types, allocations, and approval workflows |
| Payroll | Salary computation, payslips, and pay runs |
| Recruitment | Job postings, applicant pipeline, and offers |
| Appraisals | Performance reviews and 360° feedback |
| Fleet | Company vehicle management |
| Frontdesk | Visitor management |
| Lunch | Employee meal ordering |

---

## Employees

### Employee Record Structure

| Tab | Key Fields |
|---|---|
| General | Job Position, Job Title, Department, Manager, Coach, Work Location |
| Work Information | Working Hours, Timezone, Work Email, Work Phone |
| Private Information | Citizenship, Home Address, Certificate Level, Private Email, Emergency Contact |
| HR Settings | Related User (portal/system access), Employee Type, Payroll |
| Contract | Current contract summary (salary, structure type) |
| Resume | Skills, Work Experience, Education (CV tab) |

- **Job Position vs Job Title**: Position is a formal role (headcount tracked); Title is the display name on business card
- **Manager**: sets org chart hierarchy; affects approval workflows for time off, expenses
- **Coach**: mentoring relationship — different from manager
- **Work Location**: Home / Office / Other — used for attendance and hybrid work tracking

### Employee Lifecycle

**Onboarding**:
- Employees → Configuration → Onboarding Plans
- Create structured plans with steps: send contract, set up equipment, intro meeting, etc.
- Assign plan to new employee → tracks completion of each step

**Offboarding**:
- Similar plan structure for exit process: collect equipment, access removal, exit interview

### Departments

- Employees → Configuration → Departments
- View modes: Kanban (org chart), List, Hierarchy
- Each department can have a manager and parent department

### Skills

- Skill types → Skill → Skill Levels (e.g., Beginner, Expert)
- Add to employee Resume tab → used in recruitment matching and appraisals
- **Certifications**: track professional certifications with expiry dates and renewal alerts

### Equipment Assignment

- Link company equipment (laptops, phones) to individual employees or departments
- Tracked in Maintenance module → visible on employee form

---

## Attendances

### Check-in / Check-out Methods

| Method | Setup |
|---|---|
| Manual (web) | Employee logs in to Attendances app and clicks Check In |
| Kiosk mode | Tablet at office entrance — employees scan badge or enter PIN |
| RFID token | IoT Box + RFID reader at kiosk |
| Badge scan | Barcode badge at kiosk |

### Kiosk Configuration
- Attendances → Configuration → Settings → Kiosk Mode
- Assign PIN codes or badge IDs to employees

### Overtime Management
- Attendances → Configuration → Settings → enable Overtime
- Set working schedule expected hours vs actual check-in/out
- Overtime dashboard: managers see pending overtime to approve or refuse
- Approved overtime can be converted to time-off credits (extra days off)

### Attendance Logs
- Attendances → Attendances — full log of all check-in/check-out records
- Filter/group by employee, department, date
- Edit to correct errors (manager/HR only)

### Reporting
- Attendances → Reporting → Attendance Analysis
- Track hours worked, overtime, attendance rate per employee

---

## Time Off

### Time Off Types

Configure: Time Off → Configuration → Activity Types

| Setting | Options |
|---|---|
| Leave Validation | No validation / By Time Off Officer / By Employee's Manager |
| Allocation | Requires allocation, no allocation needed, fixed by HR |
| Carry over | None / unlimited / up to N days |
| Negative balance | Allow or prevent going negative |

### Public Holidays
- Time Off → Configuration → Public Holidays
- Set by country/state — auto-blocks those days from leave count

### Allocation

- **Manual allocation**: HR creates allocation for employee (Time Off → Managers → Allocation Requests → New)
- **Accrual plans**: automatic accumulation — e.g., 1.5 days/month accrued progressively
  - Time Off → Configuration → Accrual Plans → define milestone rules
  - Assign accrual plan to allocation

### Employee Flow
1. Time Off (app) → New Time Off Request → select type, dates
2. Submitted → Manager / HR approves or refuses
3. Approved → deducted from allocation balance

### Manager / HR View
- Time Off → Managers → Time Off → see all requests, filter by department
- Time Off → Reporting → by Employee, Analysis

---

## Payroll

### Setup Prerequisites
1. Working Schedules: Employees → Configuration → Working Schedules
2. Salary Structures: Payroll → Configuration → Salary Structures (defines computation rules)
3. Salary Structure Types: groups structures (e.g., Employee, Worker)
4. Pay Schedules: monthly, bi-weekly, etc.

### Contracts

- Every employee needs an active contract to be included in payroll
- Employees → Contracts → New
- Fields: Contract Date, Salary (basic wage), Structure Type, HR Responsible
- Contract status: New → Running → Expired / Cancelled

### Work Entries

- Work entries are the daily records of attendance, time off, overtime, etc.
- They are the source data for payslip computation
- Payroll → Work Entries → validate entries for the pay period before generating payslips
- **Conflict resolution**: overlapping entries (e.g., attendance + sick leave) must be resolved

### Payslip Generation

1. Payroll → Payslips → Payslip Batches → Generate Payslips
2. Select period → system generates one draft payslip per employee
3. Review each payslip: salary lines computed by structure rules
4. Confirm batch → payslips posted → accounting journal entries created
5. Register payment → bank transfer or check

### Salary Computation

- Structure rules define how each salary component is calculated (Python expressions or fixed values)
- Common components: Basic Salary, Transport Allowance, BPJS (Indonesia), Tax (PPh 21), Net Salary
- **Localizations**: country-specific structures for Indonesia, Belgium, Australia, India, Mexico, etc.

### Commissions

- Link payroll to sales performance
- Payroll → Configuration → Commission Plans → define target and rates
- Commission payslip line auto-populates based on invoiced sales

### Analysis

- Payroll → Reporting → Payslip Analysis — pivot by employee, structure type, period
- Headcount Report: staffing levels over time

---

## Recruitment

### Job Positions

- Recruitment → Configuration → Job Positions (or Employees → Job Positions)
- Set: Department, Expected New Employees (headcount), Responsible Recruiter
- Publish job on Website → opens careers page listing

### Recruitment Pipeline

Stages (configurable): New → Qualified → First Interview → Second Interview → Contract Proposed → Contract Signed

- Drag applicants between stages in kanban view
- Each stage can have: fold, email template sent automatically on stage change, probability

### Applicant Sources

- Job applications come from: website form, LinkedIn, email alias, manual entry
- **UTM tracking**: tag application source via URL parameters

### Interview Process
- Schedule interviews: applicant form → Plan Interview button → creates Calendar event
- Send interview invitations from applicant chatter

### Offer & Hire
- Create Offer from applicant → generates contract draft
- Set salary, start date, contract type
- Accept Offer → creates Employee record automatically

### Referral Program
- Employees → Referrals → employees share job links
- When referred applicant is hired: employee earns points → redeem rewards
- HR configures reward catalog

### Reporting
- Recruitment → Reporting → Recruitment Analysis — source, pipeline stage, time-to-hire
- Team Performance: compare recruiters

---

## Appraisals

### Setup
- Appraisals → Configuration → Settings
- Enable: 360 feedback, skill evolution tracking
- **Appraisal Plans**: schedule automatic appraisals (e.g., 6 months after hire, then annually)

### Appraisal Workflow
1. Auto-created by plan OR HR creates manually: Appraisals → New
2. Employee completes **self-assessment** (online form)
3. Manager (and others in 360°) complete their feedback
4. Manager conducts appraisal meeting → fills final appraisal form
5. Appraisal confirmed → skills updated, next appraisal scheduled

### Templates
- Appraisals → Configuration → Appraisal Templates
- Define questions, skill sections, rating scales

### Skills Evolution
- Appraisals → Reporting → Skills Evolution — track how employee skill levels change over appraisal cycles

### Analysis
- Appraisals → Reporting → Appraisal Analysis — filter by status (done, in progress, cancelled)

---

## Fleet

### Vehicle Setup
- Fleet → Vehicles → New
- Fields: Brand/Model, License Plate, Driver (linked employee), Acquisition Date, Fuel Type
- **Manufacturers & Models**: Fleet → Configuration → Manufacturers and Models — set CO2 emissions, fuel type defaults

### Services & Maintenance
- Log service records: oil change, tire rotation, inspections — with date, vendor, cost
- Set recurring service alerts by odometer or date

### Accident Tracking
- Fleet → Vehicles → Accidents — document incidents with date, description, cost

### Cost Analysis
- Fleet → Reporting → Fleet Analysis — total cost per vehicle, per driver
- **Depreciation Report**: calculates vehicle depreciation over time

---

## Key Configuration Checklist

| Setting | Where |
|---|---|
| Working schedules | Employees → Configuration → Working Schedules |
| Time off types | Time Off → Configuration → Activity Types |
| Accrual plans | Time Off → Configuration → Accrual Plans |
| Salary structures | Payroll → Configuration → Salary Structures |
| Recruitment stages | Recruitment → Configuration → Stages |
| Appraisal plans | Appraisals → Configuration → Settings |
| Kiosk mode | Attendances → Configuration → Settings |

---

## Common Troubleshooting

| Issue | Check |
|---|---|
| Employee missing from payroll batch | Check if employee has an active contract for the period |
| Time off not deducting from balance | Check allocation exists and is approved |
| Attendance not showing overtime | Working schedule must be set; overtime feature enabled |
| Appraisal not auto-creating | Check appraisal plan is assigned to employee's contract/department |
| Applicant not converting to employee | "Create Employee" button appears only after stage = Contract Signed |
| Payslip computation wrong | Review salary structure rules; check work entries for the period |
