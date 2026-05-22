"""SQL query functions for the SRPMS CLI prototype."""

from db import get_connection


def print_rows(headers, rows):
    """Print query results in a readable table with aligned columns."""
    if not rows:
        print("No records found.")
        return

    string_rows = [
        [str(value) if value is not None else "" for value in row]
        for row in rows
    ]

    column_widths = []
    for index, header in enumerate(headers):
        max_data_width = max(len(row[index]) for row in string_rows)
        column_widths.append(max(len(header), max_data_width))

    border = "+" + "+".join("-" * (width + 2) for width in column_widths) + "+"
    header_line = "|" + "|".join(
        f" {header:<{column_widths[index]}} "
        for index, header in enumerate(headers)
    ) + "|"

    print(border)
    print(header_line)
    print(border)

    for row in string_rows:
        row_line = "|" + "|".join(
            f" {value:<{column_widths[index]}} "
            for index, value in enumerate(row)
        ) + "|"
        print(row_line)

    print(border)


def list_customers():
    """Display all customers."""
    sql = """
        SELECT customer_id,
               first_name,
               last_name,
               phone,
               email,
               city,
               state
        FROM customer
        ORDER BY customer_id
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()

    print_rows(
        ["ID", "First Name", "Last Name", "Phone", "Email", "City", "State"],
        rows,
    )


def list_equipment_by_customer(customer_id):
    """Display equipment owned by a specific customer."""
    sql = """
        SELECT e.equipment_id,
               em.equipment_type,
               em.make,
               em.model,
               em.model_year,
               em.engine_spec,
               e.serial_number
        FROM equipment e
        JOIN equipment_model em
          ON e.equipment_model_id = em.equipment_model_id
        WHERE e.customer_id = :customer_id
        ORDER BY e.equipment_id
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, customer_id=customer_id)
            rows = cursor.fetchall()

    print_rows(
        ["Equipment ID", "Type", "Make", "Model", "Year", "Engine", "Serial"],
        rows,
    )


def list_compatible_parts_for_equipment(equipment_id):
    """Display compatible parts for a customer-owned equipment unit."""
    sql = """
        SELECT p.part_id,
               p.part_name,
               p.category,
               p.sku,
               p.unit_price,
               p.quantity_in_stock,
               pf.notes
        FROM equipment e
        JOIN equipment_model em
          ON e.equipment_model_id = em.equipment_model_id
        JOIN part_fitment pf
          ON em.equipment_model_id = pf.equipment_model_id
        JOIN part p
          ON pf.part_id = p.part_id
        WHERE e.equipment_id = :equipment_id
        ORDER BY p.category, p.part_name
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, equipment_id=equipment_id)
            rows = cursor.fetchall()

    print_rows(
        ["Part ID", "Part", "Category", "SKU", "Unit Price", "Stock", "Notes"],
        rows,
    )


def list_active_service_orders():
    """Display service orders that are not closed or declined."""
    sql = """
        SELECT so.service_order_id,
               c.first_name || ' ' || c.last_name AS customer_name,
               em.make || ' ' || em.model AS equipment_model,
               e.serial_number,
               so.date_opened,
               so.status,
               so.reported_issue
        FROM service_order so
        JOIN equipment e
          ON so.equipment_id = e.equipment_id
        JOIN equipment_model em
          ON e.equipment_model_id = em.equipment_model_id
        JOIN customer c
          ON e.customer_id = c.customer_id
        WHERE so.status NOT IN ('CLOSED', 'DECLINED')
        ORDER BY so.date_opened, so.service_order_id
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()

    print_rows(
        ["Order ID", "Customer", "Equipment", "Serial", "Opened", "Status", "Issue"],
        rows,
    )


def list_low_stock_parts(threshold=5):
    """Display parts with stock less than or equal to a threshold."""
    sql = """
        SELECT part_id,
               part_name,
               category,
               sku,
               quantity_in_stock
        FROM part
        WHERE quantity_in_stock <= :threshold
        ORDER BY quantity_in_stock, part_name
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, threshold=threshold)
            rows = cursor.fetchall()

    print_rows(
        ["Part ID", "Part", "Category", "SKU", "Stock"],
        rows,
    )


def update_service_order_status(service_order_id, new_status):
    """Update a service order status and commit the change."""
    sql = """
        UPDATE service_order
        SET status = :new_status
        WHERE service_order_id = :service_order_id
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                sql,
                new_status=new_status,
                service_order_id=service_order_id,
            )

            if cursor.rowcount == 0:
                print("No matching service order found.")
                return False

            connection.commit()

    print(f"Service order {service_order_id} updated to {new_status}.")
    return True


