"""Text-based SRPMS prototype interface."""

from db import test_connection
from queries import (
    add_part_to_service_order,
    create_customer,
    create_equipment,
    create_service_order,
    list_active_service_orders,
    list_compatible_parts_for_equipment,
    list_compatible_parts_for_service_order,
    list_customers,
    list_equipment_by_customer,
    list_equipment_models,
    list_invoices,
    list_low_stock_parts,
    mark_invoice_paid,
    show_invoice_for_service_order,
    show_service_order_estimate,
    update_service_order_details,
    update_service_order_status,
)


VALID_STATUSES = [
    "DROPPED_OFF",
    "AWAITING_APPROVAL",
    "WAITING_FOR_PARTS",
    "IN_REPAIR",
    "READY_FOR_PICKUP",
    "DECLINED",
    "CLOSED",
]


MAIN_MENU_OPTIONS = [
    "Customers & Equipment",
    "Service Orders",
    "Parts & Inventory",
    "Invoices",
]


def print_numbered_menu(title, options, exit_label="Back"):
    """Print a numbered menu with a consistent layout."""
    print()
    print(title)
    print("-" * len(title))

    for index, option in enumerate(options, start=1):
        print(f"{index}. {option}")

    print(f"0. {exit_label}")
    print()


def read_int(prompt):
    """Read an integer from the user."""
    while True:
        value = input(prompt).strip()

        try:
            return int(value)
        except ValueError:
            print("Please enter a valid number.")


def read_float(prompt):
    """Read a decimal number from the user."""
    while True:
        value = input(prompt).strip()

        try:
            return float(value)
        except ValueError:
            print("Please enter a valid decimal number.")


def handle_equipment_by_customer():
    customer_id = read_int("Enter customer ID: ")
    list_equipment_by_customer(customer_id)


def handle_compatible_parts():
    print("Customers:")
    list_customers()

    customer_id = read_int("Enter customer ID to view equipment: ")
    list_equipment_by_customer(customer_id)

    equipment_id = read_int("Enter equipment ID to view compatible parts: ")
    list_compatible_parts_for_equipment(equipment_id)


def handle_low_stock_parts():
    threshold = read_int("Enter stock threshold: ")
    list_low_stock_parts(threshold)


def handle_status_update():
    service_order_id = read_int("Enter service order ID: ")

    print_numbered_menu("Valid Statuses", VALID_STATUSES, exit_label="Cancel")
    status_choice = read_int("Choose new status: ")

    if status_choice == 0:
        print("Status update canceled.")
        return

    if status_choice < 1 or status_choice > len(VALID_STATUSES):
        print("Invalid status option. No update was made.")
        return

    new_status = VALID_STATUSES[status_choice - 1]
    update_service_order_status(service_order_id, new_status)


def handle_invoice_lookup():
    service_order_id = read_int("Enter service order ID: ")
    show_invoice_for_service_order(service_order_id)


def handle_list_invoices():
    list_invoices()


def handle_create_customer():
    first_name = input("First name: ").strip()
    last_name = input("Last name: ").strip()
    phone = input("Phone: ").strip()
    email = input("Email: ").strip()
    street = input("Street: ").strip()
    city = input("City: ").strip()
    state = input("State: ").strip().upper()
    zip_code = input("Zip code: ").strip()

    create_customer(first_name, last_name, phone, email, street, city, state, zip_code)


def handle_create_equipment():
    customer_id = read_int("Customer ID: ")
    print("Available equipment models:")
    list_equipment_models()
    equipment_model_id = read_int("Equipment model ID: ")
    serial_number = input("Serial number: ").strip()

    create_equipment(customer_id, equipment_model_id, serial_number)


def handle_create_service_order():
    equipment_id = read_int("Equipment ID: ")
    reported_issue = input("Reported issue: ").strip()

    create_service_order(
        equipment_id,
        reported_issue,
        "",
        0,
        "DROPPED_OFF",
    )



def handle_add_part_to_service_order():
    service_order_id = read_int("Service order ID: ")
    part_id = read_int("Part ID: ")
    quantity_used = read_int("Quantity used: ")

    add_part_to_service_order(service_order_id, part_id, quantity_used)


def handle_show_service_order_estimate():
    service_order_id = read_int("Service order ID: ")
    show_service_order_estimate(service_order_id)


