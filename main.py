# main prgram of the project, which will run the whole program
# Author: Stephen Kerr

from db_mysql import connect_to_mysql, get_rooms, search_speaker_by_name, get_company, get_attendees_by_company
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
            # View Speakers & Sessions
            speaker_name = input("Enter speaker name (or part of the name) : ").strip()

            print(f"\nSession Details For : {speaker_name}")

            speakers = search_speaker_by_name(mysql_conn, speaker_name)
            if speakers:
                print("Speaker Name | Session Title | Room Name")
                print("-" * 50)
                for speaker in speakers:
                    print(f"{speaker[0]} | {speaker[1]} | {speaker[2]}")
            else:
                print("No speakers found of that name.")

                        
            input("\nPress Enter to continue...")

        elif choice == '2':
            # View Attendees by Company
            company_id = input("Enter company ID: ").strip()

            # check if company ID is positive integer
            if not company_id.isnumeric() or int(company_id) <=1:
                print("*** ERROR *** Invalid Company ID")
                continue
            companies = get_company(mysql_conn, company_id)
            if not companies:
                print(f"Company with ID {company_id} doesn't exist.")
                continue
            print(f"{companies[1]} Attendees")
            attendees = get_attendees_by_company(mysql_conn, company_id)
            if attendees:
                print("Attendee Name | Attendee DOB | Session Title | Speaker Name | Room Name")
                print("-" * 80)
                for attendee in attendees:
                    print(f"{attendee[0]} | {attendee[1]} | {attendee[2]} | {attendee[3]} | {attendee[4]}")
            else:
                print(f"No attendees found for {companies[1]}.")
            
            input("\nPress Enter to continue...")

        elif choice == '3':
            pass
        elif choice == '4':
            pass
        elif choice == '5':
            pass

        elif choice == '6':
            # View Rooms
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