def list_compatible_parts_for_service_order(service_order_id):
    """Display compatible parts for the equipment attached to a service order."""
    sql = """
        SELECT p.part_id,
               p.part_name,
               p.category,
               p.sku,
               p.unit_price,
               p.quantity_in_stock,
               pf.notes
        FROM service_order so
        JOIN equipment e
          ON so.equipment_id = e.equipment_id
        JOIN equipment_model em
          ON e.equipment_model_id = em.equipment_model_id
        JOIN part_fitment pf
          ON em.equipment_model_id = pf.equipment_model_id
        JOIN part p
          ON pf.part_id = p.part_id
        WHERE so.service_order_id = :service_order_id
        ORDER BY p.category, p.part_name
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, service_order_id=service_order_id)
            rows = cursor.fetchall()

    print_rows(
        ["Part ID", "Part", "Category", "SKU", "Unit Price", "Stock", "Notes"],
        rows,
    )


def update_service_order_details(service_order_id, diagnosis_notes, labor_cost):
    """Update mechanic diagnosis notes and labor cost for a service order."""
    sql = """
        UPDATE service_order
        SET diagnosis_notes = :diagnosis_notes,
            labor_cost = :labor_cost
        WHERE service_order_id = :service_order_id
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                sql,
                service_order_id=service_order_id,
                diagnosis_notes=diagnosis_notes,
                labor_cost=labor_cost,
            )

            if cursor.rowcount == 0:
                print("No matching service order found.")
                return False

            connection.commit()

    print(f"Service order {service_order_id} diagnosis/labor updated.")
    return True


