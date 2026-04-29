import csv
from connect import get_connection


def insert_contact(username, phone):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO phonebook (username, phone) VALUES (%s, %s);",
            (username, phone)
        )

        conn.commit()
        print("Contact added successfully.")

        cur.close()
        conn.close()

    except Exception as e:
        print("Error:", e)


def show_contacts():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM phonebook;")
        rows = cur.fetchall()

        print("\nContacts:")
        for row in rows:
            print(row)

        cur.close()
        conn.close()

    except Exception as e:
        print("Error:", e)


def update_contact(username, new_phone):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "UPDATE phonebook SET phone = %s WHERE username = %s;",
            (new_phone, username)
        )

        conn.commit()
        print("Contact updated successfully.")

        cur.close()
        conn.close()

    except Exception as e:
        print("Error:", e)


def delete_contact(username):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM phonebook WHERE username = %s;",
            (username,)
        )

        conn.commit()
        print("Contact deleted successfully.")

        cur.close()
        conn.close()

    except Exception as e:
        print("Error:", e)


def insert_from_csv(filename):
    try:
        conn = get_connection()
        cur = conn.cursor()

        with open(filename, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)

            for row in reader:
                username, phone = row

                cur.execute(
                    "INSERT INTO phonebook (username, phone) VALUES (%s, %s);",
                    (username, phone)
                )

        conn.commit()
        print("CSV data inserted successfully.")

        cur.close()
        conn.close()

    except Exception as e:
        print("Error:", e)


def menu():
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Add contact")
        print("2. Show contacts")
        print("3. Update contact")
        print("4. Delete contact")
        print("5. Import from CSV")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter name: ")
            phone = input("Enter phone: ")
            insert_contact(username, phone)

        elif choice == "2":
            show_contacts()

        elif choice == "3":
            username = input("Enter name to update: ")
            new_phone = input("Enter new phone: ")
            update_contact(username, new_phone)

        elif choice == "4":
            username = input("Enter name to delete: ")
            delete_contact(username)

        elif choice == "5":
            insert_from_csv("contacts.csv")

        elif choice == "0":
            print("Goodbye.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()