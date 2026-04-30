# main prgram of the project, which will run the whole program
# Author: Stephen Kerr

from db_mysql import connect_to_mysql, get_rooms
from db_neo4j import connect_to_neo4j

def show_menu():
    print("-" * 30 )
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

    # Connect to databases
    mysql_conn = connect_to_mysql()
    neo4j_driver = connect_to_neo4j()

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
            rooms = get_rooms(mysql_conn)
            print("RoomID | RoomName | Capacity")
            print("-" * 30)
            for room in rooms:
                print(f"{room[0]} | {room[1]} | {room[2]}")
            
            input("\nPress Enter to continue...")


        elif choice == 'x':
            print("Exiting application")
            break
        else:
            print("Invalid choice, please try again")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()
