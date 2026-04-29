import csv
import json
from connect import get_connection


def run_sql_file(filename):
    conn = get_connection()
    cur = conn.cursor()

    with open(filename, "r", encoding="utf-8") as file:
        sql = file.read()

    cur.execute(sql)
    conn.commit()

    cur.close()
    conn.close()


def setup_database():
    run_sql_file("schema.sql")
    run_sql_file("procedures.sql")
    print("Database setup completed.")


def get_group_id(cur, group_name):
    cur.execute(
        """
        INSERT INTO groups (name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING
        """,
        (group_name,)
    )

    cur.execute(
        "SELECT id FROM groups WHERE LOWER(name) = LOWER(%s)",
        (group_name,)
    )

    result = cur.fetchone()
    return result[0]


def add_contact():
    name = input("Enter name: ")
    email = input("Enter email: ")
    birthday = input("Enter birthday YYYY-MM-DD: ")
    group_name = input("Enter group Family/Work/Friend/Other: ")
    phone = input("Enter phone: ")
    phone_type = input("Enter phone type home/work/mobile: ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        group_id = get_group_id(cur, group_name)

        cur.execute(
            """
            INSERT INTO contacts (name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """,
            (name, email, birthday, group_id)
        )

        contact_id = cur.fetchone()[0]

        cur.execute(
            """
            INSERT INTO phones (contact_id, phone, type)
            VALUES (%s, %s, %s)
            """,
            (contact_id, phone, phone_type)
        )

        conn.commit()
        print("Contact added successfully.")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    cur.close()
    conn.close()


def add_phone_to_contact():
    name = input("Enter contact name: ")
    phone = input("Enter new phone: ")
    phone_type = input("Enter type home/work/mobile: ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "CALL add_phone(%s, %s, %s)",
            (name, phone, phone_type)
        )

        conn.commit()
        print("Phone added successfully.")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    cur.close()
    conn.close()


def move_contact_to_group():
    name = input("Enter contact name: ")
    group_name = input("Enter new group: ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "CALL move_to_group(%s, %s)",
            (name, group_name)
        )

        conn.commit()
        print("Contact moved to group successfully.")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    cur.close()
    conn.close()


def show_contacts(rows):
    print()
    print("=" * 120)
    print(f"{'ID':<5} {'Name':<20} {'Email':<25} {'Birthday':<15} {'Group':<15} {'Phones':<40}")
    print("=" * 120)

    for row in rows:
        print(
            f"{row[0]:<5} "
            f"{row[1]:<20} "
            f"{str(row[2]):<25} "
            f"{str(row[3]):<15} "
            f"{str(row[4]):<15} "
            f"{str(row[5]):<40}"
        )

    print("=" * 120)


def view_all_contacts():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            c.id,
            c.name,
            c.email,
            c.birthday,
            g.name,
            COALESCE(STRING_AGG(p.phone || ' (' || p.type || ')', ', '), '')
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        GROUP BY c.id, c.name, c.email, c.birthday, g.name
        ORDER BY c.id
        """
    )

    rows = cur.fetchall()
    show_contacts(rows)

    cur.close()
    conn.close()


def filter_by_group():
    group_name = input("Enter group name: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            c.id,
            c.name,
            c.email,
            c.birthday,
            g.name,
            COALESCE(STRING_AGG(p.phone || ' (' || p.type || ')', ', '), '')
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        WHERE LOWER(g.name) = LOWER(%s)
        GROUP BY c.id, c.name, c.email, c.birthday, g.name
        ORDER BY c.name
        """,
        (group_name,)
    )

    rows = cur.fetchall()
    show_contacts(rows)

    cur.close()
    conn.close()


def search_contact():
    query = input("Search by name, email, or phone: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM search_contacts(%s)",
        (query,)
    )

    rows = cur.fetchall()
    show_contacts(rows)

    cur.close()
    conn.close()


def sort_contacts():
    print("1. Sort by name")
    print("2. Sort by birthday")
    print("3. Sort by date added")

    choice = input("Choose: ")

    if choice == "1":
        order_by = "c.name"
    elif choice == "2":
        order_by = "c.birthday NULLS LAST"
    elif choice == "3":
        order_by = "c.created_at"
    else:
        print("Wrong choice.")
        return

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        f"""
        SELECT
            c.id,
            c.name,
            c.email,
            c.birthday,
            g.name,
            COALESCE(STRING_AGG(p.phone || ' (' || p.type || ')', ', '), '')
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        GROUP BY c.id, c.name, c.email, c.birthday, g.name
        ORDER BY {order_by}
        """
    )

    rows = cur.fetchall()
    show_contacts(rows)

    cur.close()
    conn.close()


def pagination(): 
    limit = 3
    offset = 0


    while True:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM get_contacts_paginated(%s, %s)",
            (limit, offset)
        )

        rows = cur.fetchall()

        cur.close()
        conn.close()

        if len(rows) == 0:
            print("No contacts on this page.")
        else:
            show_contacts(rows)

        command = input("next / prev / quit: ")

        if command == "next":
            offset += limit

        elif command == "prev":
            offset -= limit

            if offset < 0:
                offset = 0

        elif command == "quit":
            break

        else:
            print("Wrong command.")
 


