"""Populate SRPMS with demo data."""

import oracledb

from db import get_connection


CUSTOMERS = [
    {
        "first_name": "Mark",
        "last_name": "Johnson",
        "phone": "260-555-0142",
        "email": "mark.johnson@example.com",
        "street": "1148 Maple Ridge Dr",
        "city": "Fort Wayne",
        "state": "IN",
        "zip_code": "46804",
    },
    {
        "first_name": "Elena",
        "last_name": "Ramirez",
        "phone": "260-555-0188",
        "email": "elena.ramirez@example.com",
        "street": "7832 Oak Hollow Ln",
        "city": "Fort Wayne",
        "state": "IN",
        "zip_code": "46825",
    },
    {
        "first_name": "Brian",
        "last_name": "Miller",
        "phone": "260-555-0117",
        "email": "brian.miller@example.com",
        "street": "4021 Auburn Rd",
        "city": "Fort Wayne",
        "state": "IN",
        "zip_code": "46806",
    },
    {
        "first_name": "Nina",
        "last_name": "Patel",
        "phone": "260-555-0164",
        "email": "nina.patel@example.com",
        "street": "9910 Coldwater Rd",
        "city": "Fort Wayne",
        "state": "IN",
        "zip_code": "46845",
    },
    {
        "first_name": "Carlos",
        "last_name": "Mendoza",
        "phone": "260-555-0199",
        "email": "carlos.mendoza@example.com",
        "street": "2250 Fairfield Ave",
        "city": "Fort Wayne",
        "state": "IN",
        "zip_code": "46807",
    },
    {
        "first_name": "Amy",
        "last_name": "Wilson",
        "phone": "260-555-0135",
        "email": "amy.wilson@example.com",
        "street": "6709 Lima Rd",
        "city": "Fort Wayne",
        "state": "IN",
        "zip_code": "46818",
    },
    {
        "first_name": "George",
        "last_name": "Harris",
        "phone": "260-555-0108",
        "email": "george.harris@example.com",
        "street": "3105 Stellhorn Rd",
        "city": "Fort Wayne",
        "state": "IN",
        "zip_code": "46815",
    },
    {
        "first_name": "Linda",
        "last_name": "Brooks",
        "phone": "260-555-0124",
        "email": "linda.brooks@example.com",
        "street": "1402 Illinois Rd",
        "city": "Fort Wayne",
        "state": "IN",
        "zip_code": "46804",
    },
    {
        "first_name": "Samuel",
        "last_name": "Reed",
        "phone": "260-555-0173",
        "email": "samuel.reed@example.com",
        "street": "5521 Maplecrest Rd",
        "city": "Fort Wayne",
        "state": "IN",
        "zip_code": "46835",
    },
    {
        "first_name": "Patricia",
        "last_name": "Nguyen",
        "phone": "260-555-0156",
        "email": "patricia.nguyen@example.com",
        "street": "809 W Jefferson Blvd",
        "city": "Fort Wayne",
        "state": "IN",
        "zip_code": "46802",
    },
    {
        "first_name": "Derek",
        "last_name": "Coleman",
        "phone": "260-555-0181",
        "email": "derek.coleman@example.com",
        "street": "7315 St Joe Rd",
        "city": "Fort Wayne",
        "state": "IN",
        "zip_code": "46835",
    },
    {
        "first_name": "Monica",
        "last_name": "Price",
        "phone": "260-555-0149",
        "email": "monica.price@example.com",
        "street": "4602 Trier Rd",
        "city": "Fort Wayne",
        "state": "IN",
        "zip_code": "46815",
    },
]