def show_service_order_estimate(service_order_id):
    """Display service order details, parts, labor, and estimated total."""
    order_sql = """
        SELECT so.service_order_id,
               c.first_name || ' ' || c.last_name AS customer_name,
               em.equipment_type,
               em.make,
               em.model,
               e.serial_number,
               so.status,
               so.reported_issue,
               so.diagnosis_notes,
               so.labor_cost
        FROM service_order so
        JOIN equipment e
          ON so.equipment_id = e.equipment_id
        JOIN equipment_model em
          ON e.equipment_model_id = em.equipment_model_id
        JOIN customer c
          ON e.customer_id = c.customer_id
        WHERE so.service_order_id = :service_order_id
    """

    parts_sql = """
        SELECT p.part_id,
               p.part_name,
               sop.quantity_used,
               sop.unit_price_at_use,
               sop.quantity_used * sop.unit_price_at_use AS line_total
        FROM service_order_part sop
        JOIN part p
          ON sop.part_id = p.part_id
        WHERE sop.service_order_id = :service_order_id
        ORDER BY p.part_name
    """

    total_sql = """
        SELECT so.labor_cost + NVL(SUM(sop.quantity_used * sop.unit_price_at_use), 0) AS subtotal,
               ROUND((so.labor_cost + NVL(SUM(sop.quantity_used * sop.unit_price_at_use), 0)) * 0.07, 2) AS tax,
               ROUND((so.labor_cost + NVL(SUM(sop.quantity_used * sop.unit_price_at_use), 0)) * 1.07, 2) AS estimated_total
        FROM service_order so
        LEFT JOIN service_order_part sop
          ON so.service_order_id = sop.service_order_id
        WHERE so.service_order_id = :service_order_id
        GROUP BY so.labor_cost
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(order_sql, service_order_id=service_order_id)
            order_rows = cursor.fetchall()

            cursor.execute(parts_sql, service_order_id=service_order_id)
            part_rows = cursor.fetchall()

            cursor.execute(total_sql, service_order_id=service_order_id)
            total_rows = cursor.fetchall()

    print("Service Order Estimate")
    print_rows(
        [
            "Order ID",
            "Customer",
            "Type",
            "Make",
            "Model",
            "Serial",
            "Status",
            "Reported Issue",
            "Diagnosis",
            "Labor",
        ],
        order_rows,
    )

    print()
    print("Estimated Parts")
    print_rows(
        ["Part ID", "Part", "Qty", "Unit Price", "Line Total"],
        part_rows,
    )

    print()
    print("Estimated Total")
    print_rows(
        ["Subtotal", "Tax", "Estimated Total"],
        total_rows,
    )


def show_invoice_for_service_order(service_order_id):
    """Display invoice summary, parts used, and labor cost for a service order."""
    invoice_sql = """
        SELECT i.invoice_id,
               i.service_order_id,
               i.invoice_date,
               i.due_date,
               i.subtotal,
               i.tax_amount,
               i.subtotal + i.tax_amount AS total,
               i.payment_status,
               i.payment_method,
               i.payment_date
        FROM invoice i
        WHERE i.service_order_id = :service_order_id
    """

    parts_sql = """
        SELECT p.part_id,
               p.part_name,
               sop.quantity_used,
               sop.unit_price_at_use,
               sop.quantity_used * sop.unit_price_at_use AS line_total
        FROM service_order_part sop
        JOIN part p
          ON sop.part_id = p.part_id
        WHERE sop.service_order_id = :service_order_id
        ORDER BY p.part_name
    """

    labor_sql = """
        SELECT labor_cost
        FROM service_order
        WHERE service_order_id = :service_order_id
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(invoice_sql, service_order_id=service_order_id)
            invoice_rows = cursor.fetchall()

            cursor.execute(parts_sql, service_order_id=service_order_id)
            part_rows = cursor.fetchall()

            cursor.execute(labor_sql, service_order_id=service_order_id)
            labor_row = cursor.fetchone()

    print("Invoice Summary")
    print_rows(
        [
            "Invoice ID",
            "Order ID",
            "Invoice Date",
            "Due Date",
            "Subtotal",
            "Tax",
            "Total",
            "Payment Status",
            "Method",
            "Payment Date",
        ],
        invoice_rows,
    )

    print()
    print("Parts Used")
    print_rows(
        ["Part ID", "Part", "Qty", "Unit Price", "Line Total"],
        part_rows,
    )

    if labor_row is not None:
        print()
        print(f"Labor Cost: {labor_row[0]}")


def list_invoices():
    """Display all invoices with customer, equipment, and payment details."""
    sql = """
        SELECT i.invoice_id,
               i.service_order_id,
               c.first_name || ' ' || c.last_name AS customer_name,
               em.make || ' ' || em.model AS equipment_model,
               i.invoice_date,
               i.due_date,
               i.subtotal,
               i.tax_amount,
               i.subtotal + i.tax_amount AS total,
               i.payment_status,
               i.payment_method,
               i.payment_date
        FROM invoice i
        JOIN service_order so
          ON i.service_order_id = so.service_order_id
        JOIN equipment e
          ON so.equipment_id = e.equipment_id
        JOIN equipment_model em
          ON e.equipment_model_id = em.equipment_model_id
        JOIN customer c
          ON e.customer_id = c.customer_id
        ORDER BY i.invoice_id
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()

    print_rows(
        [
            "Invoice ID",
            "Order ID",
            "Customer",
            "Equipment",
            "Invoice Date",
            "Due Date",
            "Subtotal",
            "Tax",
            "Total",
            "Status",
            "Method",
            "Payment Date",
        ],
        rows,
    )



def list_equipment_models():
    """Display available equipment models."""
    sql = """
        SELECT equipment_model_id,
               equipment_type,
               make,
               model,
               model_year,
               engine_spec
        FROM equipment_model
        ORDER BY make, model, model_year
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()

    print_rows(
        ["Model ID", "Type", "Make", "Model", "Year", "Engine"],
        rows,
    )


