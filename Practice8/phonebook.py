import psycopg2
from connect import get_connection


#1
def show_contacts():
    limit = int(input("Limit: "))
    offset = int(input("Offset: "))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM get_contacts_paginated(%s, %s)",
        (limit, offset)
    )

    rows = cur.fetchall()

    if not rows:
        print("No data")
    else:
        for row in rows:
            print(row)

    cur.close()
    conn.close()


#2
def add_or_update():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "CALL upsert_contact(%s, %s)",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Done!")


#3
def search_contact():
    value = input("Search: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM get_contacts_by_pattern(%s)",
        (value,)
    )

    rows = cur.fetchall()

    if not rows:
        print("Not found")
    else:
        for row in rows:
            print(row)

    cur.close()
    conn.close()


#4
def delete_contact():
    value = input("Enter name or phone: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "CALL delete_contact_proc(%s)",
        (value,)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Deleted!")


#5
def bulk_insert():
    names = input("Names (comma): ").split(",")
    phones = input("Phones (comma): ").split(",")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "CALL insert_many_contacts(%s, %s)",
        (names, phones)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Bulk insert done!")

def main():
    while True:
        print("\n--- PHONEBOOK ---")
        print("1 - Show contacts")
        print("2 - Add / Update")
        print("3 - Search")
        print("4 - Delete")
        print("5 - Bulk insert")
        print("6 - Exit")

        choice = input("Choose: ")

        if choice == "1":
            show_contacts()
        elif choice == "2":
            add_or_update()
        elif choice == "3":
            search_contact()
        elif choice == "4":
            delete_contact()
        elif choice == "5":
            bulk_insert()
        elif choice == "6":
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()