EQUIPMENT_MODELS = [
    {
        "equipment_type": "Pressure Washer",
        "make": "Honda",
        "model": "GX390 Washer",
        "model_year": 2021,
        "engine_spec": "GX390 13HP",
    },
    {
        "equipment_type": "Zero-Turn Mower",
        "make": "Husqvarna",
        "model": "Z254F",
        "model_year": 2020,
        "engine_spec": "Kawasaki FR691V",
    },
    {
        "equipment_type": "Paint Sprayer",
        "make": "Graco",
        "model": "Ultra Max II 490",
        "model_year": 2019,
        "engine_spec": "Electric 120V",
    },
    {
        "equipment_type": "Generator",
        "make": "Generac",
        "model": "GP6500",
        "model_year": 2022,
        "engine_spec": "389cc OHV",
    },
    {
        "equipment_type": "Walk-Behind Mower",
        "make": "Toro",
        "model": "Recycler 22",
        "model_year": 2021,
        "engine_spec": "Briggs 163cc",
    },
    {
        "equipment_type": "String Trimmer",
        "make": "Stihl",
        "model": "FS 56 RC-E",
        "model_year": 2020,
        "engine_spec": "27.2cc 2-Stroke",
    },
    {
        "equipment_type": "Backpack Blower",
        "make": "Echo",
        "model": "PB-580T",
        "model_year": 2019,
        "engine_spec": "58.2cc 2-Stroke",
    },
    {
        "equipment_type": "Air Compressor",
        "make": "DeWalt",
        "model": "DXCM271",
        "model_year": 2022,
        "engine_spec": "Electric 120V",
    },
]


PARTS = [
    {
        "part_name": "Spark Plug BPR6ES",
        "category": "Ignition",
        "sku": "SP-BPR6ES",
        "unit_price": 7.99,
        "quantity_in_stock": 25,
    },
    {
        "part_name": "Air Filter GX390",
        "category": "Air Intake",
        "sku": "AF-GX390",
        "unit_price": 14.50,
        "quantity_in_stock": 12,
    },
    {
        "part_name": "Carburetor Assembly GX390",
        "category": "Fuel System",
        "sku": "CARB-GX390",
        "unit_price": 89.99,
        "quantity_in_stock": 4,
    },
    {
        "part_name": "Kawasaki Oil Filter",
        "category": "Lubrication",
        "sku": "OF-KAW-FR",
        "unit_price": 12.75,
        "quantity_in_stock": 18,
    },
    {
        "part_name": "Mower Blade Set 54in",
        "category": "Cutting Deck",
        "sku": "BLD-HUS-54",
        "unit_price": 46.00,
        "quantity_in_stock": 6,
    },
    {
        "part_name": "Sprayer Pump Repair Kit",
        "category": "Pump",
        "sku": "KIT-GR-490",
        "unit_price": 74.25,
        "quantity_in_stock": 3,
    },
    {
        "part_name": "Sprayer Tip Guard",
        "category": "Spray Gun",
        "sku": "TG-GR-7-8",
        "unit_price": 19.95,
        "quantity_in_stock": 20,
    },
    {
        "part_name": "Generator Voltage Regulator",
        "category": "Electrical",
        "sku": "VR-GEN-6500",
        "unit_price": 58.40,
        "quantity_in_stock": 5,
    },
    {
        "part_name": "Generator Fuel Shutoff Valve",
        "category": "Fuel System",
        "sku": "FSV-GEN",
        "unit_price": 16.80,
        "quantity_in_stock": 2,
    },
    {
        "part_name": "Briggs Air Filter 163cc",
        "category": "Air Intake",
        "sku": "AF-BR-163",
        "unit_price": 10.95,
        "quantity_in_stock": 14,
    },
    {
        "part_name": "Toro Recycler Blade 22in",
        "category": "Cutting Deck",
        "sku": "BLD-TOR-22",
        "unit_price": 28.75,
        "quantity_in_stock": 9,
    },
    {
        "part_name": "Stihl Trimmer Head",
        "category": "Cutting Head",
        "sku": "HEAD-ST-FS56",
        "unit_price": 32.50,
        "quantity_in_stock": 7,
    },
    {
        "part_name": "Stihl Fuel Line Kit",
        "category": "Fuel System",
        "sku": "FL-ST-2CYC",
        "unit_price": 13.40,
        "quantity_in_stock": 4,
    },
    {
        "part_name": "Echo Blower Carburetor",
        "category": "Fuel System",
        "sku": "CARB-ECHO-58",
        "unit_price": 62.99,
        "quantity_in_stock": 3,
    },
    {
        "part_name": "Echo Air Filter PB580",
        "category": "Air Intake",
        "sku": "AF-ECHO-580",
        "unit_price": 11.25,
        "quantity_in_stock": 11,
    },
    {
        "part_name": "Compressor Pressure Switch",
        "category": "Electrical",
        "sku": "PS-DW-COMP",
        "unit_price": 39.80,
        "quantity_in_stock": 6,
    },
    {
        "part_name": "Compressor Regulator Assembly",
        "category": "Air Control",
        "sku": "REG-DW-COMP",
        "unit_price": 47.60,
        "quantity_in_stock": 2,
    },
    {
        "part_name": "Small Engine Oil 10W-30",
        "category": "Lubrication",
        "sku": "OIL-10W30-QT",
        "unit_price": 6.50,
        "quantity_in_stock": 30,
    },
    {
        "part_name": "Shop Supplies Charge",
        "category": "Supplies",
        "sku": "SHOP-SUP",
        "unit_price": 8.00,
        "quantity_in_stock": 100,
    },
]


