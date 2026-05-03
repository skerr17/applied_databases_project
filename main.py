# main prgram of the project, which will run the Conference Management CLI app
# It will connect to both the mysql and neo4j databases 
# and provide a menu for the user to interact with the data
# # Author: Stephen Kerr

from db_mysql import connect_to_mysql, get_rooms, search_speaker_by_name, get_company, get_attendees_by_company, add_attendee, get_attendee_by_id, get_stats, get_agenda
from db_neo4j import connect_to_neo4j, get_connected_attendees, already_connected, add_connection, get_most_connected, get_friends_of_friends

from colorama import init, Fore # for colored text in the terminal see documentation for colorama for more details https://pypi.org/project/colorama/

from tabulate import tabulate # for printing tables in the terminal see documentation for tabulate for more details https://pypi.org/project/tabulate/

from export import export_to_csv # for exporting data to csv file see export.py for more details

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
    print("7 - Conference Statistics Dashboard")
    print("8 - View Conference Agenda")
    print("x - Exit Application")


def main():

    # Connect to databases
    mysql_conn = connect_to_mysql()
    neo4j_driver = connect_to_neo4j()

    # rooms cache
    rooms_cache = None

    while True:
        show_menu()
        choice = input("Choice: ").strip()

        if choice == '1':
            # View Speakers & Sessions
            speaker_name = input("Enter speaker name (or part of the name) : ").strip()

            print(f"\nSession Details For : {speaker_name}")

            speakers = search_speaker_by_name(mysql_conn, speaker_name)
            if speakers:
                print(Fore.CYAN + tabulate(
                    speakers,
                    headers=["Speaker Name", "Session Title", "Room Name"],
                    tablefmt="rounded_grid"
                ))
                
                # export option
                export = input("Export to CSV? (y/n): ").strip().lower()
                if export == "y":
                    export_to_csv(
                        f"speaker_sessions_{speaker_name.replace(' ', '_')}",
                        ["Speaker Name", "Session Title", "Room Name"],
                        speakers
                        )
            else:
                print(Fore.RED + "No speakers found of that name.")



                        
            input("\nPress Enter to continue...")

        elif choice == '2':
            # View Attendees by Company
            while True:
                company_id = input("Enter company ID: ").strip()

                # check if company ID is positive integer
                if not company_id.isnumeric() or int(company_id) <= 0:
                    print(Fore.RED + "*** ERROR *** Invalid Company ID")
                    continue

                companies = get_company(mysql_conn, company_id)
                if not companies:
                    print(Fore.RED + f"Company with ID {company_id} doesn't exist.")
                    continue

                print(f"{companies[1]} Attendees")
                attendees = get_attendees_by_company(mysql_conn, company_id)
                if attendees:
                    print(Fore.CYAN + tabulate(
                        attendees,
                        headers=["Attendee Name", "DOB", "Session Title", "Speaker Name", "Room Name"],
                        tablefmt="rounded_grid"
                    ))

                    # export option 
                    export = input("Export to CSV? (y/n): ").strip().lower()
                    if export == "y":
                        export_to_csv(
                            f"company_{company_id}_attendees",
                            ["Attendee Name", "DOB", "Session Title", "Speaker", "Room"],
                            attendees
                        )
                
                else:
                    print(Fore.RED + f"No attendees found for {companies[1]}.")
                

                input("\nPress Enter to continue...")
                break

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
                    continue

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

                    
                    # friends of friends (2nd degree connections)
                    fof_choice = input("\nView friends of friends (2nd degree connections)? (y/n): ").strip().lower()

                    if fof_choice == "y":
                        print("\nFriend of Friends:")
                        print("-" * 30)
                        fof_data = get_friends_of_friends(neo4j_driver, int(attendee_id), connected_attendees)
                        
                        # check if there are any friends of friends connections
                        if not fof_data:
                            print(Fore.RED + "No friends of friends connections.")
                        else:
                            for cid, fof_ids in fof_data.items():
                                connected_attendee = get_attendee_by_id(mysql_conn, cid)
                                if connected_attendee:
                                    print(f"{connected_attendee[0]}:")
                                    for fid in fof_ids:
                                        fof = get_attendee_by_id(mysql_conn, fid)
                                        if fof:
                                            print(f"  └── {fid} | {fof[0]}")
                             
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
                    print(Fore.RED + "*** ERROR *** An Attendee cannot connect to him/herself")
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
            if rooms_cache is None:
                rooms = get_rooms(mysql_conn)
                rooms_cache = rooms
            
            print(Fore.CYAN + tabulate(
                rooms_cache,
                headers=["RoomID", "RoomName", "Capacity"],
                tablefmt="rounded_grid"
                ))
            
            # export option
            export = input("Export to CSV? (y/n): ").strip().lower()
            if export == "y":
                export_to_csv(
                    "conference_rooms",
                    ["RoomID", "RoomName", "Capacity"],
                    rooms_cache
                )
            
            input("\nPress Enter to continue...")


        elif choice == '7':
            # Stats Dasboard
            stats = get_stats(mysql_conn)
            most_connected =  get_most_connected(neo4j_driver)


            # default most_connected_name to N/A in the case there are no connections in the database to avoid errors when trying to access the mysql database with a None value
            most_connected_name = "N/A"

            # get most connected attendee name from mysql database using the id from neo4j
            if most_connected:
                most_connected_attendee = get_attendee_by_id(mysql_conn, most_connected[0])
                most_connected_name = most_connected_attendee[0] if most_connected_attendee else "Unknown"

            stats_data = [
                ["Total Attendees", stats["total_attendees"]],
                ["Total Registrations", stats["total_registrations"]],
                ["Total Companies", stats["total_companies"]],
                ["Total Sessions", stats["total_sessions"]],
                ["Most Connected Attendee", f"{most_connected_name} (ID: {most_connected[0]}) with {most_connected[1]} connections" if most_connected else "N/A"],
                ["Most Popular Session", stats["popular_session"]],
            ]

            print(Fore.CYAN + "\n" + "=" * 30)
            print(Fore.CYAN + "Conference Statistics Dashboard")
            print(Fore.CYAN + "=" * 30)

            print(Fore.CYAN + 
            tabulate(
                stats_data, 
                headers=["Statistic", "Value"], 
                tablefmt="rounded_grid"
                ))
            
            input("Press Enter to continue...")
            

        elif choice == '8':
            # View conference agenda
            agenda = get_agenda(mysql_conn)

            print(Fore.CYAN + "\n" + "=" * 30)
            print(Fore.CYAN + "Conference Agenda")
            print(Fore.CYAN + "=" * 30)
            
            print(Fore.CYAN + tabulate(
                agenda,
                headers=["Date", "Room Name", "Session Title", "Speaker Name"],
                tablefmt="rounded_grid"
            ))
            #export option
            export = input("Export to CSV? (y/n): ").strip().lower()
            if export == "y":
                export_to_csv(
                    "conference_agenda",
                    ["Date", "Room Name", "Session Title", "Speaker Name"],
                    agenda
                )
            
            input("Press Enter to continue...")


        elif choice == 'x':
            print("Exiting application")
            break
        else:
            print("Invalid choice, please try again")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
