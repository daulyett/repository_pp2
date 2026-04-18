from connect import connect


#1 FUNCTION: search
def search_pattern(pattern):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


#2 FUNCTION: pagination
def get_paginated(limit, offset):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM get_contacts_paginated(%s, %s)",
        (limit, offset)
    )

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


#3 PROCEDURE: upsert
def upsert(name, phone):
    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL upsert_contact(%s, %s)", (name, phone))

    conn.commit()
    cur.close()
    conn.close()


#4 PROCEDURE: delete
def delete_contact(name=None, phone=None):
    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL delete_contact_proc(%s, %s)", (name, phone))

    conn.commit()
    cur.close()
    conn.close()


#5 MENU
def menu():
    while True:
        print("\nPractice8 Menu:")
        print("1. Search pattern")
        print("2. Pagination")
        print("3. Upsert contact")
        print("4. Delete contact")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            search_pattern(input("Pattern: "))

        elif choice == "2":
            limit = int(input("Limit: "))
            offset = int(input("Offset: "))
            get_paginated(limit, offset)

        elif choice == "3":
            upsert(input("Name: "), input("Phone: "))

        elif choice == "4":
            delete_contact(
                input("Name (or Enter): ") or None,
                input("Phone (or Enter): ") or None
            )

        elif choice == "0":
            break


if __name__ == "__main__":
    menu()