EQUIPMENT = [
    {"customer_index": 0, "model_index": 0, "serial_number": "HW-GX390-1044"},
    {"customer_index": 0, "model_index": 1, "serial_number": "HZ254F-8871"},
    {"customer_index": 1, "model_index": 2, "serial_number": "GR490-5520"},
    {"customer_index": 2, "model_index": 3, "serial_number": "GEN6500-2409"},
    {"customer_index": 3, "model_index": 0, "serial_number": "HW-GX390-1182"},
    {"customer_index": 4, "model_index": 1, "serial_number": "HZ254F-9134"},
    {"customer_index": 5, "model_index": 2, "serial_number": "GR490-6177"},
    {"customer_index": 6, "model_index": 3, "serial_number": "GEN6500-3081"},
    {"customer_index": 6, "model_index": 0, "serial_number": "HW-GX390-1309"},
    {"customer_index": 7, "model_index": 4, "serial_number": "TOR22-4018"},
    {"customer_index": 7, "model_index": 5, "serial_number": "STFS56-2284"},
    {"customer_index": 8, "model_index": 6, "serial_number": "ECHO580-7712"},
    {"customer_index": 9, "model_index": 7, "serial_number": "DWCOMP-6521"},
    {"customer_index": 10, "model_index": 4, "serial_number": "TOR22-4490"},
    {"customer_index": 11, "model_index": 5, "serial_number": "STFS56-3102"},
    {"customer_index": 11, "model_index": 6, "serial_number": "ECHO580-8225"},
]


PART_FITMENTS = [
    {"model_index": 0, "part_index": 0, "notes": "Common tune-up plug for GX390 engines."},
    {"model_index": 0, "part_index": 1, "notes": "Direct-fit air filter for GX390 pressure washer engines."},
    {"model_index": 0, "part_index": 2, "notes": "Compatible replacement carburetor assembly."},
    {"model_index": 1, "part_index": 0, "notes": "Compatible ignition plug for Kawasaki FR-series engine."},
    {"model_index": 1, "part_index": 3, "notes": "Oil filter for Kawasaki FR-series mower engines."},
    {"model_index": 1, "part_index": 4, "notes": "Blade set for 54-inch deck."},
    {"model_index": 2, "part_index": 5, "notes": "Pump rebuild kit for Ultra Max II 490."},
    {"model_index": 2, "part_index": 6, "notes": "Compatible guard for standard Graco spray tips."},
    {"model_index": 3, "part_index": 7, "notes": "Voltage regulator for GP6500 generator output issues."},
    {"model_index": 3, "part_index": 8, "notes": "Fuel shutoff valve for GP-series generators."},
    {"model_index": 4, "part_index": 0, "notes": "Common plug used during walk-behind mower tune-up."},
    {"model_index": 4, "part_index": 9, "notes": "Direct-fit Briggs air filter for Toro Recycler 22."},
    {"model_index": 4, "part_index": 10, "notes": "Replacement blade for 22-inch Recycler deck."},
    {"model_index": 4, "part_index": 17, "notes": "Standard small-engine oil used during mower service."},
    {"model_index": 5, "part_index": 11, "notes": "Replacement cutting head for FS 56 trimmer."},
    {"model_index": 5, "part_index": 12, "notes": "Fuel line kit for 2-stroke trimmer fuel delivery issues."},
    {"model_index": 5, "part_index": 18, "notes": "Shop supplies entry for fuel-system service."},
    {"model_index": 6, "part_index": 13, "notes": "Carburetor replacement for Echo PB-580T blower."},
    {"model_index": 6, "part_index": 14, "notes": "Air filter for Echo backpack blower service."},
    {"model_index": 6, "part_index": 18, "notes": "Shop supplies entry for blower service."},
    {"model_index": 7, "part_index": 15, "notes": "Pressure switch for compressor start/stop problems."},
    {"model_index": 7, "part_index": 16, "notes": "Regulator assembly for pressure control issues."},
]


