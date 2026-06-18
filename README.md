<div align="center">
  <img src="docs/images/caselink-logo.png" alt="CaseLink logo" width="140">
  <h1>CaseLink</h1>
  <h3>Investigation Link Analysis &amp; Intelligence Platform</h3>
  <p><strong>Connecting Evidence. Accelerating Investigations.</strong></p>
  <p><sub>A clean investigation link analysis platform for managing cases, correlating shared evidence, visualizing hidden networks, searching records, exporting case data, and generating reports for cybercrime, financial fraud, vehicle, identity, property, witness, and organized crime investigations.</sub></p>
</div>

## Overview

Investigators across multiple domains receive numerous case reports containing scattered evidence such as phone numbers, bank accounts, email addresses, names, license plates, and physical items.

Identifying hidden relationships between these cases manually is time-consuming and increases the risk of missing organized patterns.

CaseLink is a general-purpose investigation intelligence platform that helps investigators create and manage cases, add evidence entities, detect direct and indirect relationships, visualize case networks, search across records, export case data, and generate case reports.

## Architecture / Workflow

```text
Investigation Registration
        |
        v
Evidence Collection
        |
        v
Entity Correlation Engine
        |
        v
Link Detection
        |
        v
Evidence Network Visualization
        |
        v
Investigation Insights
        |
        v
PDF Report Generation
```

## Features

- Creates, edits, filters, exports, and deletes investigation records.
- Correlates shared evidence across investigations.
- Detects direct and indirect relationships between cases.
- Identifies repeat evidence appearing in multiple investigations.
- Provides dashboard insights, work queues, and recent activity.
- Visualizes evidence networks using interactive graphs.
- Produces professional PDF investigation reports.
- Provides investigation-wide search capabilities.
- Supports note management and quick copy/search actions for evidence.

## Technology Stack

- **Backend**: Flask, SQLAlchemy
- **Database**: SQLite
- **Graph Analysis**: NetworkX
- **Visualization**: PyVis
- **Reporting**: ReportLab
- **Frontend**: HTML, CSS, JavaScript
- **UI Components**: Bootstrap 5.3, Lucide Icons
- **Typography**: Inter Font

## User Interface

CaseLink features a clean, simple investigation dashboard built for fast police demos and daily analyst use:

### Dashboard Metrics
- **Total Investigations**: Overview of all active and closed cases
- **Active Investigations**: In-progress case count
- **Unique Evidence Records**: Total distinct evidence entities tracked
- **Linked Investigation Networks**: Number of connected investigation clusters
- **Repeat Evidence Indicators**: Entities appearing across multiple investigations
- **Investigation Insights**: AI-generated findings from correlation analysis

### Key Features
- **Global Evidence Search**: Find cases and entities across the entire system
- **Advanced Case Register**: Filter by keyword, status, evidence type, and sort order
- **CSV Export**: Export filtered case lists for review or briefing
- **Investigation Metrics**: Dashboard with actionable statistics and work queues
- **Network Visualization**: Interactive graph showing evidence relationships
- **Case Management**: Create, update, delete, and track investigations
- **Evidence Correlation**: Automated detection of shared identifiers
- **Report Generation**: Export case-ready findings in professional PDF format
- **Clean UI**: Simple responsive layout with Lucide icons and readable cards

### Supported Evidence Types
- **Cyber Fraud**: Phone, UPI, Bank Account, Email, IP Address
- **Vehicle/Property**: License Plate, VIN, Address
- **Identity**: Aadhaar, Passport, Name, Alias
- **Physical Evidence**: Weapon, Device, Document, Serial Number
- **Other**: Witnesses

### Investigation Workflow
1. **Create Investigation** - Register a new case with basic details
2. **Add Digital Evidence** - Input phone numbers, identifiers, addresses, and more
3. **Correlate Evidence** - CaseLink automatically matches shared identifiers
4. **Detect Relationships** - Review repeat evidence and linked investigations
5. **Visualize Networks** - Explore evidence connections in an interactive graph
6. **Generate Reports** - Export findings with network diagrams and analysis

## Example Investigation

```text
CASE-001
Phone: +91-88220-44119
UPI: refunddesk@upi
Bank: ACCT-DEMO-3921

CASE-002
Phone: +91-88220-44119
IP: 103.88.44.21

CASE-003
UPI: loanverify@upi
Bank: ACCT-DEMO-3921
Vehicle Plate: MH-12-DE-9090

CASE-004
Vehicle Plate: MH-12-DE-9090
Alias: Raka
```

CaseLink detects the relationship pattern:

```text
CASE-001
        |
     Phone
        |
CASE-002
        |
       IP
        |
CASE-003
        |
 Vehicle Plate
        |
CASE-004
```

This helps investigators uncover hidden relationships across complaints that may otherwise appear unrelated during manual review.

## Screenshots

### Dashboard

![Dashboard](docs/images/dashboard.png)

### Evidence Network Visualization

![Evidence Network Visualization](docs/images/network.png)

### Investigation Workflow

![Investigation Workflow](docs/images/workflow.png)

## Setup

### Windows

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python demo_police_cases.py
python run.py
```

### macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 demo_police_cases.py
python run.py
```

Open:

```text
http://127.0.0.1:5000
```

Useful demo pages:

```text
http://127.0.0.1:5000/cases
http://127.0.0.1:5000/network
http://127.0.0.1:5000/search
```

## Police Demo Data

The demo file `demo_police_cases.py` loads connected cases from `CASE-001` to `CASE-010`.

It covers cyber fraud, loan fraud, marketplace fraud, vehicle theft, property fraud, identity misuse, weapon/extortion evidence, document forgery, witness information, and organized crime coordination.

It also includes all supported evidence types: phone, UPI, bank account, email, IP address, license plate, VIN, address, Aadhaar, passport, suspect name, alias, weapon, mobile device, document, serial number, and witness.

You can rerun the demo script before a presentation:

```bash
python3 demo_police_cases.py
python3 run.py
```

The script refreshes only demo cases `CASE-001` to `CASE-010`.

## Notes

The local database file is created at `instance/linksutra.sqlite3`. The police demo script provides connected investigation records for evaluation, demonstration, and testing.
