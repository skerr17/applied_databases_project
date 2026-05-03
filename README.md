# Conference Management System

By Stephen Kerr

## Overview
A command-line Python application for managing a conference. It connects to both a **MySQL** relational database and a **Neo4j** graph database to provide a full suite of conference management features, from browsing sessions and attendees to exploring social connections and generating exportable reports.

Built as part of the Applied Databases module, [HDIP in Computing and Data Analytics](https://www.atu.ie/courses/higher-diploma-in-science-data-analytics) at ATU.

## Features
- Search speakers and sessions by name
- View attendees by company with full session details
- Add new attendees to the database
- Explore social connections between attendees via a Neo4j graph database
- View 2nd degree (friends of friends) connections
- View room availability and session capacity utilization
- Conference statistics dashboard combining both MySQL and Neo4j data
- Full conference agenda ordered by date
- Export any data view to a timestamped CSV file

## Technologies
- Python
- MySQL
- Neo4j
- Git, GitHub

## Project Structure
- `main.py` -> Main application entry point, runs the CLI menu loop
- `db_mysql.py` -> MySQL connection and all query functions
- `db_neo4j.py` -> Neo4j connection and all graph query functions
- `export.py` -> CSV export functionality with timestamped filenames
- `config.py` -> Database connection credentials for MySQL and Neo4j
- `requirements.txt` -> Required Python packages
- `innovation.pdf` -> Documentation of extra features and innovations
- `GitLink.pdf` -> Link to this GitHub repository
- `output/` -> Directory where all CSV exports are saved (auto-created)

## Getting Started

### Prerequisites
- Python 3.8+
- MySQL
- Neo4j

### Installation

1. Clone the repository
```bash
git clone <https://github.com/skerr17/applied_databases_project>
cd applied_databases_project
```

2. Install the required Python packages
```bash
pip install -r requirements.txt
```

3. Set up the MySQL database
```bash
mysql -u root -p < appdbproj.sql
```

4. Import `appdbprojNeo4j.json` into a Neo4j instance called `appdbprojNeo4j`

5. Create a `config.py` file with your database credentials
```python
# MySQL
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "your_password"
MYSQL_DATABASE = "appdbproj"

# Neo4j
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "your_password"
```
> ⚠️ `config.py` is not included in the repository for security reasons. Create it manually using the template above.

6. Run the application
```bash
python main.py
```

## Menu Options

| Option | Feature |
|---|---|
| 1 | View Speakers & Sessions — search by name or partial name |
| 2 | View Attendees by Company — enter a company ID |
| 3 | Add New Attendee — insert a new attendee into MySQL |
| 4 | View Connected Attendees — Neo4j connections + friends of friends |
| 5 | Add Attendee Connection — create a Neo4j CONNECTED_TO relationship |
| 6 | View Rooms — cached on first load |
| 7 | Conference Statistics Dashboard — key stats across both databases |
| 8 | View Conference Agenda — all sessions ordered by date |
| 9 | Session Capacity Utilization — registered vs capacity vs spots left |
| x | Exit Application |

## CSV Export
Most options offer the ability to export displayed data to CSV:
- Files are saved to the `output/` folder (auto-created if it doesn't exist)
- Filenames are timestamped to avoid overwriting e.g. `conference_agenda_2025-05-12_10-30-00.csv`

## Notes
- The rooms list (option 6) is cached on first load, rooms added to MySQL after that will not appear until the application is restarted
- `CONNECTED_TO` relationships in Neo4j are treated as bidirectional
- Any attendee in the Neo4j database is assumed to also exist in the MySQL database