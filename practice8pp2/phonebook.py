from connect import get_connection


def search_contacts(pattern):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM search_contacts(%s);", (pattern,))
        rows = cur.fetchall()

        print("\nSearch results:")
        for row in rows:
            print(row)

        cur.close()
        conn.close()

    except Exception as e:
        print("Error:", e)


def get_contacts_page(limit, offset):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM get_contacts_page(%s, %s);", (limit, offset))
        rows = cur.fetchall()

        print("\nPage results:")
        for row in rows:
            print(row)

        cur.close()
        conn.close()

    except Exception as e:
        print("Error:", e)


def upsert_contact(username, phone):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("CALL upsert_contact(%s, %s);", (username, phone))
        conn.commit()

        print("Upsert completed successfully.")

        cur.close()
        conn.close()

    except Exception as e:
        print("Error:", e)


def insert_many_contacts(usernames, phones):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("CALL insert_many_contacts(%s, %s);", (usernames, phones))
        conn.commit()

        print("Bulk insert completed successfully.")

        cur.close()
        conn.close()

    except Exception as e:
        print("Error:", e)


def delete_contact(value):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("CALL delete_contact(%s);", (value,))
        conn.commit()

        print("Delete completed successfully.")

        cur.close()
        conn.close()

    except Exception as e:
        print("Error:", e)


def menu():
    while True:
        print("\n--- PRACTICE 8 MENU ---")
        print("1. Search contacts by pattern")
        print("2. Upsert contact")
        print("3. Insert many contacts")
        print("4. Get contacts with pagination")
        print("5. Delete contact by username or phone")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            pattern = input("Enter search pattern: ")
            search_contacts(pattern)

        elif choice == "2":
            username = input("Enter username: ")
            phone = input("Enter phone: ")
            upsert_contact(username, phone)

        elif choice == "3":
            names_input = input("Enter usernames separated by comma: ")
            phones_input = input("Enter phones separated by comma: ")

            usernames = [name.strip() for name in names_input.split(",")]
            phones = [phone.strip() for phone in phones_input.split(",")]

            insert_many_contacts(usernames, phones)

        elif choice == "4":
            limit = int(input("Enter limit: "))
            offset = int(input("Enter offset: "))
            get_contacts_page(limit, offset)

        elif choice == "5":
            value = input("Enter username or phone to delete: ")
            delete_contact(value)

        elif choice == "0":
            print("Goodbye.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()