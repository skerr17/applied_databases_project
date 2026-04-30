# main prgram of the project, which will run the whole program
# Author: Stephen Kerr

from db_mysql import connect_to_mysql
from db_neo4j import connect_to_neo4j

def show_menu():
    print("Conference Management")
    print("-" * 30 )
    print("\nMENU")
    print("=" * 20)
    print("1 - View Speakers & Sessions")
    print("2 - View Attendees by Company")
    print("3 - Add New Attendees")
    print("4 - View Connected Attendees")
    print("5 - Add Attendee Connection")
    print("6 - View Rooms")
    print("x - Exit Application")


def main():
    while True:
        show_menu()
        choice = input("Choice: ").strip()

        if choice == '1':
            pass
        elif choice == '2':
            pass
        elif choice == '3':
            pass
        elif choice == '4':
            pass
        elif choice == '5':
            pass
        elif choice == '6':
            pass
        elif choice == 'x':
            print("Exiting application")
            break
        else:
            print("Invalid choice, please try again")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()
