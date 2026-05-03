# main prgram of the project, which will run the whole program
# Author: Stephen Kerr

from db_mysql import connect_to_mysql, get_rooms, search_speaker_by_name, get_company, get_attendees_by_company, add_attendee, get_attendee_by_id
from db_neo4j import connect_to_neo4j, get_connected_attendees, already_connected, add_connection

from colorama import init, Fore # for colored text in the terminal

init(autoreset=True) # initialize colorama


def show_menu():
    print(Fore.CYAN + "-" * 30 )
    print(Fore.CYAN + "Conference Management")
    print(Fore.CYAN + "-" * 30 )
    print(Fore.YELLOW + "\nMENU")
    print(Fore.YELLOW + "=" * 20)
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
                print(Fore.RED + "No speakers found of that name.")

                        
            input("\nPress Enter to continue...")

        elif choice == '2':
            # View Attendees by Company
            company_id = input("Enter company ID: ").strip()

            # check if company ID is positive integer
            if not company_id.isnumeric() or int(company_id) <=1:
                print(Fore.RED + "*** ERROR *** Invalid Company ID")
                continue
            companies = get_company(mysql_conn, company_id)
            if not companies:
                print(Fore.RED + f"Company with ID {company_id} doesn't exist.")
                continue
            print(f"{companies[1]} Attendees")
            attendees = get_attendees_by_company(mysql_conn, company_id)
            if attendees:
                print("Attendee Name | Attendee DOB | Session Title | Speaker Name | Room Name")
                print("-" * 80)
                for attendee in attendees:
                    print(f"{attendee[0]} | {attendee[1]} | {attendee[2]} | {attendee[3]} | {attendee[4]}")
            else:
                print(Fore.RED + f"No attendees found for {companies[1]}.")
            
            input("\nPress Enter to continue...")

        elif choice == '3':
            # Add New Attendees
            print("Add New Attendee")
            print("-" * 20)
            attendee_id = input("Enter Attendee ID: ").strip()
            name = input("Enter Attendee Name: ").strip()
            dob = input("Enter Attendee DOB (YYYY-MM-DD): ").strip()
            gender = input("Enter Attendee Gender (Male/Female): ").strip()
            company_id = input("Enter Attendee Company ID: ").strip()

            add_attendee(mysql_conn, attendee_id, name, dob, gender, company_id)

            input("\nPress Enter to continue...")   

            
        elif choice == '4':
            # View Connected Attendees
            while True:
                attendee_id = input("Enter Attendee ID to view connections: ").strip()

                # check if the id is a positive integer
                if not attendee_id.isnumeric() or int(attendee_id) <= 0:
                    print(Fore.RED + "*** ERROR *** Invalid Attendee ID")
                    continue

                attendee = get_attendee_by_id(mysql_conn, attendee_id)

                # check if attendee exists
                if not attendee:
                    print(Fore.RED + f"Attendee with ID {attendee_id} doesn't exist.")
                    break

                print(f"Attendee Name: {attendee[0]}")
                print("-" * 30)

                connected_attendees = get_connected_attendees(neo4j_driver, int(attendee_id))

                if not connected_attendees:
                    print(Fore.RED + "No connections.")
                else:
                    print("These attendees are connected:")
                    for cid in connected_attendees:
                        # need to get the name of the connected id using the mysql databases and the function get_attendee_by_id
                        connected_attendee = get_attendee_by_id(mysql_conn, cid)
                        if connected_attendee:
                            print(f"{cid} | {connected_attendee[0]}")
                        
                input("\nPress Enter to continue...")
                break

        elif choice == '5':
            # Add Attendee Connection
            while True: 
                id1 = input("Enter first Attendee ID: ").strip()
                id2 = input("Enter second Attendee ID: ").strip()

                # check if the ids are positive integers
                if not id1.isnumeric() or not id2.isnumeric():
                    print(Fore.RED + "*** ERROR *** Attendee IDs must be numbers")
                    continue


                id1, id2 = int(id1), int(id2)

                # check if the ids are the same
                if id1 == id2:
                    print(Fore.RED + "*** ERROR *** AN Attendee cannot connect to him/herself")
                    continue

                # check if both attendees exist in the mysql database
                attendee1 = get_attendee_by_id(mysql_conn, id1)
                attendee2 = get_attendee_by_id(mysql_conn, id2)

                if not attendee1 or not attendee2:
                    print(Fore.RED + "*** ERROR *** One or Both Attendee IDs do not exist")
                    continue

                #check if the connection already exists in the neo4j database
                if already_connected(neo4j_driver, id1, id2):
                    print(Fore.RED + "*** ERROR *** These attendees are already connected")
                    continue

                # add the connection to the neo4j database
                add_connection(neo4j_driver, id1, id2)
                print(Fore.GREEN + f"Attendee {id1} is now connected to Attendee {id2}")

                input("\nPress Enter to continue...")
                break

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
