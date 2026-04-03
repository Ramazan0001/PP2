from connect import get_connection
import csv


def show_paginated():
    limit = 5
    page = int(input("Enter page number: "))
    offset = (page - 1) * limit

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM phonebook LIMIT %s OFFSET %s",
        (limit, offset)
    )

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def add_or_update():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    conn = get_connection()
    cur = conn.cursor()

    # Проверяем есть ли уже контакт
    cur.execute(
        "SELECT * FROM phonebook WHERE name = %s",
        (name,)
    )

    result = cur.fetchone()

    if result:
        # UPDATE
        cur.execute(
            "UPDATE phonebook SET phone = %s WHERE name = %s",
            (phone, name)
        )
        print("Updated!")
    else:
        # INSERT
        cur.execute(
            "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
            (name, phone)
        )
        print("Added!")

    conn.commit()
    cur.close()
    conn.close()


def delete_contact():
    name = input("Enter name to delete: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM phonebook WHERE name = %s",
        (name,)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Deleted!")


def search_contact():
    name = input("Enter name to search: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM phonebook WHERE name ILIKE %s",
        ('%' + name + '%',)
    )

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def import_csv():
    filename = input("Enter CSV file name: ")

    conn = get_connection()
    cur = conn.cursor()

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.reader(file)

        for row in reader:
            name = row[0]
            phone = row[1]

            cur.execute(
                "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
                (name, phone)
            )

    conn.commit()
    cur.close()
    conn.close()

    print("CSV imported!")


def main():
    while True:
        print("\n1 - Search")
        print("2 - Add / Update")
        print("3 - Show (pagination)")
        print("4 - Delete")
        print("5 - Import CSV")
        print("6 - Exit")

        choice = input("Choose: ")

        if choice == "1":
            search_contact()
        elif choice == "2":
            add_or_update()
        elif choice == "3":
            show_paginated()
        elif choice == "4":
            delete_contact()
        elif choice == "5":
            import_csv()
        elif choice == "6":
            break
        else:
            print("Wrong choice!")


if __name__ == "__main__":
    main()