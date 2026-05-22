# SRPMS - Service Repair & Parts Management System

SRPMS is an Oracle SQL and Python command-line prototype for managing service repair operations. The project models the workflow of a small repair business, including customers, equipment, service orders, compatible parts, invoices, payment status, and repair progress.

This project was developed for an Advanced Database Systems course to demonstrate relational database design, SQL implementation, constraints, triggers, and application-level interaction with an Oracle database.

## Features

- Manage customers and equipment records
- View equipment by customer
- Track active service orders
- Update service order status
- Add parts to service orders
- View compatible parts for specific equipment models
- Track low-stock parts
- Generate and view service order estimates
- View invoices by service order
- List all invoices
- Mark invoices as paid
- Automatically create invoices when service orders are ready for pickup
- Automatically reserve parts when approved service orders move into repair

## Technologies Used

- Python
- Oracle Database
- SQL / PL/SQL
- `oracledb` Python library
- Oracle SQL Developer
- Docker
- VS Code

## Database Overview

The database includes the following main entities:

- `CUSTOMER`
- `EQUIPMENT`
- `EQUIPMENT_MODEL`
- `SERVICE_ORDER`
- `PART`
- `SERVICE_ORDER_PART`
- `PART_FITMENT`
- `INVOICE`

The schema uses:

- Primary keys
- Foreign keys
- Unique constraints
- Check constraints
- Lookup indexes
- Oracle identity columns
- Triggers for workflow automation

## Workflow Modeled

The system supports a repair workflow similar to a real small-engine repair shop:

1. A customer brings in equipment.
2. A service order is created.
3. The mechanic records diagnosis notes and labor cost.
4. Compatible parts are reviewed and added to the service order.
5. The service order status is updated as the repair progresses.
6. When the repair is ready for pickup, an invoice is created.
7. The invoice can later be marked as paid.

Example service order statuses include:

- `DROPPED_OFF`
- `AWAITING_APPROVAL`
- `DECLINED`
- `WAITING_FOR_PARTS`
- `IN_REPAIR`
- `READY_FOR_PICKUP`
- `CLOSED`

## Project Structure

```text
srpms-service-repair-management-system/
├── app.py
├── db.py
├── queries.py
├── populate.py
├── config_example.py
├── schema.sql
├── requirements.txt
└── README.md