def handle_mechanic_update_service_order():
    service_order_id = read_int("Service order ID: ")
    diagnosis_notes = input("Diagnosis notes: ").strip()
    labor_cost = read_float("Labor cost: ")

    if not update_service_order_details(service_order_id, diagnosis_notes, labor_cost):
        return

    while True:
        add_part = input("Add a part used in this repair? (y/n): ").strip().lower()

        if add_part == "n":
            break

        if add_part != "y":
            print("Please enter y or n.")
            continue

        print("Compatible parts for this service order's equipment:")
        list_compatible_parts_for_service_order(service_order_id)

        part_id = read_int("Part ID: ")
        quantity_used = read_int("Quantity used: ")
        add_part_to_service_order(service_order_id, part_id, quantity_used)

    change_status = input("Submit estimate and update status to AWAITING_APPROVAL? (y/n): ").strip().lower()

    if change_status == "y":
        update_service_order_status(service_order_id, "AWAITING_APPROVAL")


def handle_mark_invoice_paid():
    service_order_id = read_int("Service order ID: ")
    payment_method = input("Payment method: ").strip().upper()

    mark_invoice_paid(service_order_id, payment_method)


def customers_equipment_menu():
    """Run the customer/equipment submenu."""
    options = [
        "View customers",
        "Create customer",
        "View equipment by customer",
        "View equipment models",
        "Register equipment",
    ]

    while True:
        print_numbered_menu("Customers & Equipment", options)
        choice = input("Choose an option: ").strip()

        if choice == "1":
            list_customers()
        elif choice == "2":
            handle_create_customer()
        elif choice == "3":
            handle_equipment_by_customer()
        elif choice == "4":
            list_equipment_models()
        elif choice == "5":
            handle_create_equipment()
        elif choice == "0":
            break
        else:
            print("Invalid option. Please choose a menu number.")


def service_orders_menu():
    """Run the service order submenu."""
    options = [
        "View active service orders",
        "Create service order",
        "Mechanic update service order",
        "View service order estimate",
        "Add part to service order",
        "Update service order status",
    ]

    while True:
        print_numbered_menu("Service Orders", options)
        choice = input("Choose an option: ").strip()

        if choice == "1":
            list_active_service_orders()
        elif choice == "2":
            handle_create_service_order()
        elif choice == "3":
            handle_mechanic_update_service_order()
        elif choice == "4":
            handle_show_service_order_estimate()
        elif choice == "5":
            handle_add_part_to_service_order()
        elif choice == "6":
            handle_status_update()
        elif choice == "0":
            break
        else:
            print("Invalid option. Please choose a menu number.")


def parts_inventory_menu():
    """Run the parts/inventory submenu."""
    options = [
        "View compatible parts for equipment",
        "View low-stock parts",
    ]

    while True:
        print_numbered_menu("Parts & Inventory", options)
        choice = input("Choose an option: ").strip()

        if choice == "1":
            handle_compatible_parts()
        elif choice == "2":
            handle_low_stock_parts()
        elif choice == "0":
            break
        else:
            print("Invalid option. Please choose a menu number.")


def invoices_menu():
    """Run the invoice submenu."""
    options = [
        "View all invoices",
        "View invoice for service order",
        "Mark invoice as paid",
    ]

    while True:
        print_numbered_menu("Invoices", options)
        choice = input("Choose an option: ").strip()

        if choice == "1":
            handle_list_invoices()
        elif choice == "2":
            handle_invoice_lookup()
        elif choice == "3":
            handle_mark_invoice_paid()
        elif choice == "0":
            break
        else:
            print("Invalid option. Please choose a menu number.")





def run_main_menu():
    """Run the main menu loop."""
    while True:
        print_numbered_menu("SRPMS Main Menu", MAIN_MENU_OPTIONS, exit_label="Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            customers_equipment_menu()
        elif choice == "2":
            service_orders_menu()
        elif choice == "3":
            parts_inventory_menu()
        elif choice == "4":
            invoices_menu()
        elif choice == "5":
            demo_workflow_menu()
        elif choice == "0":
            print("Exiting SRPMS prototype.")
            break
        else:
            print("Invalid option. Please choose a menu number.")


def main():
    print("SRPMS CLI Prototype")
    print("-------------------")

    if test_connection():
        run_main_menu()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting SRPMS prototype.")