def export_json():
    filename = input("Enter JSON filename: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            c.id,
            c.name,
            c.email,
            c.birthday,
            c.created_at,
            g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY c.id
        """
    )

    contacts = cur.fetchall()
    data = []

    for contact in contacts:
        contact_id = contact[0]

        cur.execute(
            """
            SELECT phone, type
            FROM phones
            WHERE contact_id = %s
            """,
            (contact_id,)
        )

        phones = cur.fetchall()

        phone_list = []

        for phone in phones:
            phone_list.append({
                "phone": phone[0],
                "type": phone[1]
            })

        item = {
            "name": contact[1],
            "email": contact[2],
            "birthday": str(contact[3]) if contact[3] else None,
            "created_at": str(contact[4]) if contact[4] else None,
            "group": contact[5],
            "phones": phone_list
        }

        data.append(item)

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    cur.close()
    conn.close()

    print("Export completed.")


def import_json():
    filename = input("Enter JSON filename: ")

    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    conn = get_connection()
    cur = conn.cursor()

    for item in data:
        name = item["name"]

        cur.execute(
            "SELECT id FROM contacts WHERE LOWER(name) = LOWER(%s)",
            (name,)
        )

        existing = cur.fetchone()

        if existing:
            print(f"Contact {name} already exists.")
            action = input("skip / overwrite: ")

            if action == "skip":
                continue

            elif action == "overwrite":
                contact_id = existing[0]

                group_id = get_group_id(cur, item["group"])

                cur.execute(
                    """
                    UPDATE contacts
                    SET email = %s,
                        birthday = %s,
                        group_id = %s
                    WHERE id = %s
                    """,
                    (
                        item["email"],
                        item["birthday"],
                        group_id,
                        contact_id
                    )
                )

                cur.execute(
                    "DELETE FROM phones WHERE contact_id = %s",
                    (contact_id,)
                )

                for phone_item in item["phones"]:
                    cur.execute(
                        """
                        INSERT INTO phones (contact_id, phone, type)
                        VALUES (%s, %s, %s)
                        """,
                        (
                            contact_id,
                            phone_item["phone"],
                            phone_item["type"]
                        )
                    )

            else:
                print("Wrong action. Skipped.")
                continue

        else:
            group_id = get_group_id(cur, item["group"])

            cur.execute(
                """
                INSERT INTO contacts (name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """,
                (
                    item["name"],
                    item["email"],
                    item["birthday"],
                    group_id
                )
            )

            contact_id = cur.fetchone()[0]

            for phone_item in item["phones"]:
                cur.execute(
                    """
                    INSERT INTO phones (contact_id, phone, type)
                    VALUES (%s, %s, %s)
                    """,
                    (
                        contact_id,
                        phone_item["phone"],
                        phone_item["type"]
                    )
                )

    conn.commit()

    cur.close()
    conn.close()

    print("Import completed.")


def import_csv():
    filename = input("Enter CSV filename: ")

    conn = get_connection()
    cur = conn.cursor()

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            name = row["name"]
            email = row["email"]
            birthday = row["birthday"]
            group_name = row["group"]
            phone = row["phone"]
            phone_type = row["type"]

            group_id = get_group_id(cur, group_name)

            cur.execute(
                "SELECT id FROM contacts WHERE LOWER(name) = LOWER(%s)",
                (name,)
            )

            existing = cur.fetchone()

            if existing:
                contact_id = existing[0]
            else:
                cur.execute(
                    """
                    INSERT INTO contacts (name, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                    """,
                    (name, email, birthday, group_id)
                )

                contact_id = cur.fetchone()[0]

            cur.execute(
                """
                INSERT INTO phones (contact_id, phone, type)
                VALUES (%s, %s, %s)
                """,
                (contact_id, phone, phone_type)
            )

    conn.commit()

    cur.close()
    conn.close()

    print("CSV import completed.")


def delete_contact():
    name = input("Enter contact name to delete: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM contacts WHERE LOWER(name) = LOWER(%s)",
        (name,)
    )

    conn.commit()

    cur.close()
    conn.close()

    print("Contact deleted.")


def menu():
    while True:
        print()
        print("===== PHONEBOOK TSIS 1 =====")
        print("1. Setup database")
        print("2. Add contact")
        print("3. Add phone to contact")
        print("4. Move contact to group")
        print("5. View all contacts")
        print("6. Filter by group")
        print("7. Search by name/email/phone")
        print("8. Sort contacts")
        print("9. Pagination")
        print("10. Export to JSON")
        print("11. Import from JSON")
        print("12. Import from CSV")
        print("13. Delete contact")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            setup_database()

        elif choice == "2":
            add_contact()

        elif choice == "3":
            add_phone_to_contact()

        elif choice == "4":
            move_contact_to_group()

        elif choice == "5":
            view_all_contacts()

        elif choice == "6":
            filter_by_group()

        elif choice == "7":
            search_contact()

        elif choice == "8":
            sort_contacts()

        elif choice == "9":
            pagination()

        elif choice == "10":
            export_json()

        elif choice == "11":
            import_json()

        elif choice == "12":
            import_csv()

        elif choice == "13":
            delete_contact()

        elif choice == "0":
            print("Goodbye.")
            break

        else:
            print("Wrong choice.")


menu()