SERVICE_ORDERS = [
    {
        "equipment_index": 1,
        "reported_issue": "Mower runs rough and blades are vibrating.",
        "diagnosis_notes": "Blade set is worn; tune-up recommended.",
        "labor_cost": 95.00,
        "status": "IN_REPAIR",
        "parts": [
            {"part_index": 3, "quantity_used": 1},
            {"part_index": 4, "quantity_used": 1},
        ],
    },
    {
        "equipment_index": 2,
        "reported_issue": "Paint sprayer loses pressure during operation.",
        "diagnosis_notes": "Pump repair kit needed; customer approval pending.",
        "labor_cost": 80.00,
        "status": "AWAITING_APPROVAL",
        "parts": [
            {"part_index": 5, "quantity_used": 1},
        ],
    },
    {
        "equipment_index": 3,
        "reported_issue": "Generator starts but does not produce stable power.",
        "diagnosis_notes": "Voltage regulator failed testing.",
        "labor_cost": 110.00,
        "status": "WAITING_FOR_PARTS",
        "parts": [
            {"part_index": 7, "quantity_used": 1},
        ],
    },
    {
        "equipment_index": 4,
        "reported_issue": "Pressure washer will not start after sitting for the winter.",
        "diagnosis_notes": "Fuel varnish found in carburetor; replacement recommended.",
        "labor_cost": 72.50,
        "status": "DROPPED_OFF",
        "parts": [],
    },
    {
        "equipment_index": 5,
        "reported_issue": "Mower has uneven cut and excessive deck noise.",
        "diagnosis_notes": "Blade set is worn; oil filter replacement recommended during service.",
        "labor_cost": 125.00,
        "status": "AWAITING_APPROVAL",
        "parts": [
            {"part_index": 3, "quantity_used": 1},
            {"part_index": 4, "quantity_used": 1},
        ],
    },
    {
        "equipment_index": 6,
        "reported_issue": "Sprayer has low pressure and inconsistent spray pattern.",
        "diagnosis_notes": "Pump repair kit and tip guard replacement completed.",
        "labor_cost": 90.00,
        "status": "READY_FOR_PICKUP",
        "parts": [
            {"part_index": 5, "quantity_used": 1},
            {"part_index": 6, "quantity_used": 1},
        ],
    },
    {
        "equipment_index": 7,
        "reported_issue": "Generator fuel leaks from shutoff area.",
        "diagnosis_notes": "Fuel shutoff valve replaced; leak test passed.",
        "labor_cost": 65.00,
        "status": "READY_FOR_PICKUP",
        "parts": [
            {"part_index": 8, "quantity_used": 1},
        ],
    },
    {
        "equipment_index": 8,
        "reported_issue": "Pressure washer lacks power under load.",
        "diagnosis_notes": "Air filter clogged; spark plug fouled. Tune-up completed.",
        "labor_cost": 55.00,
        "status": "CLOSED",
        "parts": [
            {"part_index": 0, "quantity_used": 1},
            {"part_index": 1, "quantity_used": 1},
        ],
        "mark_paid": True,
        "payment_method": "CARD",
    },
    {
        "equipment_index": 9,
        "reported_issue": "Walk-behind mower will not keep running after start.",
        "diagnosis_notes": "Initial intake only; mechanic inspection pending.",
        "labor_cost": 0.00,
        "status": "DROPPED_OFF",
        "parts": [],
    },
    {
        "equipment_index": 10,
        "reported_issue": "String trimmer leaks fuel near primer area.",
        "diagnosis_notes": "Fuel line kit recommended; estimate awaiting customer approval.",
        "labor_cost": 48.00,
        "status": "AWAITING_APPROVAL",
        "parts": [
            {"part_index": 12, "quantity_used": 1},
            {"part_index": 18, "quantity_used": 1},
        ],
    },
    {
        "equipment_index": 11,
        "reported_issue": "Backpack blower starts but bogs down at full throttle.",
        "diagnosis_notes": "Carburetor replacement approved; repair in progress.",
        "labor_cost": 70.00,
        "status": "IN_REPAIR",
        "parts": [
            {"part_index": 13, "quantity_used": 1},
            {"part_index": 14, "quantity_used": 1},
        ],
    },
    {
        "equipment_index": 12,
        "reported_issue": "Air compressor will not shut off automatically.",
        "diagnosis_notes": "Pressure switch failed; waiting for regulator assembly review.",
        "labor_cost": 85.00,
        "status": "WAITING_FOR_PARTS",
        "parts": [
            {"part_index": 15, "quantity_used": 1},
        ],
    },
    {
        "equipment_index": 13,
        "reported_issue": "Mower blade is bent after hitting a root.",
        "diagnosis_notes": "Blade replacement and oil service completed.",
        "labor_cost": 62.00,
        "status": "READY_FOR_PICKUP",
        "parts": [
            {"part_index": 10, "quantity_used": 1},
            {"part_index": 17, "quantity_used": 1},
        ],
    },
    {
        "equipment_index": 14,
        "reported_issue": "Trimmer head does not feed line correctly.",
        "diagnosis_notes": "Trimmer head replaced and tested.",
        "labor_cost": 42.00,
        "status": "READY_FOR_PICKUP",
        "parts": [
            {"part_index": 11, "quantity_used": 1},
            {"part_index": 18, "quantity_used": 1},
        ],
    },
    {
        "equipment_index": 15,
        "reported_issue": "Blower hard-starts and lacks airflow.",
        "diagnosis_notes": "Air filter replaced; carburetor cleaned. Unit picked up and paid.",
        "labor_cost": 58.00,
        "status": "CLOSED",
        "parts": [
            {"part_index": 14, "quantity_used": 1},
            {"part_index": 18, "quantity_used": 1},
        ],
        "mark_paid": True,
        "payment_method": "CASH",
    },
]