def create_customer(first_name, last_name, phone, email, street, city, state, zip_code):
    """Insert a new customer."""
    sql = """
        INSERT INTO customer (
            first_name,
            last_name,
            phone,
            email,
            street,
            city,
            state,
            zip_code
        ) VALUES (
            :first_name,
            :last_name,
            :phone,
            :email,
            :street,
            :city,
            :state,
            :zip_code
        )
        RETURNING customer_id INTO :new_customer_id
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            new_customer_id = cursor.var(int)
            cursor.execute(
                sql,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email,
                street=street,
                city=city,
                state=state,
                zip_code=zip_code,
                new_customer_id=new_customer_id,
            )
            connection.commit()

    created_id = new_customer_id.getvalue()[0]
    print(f"Customer created with ID {created_id}.")
    return created_id


def create_equipment(customer_id, equipment_model_id, serial_number):
    """Insert customer-owned equipment."""
    sql = """
        INSERT INTO equipment (
            customer_id,
            equipment_model_id,
            serial_number
        ) VALUES (
            :customer_id,
            :equipment_model_id,
            :serial_number
        )
        RETURNING equipment_id INTO :new_equipment_id
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            new_equipment_id = cursor.var(int)
            cursor.execute(
                sql,
                customer_id=customer_id,
                equipment_model_id=equipment_model_id,
                serial_number=serial_number,
                new_equipment_id=new_equipment_id,
            )
            connection.commit()

    created_id = new_equipment_id.getvalue()[0]
    print(f"Equipment created with ID {created_id}.")
    return created_id


def create_service_order(equipment_id, reported_issue, diagnosis_notes, labor_cost, status):
    """Insert a new service order."""
    sql = """
        INSERT INTO service_order (
            equipment_id,
            date_opened,
            reported_issue,
            diagnosis_notes,
            labor_cost,
            status
        ) VALUES (
            :equipment_id,
            SYSDATE,
            :reported_issue,
            :diagnosis_notes,
            :labor_cost,
            :status
        )
        RETURNING service_order_id INTO :new_service_order_id
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            new_service_order_id = cursor.var(int)
            cursor.execute(
                sql,
                equipment_id=equipment_id,
                reported_issue=reported_issue,
                diagnosis_notes=diagnosis_notes,
                labor_cost=labor_cost,
                status=status,
                new_service_order_id=new_service_order_id,
            )
            connection.commit()

    created_id = new_service_order_id.getvalue()[0]
    print(f"Service order created with ID {created_id}.")
    return created_id


def add_part_to_service_order(service_order_id, part_id, quantity_used):
    """Attach a part to a service order or increase quantity if already attached."""
    update_sql = """
        UPDATE service_order_part
        SET quantity_used = quantity_used + :quantity_used
        WHERE service_order_id = :service_order_id
          AND part_id = :part_id
    """

    insert_sql = """
        INSERT INTO service_order_part (
            service_order_id,
            part_id,
            quantity_used,
            unit_price_at_use
        )
        SELECT :service_order_id,
               part_id,
               :quantity_used,
               unit_price
        FROM part
        WHERE part_id = :part_id
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                update_sql,
                service_order_id=service_order_id,
                part_id=part_id,
                quantity_used=quantity_used,
            )

            if cursor.rowcount > 0:
                connection.commit()
                print(
                    f"Part {part_id} was already on service order {service_order_id}; "
                    f"quantity increased by {quantity_used}."
                )
                return True

            cursor.execute(
                insert_sql,
                service_order_id=service_order_id,
                part_id=part_id,
                quantity_used=quantity_used,
            )

            if cursor.rowcount == 0:
                print("No matching part found. No line item was created.")
                return False

            connection.commit()

    print(f"Part {part_id} added to service order {service_order_id}.")
    return True


def mark_invoice_paid(service_order_id, payment_method):
    """Mark the invoice as paid and close the related service order."""
    invoice_sql = """
        UPDATE invoice
        SET payment_status = 'PAID',
            payment_method = :payment_method,
            payment_date = SYSDATE
        WHERE service_order_id = :service_order_id
    """

    service_order_sql = """
        UPDATE service_order
        SET status = 'CLOSED',
            date_closed = SYSDATE
        WHERE service_order_id = :service_order_id
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                invoice_sql,
                service_order_id=service_order_id,
                payment_method=payment_method,
            )

            if cursor.rowcount == 0:
                print("No invoice found for that service order.")
                return False

            cursor.execute(service_order_sql, service_order_id=service_order_id)
            connection.commit()

    print(f"Invoice for service order {service_order_id} marked as paid.")
    print(f"Service order {service_order_id} marked as CLOSED.")
    return True