PAYMENT_METHODS = ["CASH", "CARD", "CHECK"]


def insert_customer(cursor, customer):
    """Insert one customer and return its generated ID."""
    customer_id = cursor.var(int)
    cursor.execute(
        """
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
        RETURNING customer_id INTO :customer_id
        """,
        customer_id=customer_id,
        **customer,
    )
    return customer_id.getvalue()[0]


def insert_equipment_model(cursor, model):
    """Insert one equipment model and return its generated ID."""
    equipment_model_id = cursor.var(int)
    cursor.execute(
        """
        INSERT INTO equipment_model (
            equipment_type,
            make,
            model,
            model_year,
            engine_spec
        ) VALUES (
            :equipment_type,
            :make,
            :model,
            :model_year,
            :engine_spec
        )
        RETURNING equipment_model_id INTO :equipment_model_id
        """,
        equipment_model_id=equipment_model_id,
        **model,
    )
    return equipment_model_id.getvalue()[0]


def insert_part(cursor, part):
    """Insert one part and return its generated ID."""
    part_id = cursor.var(int)
    cursor.execute(
        """
        INSERT INTO part (
            part_name,
            category,
            sku,
            unit_price,
            quantity_in_stock
        ) VALUES (
            :part_name,
            :category,
            :sku,
            :unit_price,
            :quantity_in_stock
        )
        RETURNING part_id INTO :part_id
        """,
        part_id=part_id,
        **part,
    )
    return part_id.getvalue()[0]


def insert_equipment(cursor, equipment, customer_ids, model_ids):
    """Insert one customer-owned equipment unit and return its generated ID."""
    equipment_id = cursor.var(int)
    cursor.execute(
        """
        INSERT INTO equipment (
            customer_id,
            equipment_model_id,
            serial_number
        ) VALUES (
            :customer_id,
            :equipment_model_id,
            :serial_number
        )
        RETURNING equipment_id INTO :equipment_id
        """,
        equipment_id=equipment_id,
        customer_id=customer_ids[equipment["customer_index"]],
        equipment_model_id=model_ids[equipment["model_index"]],
        serial_number=equipment["serial_number"],
    )
    return equipment_id.getvalue()[0]


def insert_part_fitment(cursor, fitment, model_ids, part_ids):
    """Insert one part compatibility record."""
    cursor.execute(
        """
        INSERT INTO part_fitment (
            equipment_model_id,
            part_id,
            notes
        ) VALUES (
            :equipment_model_id,
            :part_id,
            :notes
        )
        """,
        equipment_model_id=model_ids[fitment["model_index"]],
        part_id=part_ids[fitment["part_index"]],
        notes=fitment["notes"],
    )


def insert_service_order(cursor, service_order, equipment_ids, part_ids):
    """Insert one service order and associated parts."""
    service_order_id = cursor.var(int)
    cursor.execute(
        """
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
        RETURNING service_order_id INTO :service_order_id
        """,
        service_order_id=service_order_id,
        equipment_id=equipment_ids[service_order["equipment_index"]],
        reported_issue=service_order["reported_issue"],
        diagnosis_notes=service_order["diagnosis_notes"],
        labor_cost=service_order["labor_cost"],
        status=service_order["status"],
    )

    created_order_id = service_order_id.getvalue()[0]

    for part_line in service_order["parts"]:
        part_id = part_ids[part_line["part_index"]]
        cursor.execute(
            """
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
            """,
            service_order_id=created_order_id,
            part_id=part_id,
            quantity_used=part_line["quantity_used"],
        )

    if service_order["status"] == "READY_FOR_PICKUP":
        cursor.execute(
            """
            UPDATE service_order
            SET status = 'READY_FOR_PICKUP'
            WHERE service_order_id = :service_order_id
            """,
            service_order_id=created_order_id,
        )

    if service_order.get("mark_paid"):
        cursor.execute(
            """
            UPDATE service_order
            SET status = 'READY_FOR_PICKUP'
            WHERE service_order_id = :service_order_id
            """,
            service_order_id=created_order_id,
        )
        cursor.execute(
            """
            UPDATE invoice
            SET payment_status = 'PAID',
                payment_method = :payment_method,
                payment_date = SYSDATE
            WHERE service_order_id = :service_order_id
            """,
            service_order_id=created_order_id,
            payment_method=service_order.get("payment_method", "CARD"),
        )
        cursor.execute(
            """
            UPDATE service_order
            SET status = 'CLOSED',
                date_closed = SYSDATE
            WHERE service_order_id = :service_order_id
            """,
            service_order_id=created_order_id,
        )

    return created_order_id


def populate_database():
    """Populate the database with demo-ready records."""
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                customer_ids = [insert_customer(cursor, customer) for customer in CUSTOMERS]
                model_ids = [insert_equipment_model(cursor, model) for model in EQUIPMENT_MODELS]
                part_ids = [insert_part(cursor, part) for part in PARTS]

                equipment_ids = [
                    insert_equipment(cursor, equipment, customer_ids, model_ids)
                    for equipment in EQUIPMENT
                ]

                for fitment in PART_FITMENTS:
                    insert_part_fitment(cursor, fitment, model_ids, part_ids)

                service_order_ids = [
                    insert_service_order(cursor, order, equipment_ids, part_ids)
                    for order in SERVICE_ORDERS
                ]

                connection.commit()

        print("Demo database population complete.")
       
        print()
        print("Existing sample service order IDs by status")
        print("-------------------------------------------")
        for service_order_id, order in zip(service_order_ids, SERVICE_ORDERS):
            print(f"Service order ID: {service_order_id} | Status: {order['status']}")

    except oracledb.DatabaseError as error:
        print("Database population failed.")
        print(error)


if __name__ == "__main__":
    populate_database()