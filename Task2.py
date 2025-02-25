import re
import json
from datetime import datetime

def load_user_data():
    try:
        with open("C:/Users/MBR/Desktop/user_data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_user_data(user_data):
    with open("C:/Users/MBR/Desktop/user_data.json", "w") as file:
        json.dump(user_data, file)

user_data = load_user_data()

def register():
    while True:
        fname = input("Enter your first name: ")
        lname = input("Enter your last name: ")
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        confirm_password = input("Confirm your password: ")
        mobile = input("Enter your mobile number: ")

        
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            print("Valid email address")
        else:
            print("Invalid email address")
            continue

        
        if len(password) < 8:
            print("Short Password")
            continue
        elif not any(char.isupper() for char in password):
            print("Password should contain at least one uppercase letter")
            continue
        elif not any(char.isdigit() for char in password):
            print("Password should contain at least one digit")
            continue
        else:
            print("Valid Password")

        
        if password != confirm_password:
            print("Password and Confirm Password do not match.")
            continue

        
        mobile_pattern = r"^(\+20|20)(10|11|12|15|16|19)\d{8}$"
        if not re.match(mobile_pattern, mobile):
            print("Invalid Egyptian mobile number!")
            continue
        

        new_user = {
                "first_name": fname,
                "last_name": lname,
                "email": email,
                "password": password,
                "mobile": mobile ,
                "projects": []
        }
    
        user_data.append(new_user)
        save_user_data(user_data)
        print("Registration successful!")
        break

        
    return fname, lname, email, password, confirm_password, mobile
    



def login():
   while True:  
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        for user in user_data:
            if user["email"] == email and user["password"] == password:
                print("Login successful!")
                return  user
        print("Invalid email or password! Please try again.")







def create_project(user):
    while True:
        title = input("Enter project title: ")
        details = input("Enter project details: ")
        total_target = input("Enter total target (EGP): ")
        start_date = input("Enter project start date (YYYY-MM-DD): ")
        end_date = input("Enter project end date (YYYY-MM-DD): ")

        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format! Please use YYYY-MM-DD.")
            continue

        if start_date >= end_date:
            print("Start date must be earlier than end date.")
            continue

        project = {
            "title": title,
            "details": details,
            "total_target": total_target,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }

        user["projects"].append(project)
        save_user_data(user_data)
        print("Project created successfully!")
        break

def view_projects(user):
    print("Projects:")
    if not user["projects"]:
        print("No projects found.")
    else:    
     for project in user["projects"]:
        print(f"Title: {project['title']}")
        print(f"Details: {project['details']}")
        print(f"Total Target: {project['total_target']}")
        print(f"Start Date: {project['start_date']}")
        print(f"End Date: {project['end_date']}")
        print()




def edit_project(user):
    if not user["projects"]:
        print("No projects to edit.")
        return

    print("Select a project to edit:")
    for idx, project in enumerate(user["projects"], 1):
        print(f"{idx}. {project['title']}")

    project_index = int(input("Enter project number to edit: ")) - 1

    if project_index < 0 or project_index >= len(user["projects"]):
        print("Invalid project selection.")
        return

    project = user["projects"][project_index]

    while True:
        print(f"Editing Project: {project['title']}")
        print("Select the field you want to update:")
        print("1. Title")
        print("2. Details")
        print("3. Total Target")
        print("4. Start Date")
        print("5. End Date")
        print("6. Cancel editing")

        field_choice = input("Enter your choice: ")

        if field_choice == "1":
            new_title = input(f"Enter new title (current: {project['title']}): ") or project["title"]
            project["title"] = new_title
        elif field_choice == "2":
            new_details = input(f"Enter new details (current: {project['details']}): ") or project["details"]
            project["details"] = new_details
        elif field_choice == "3":
            new_total_target = input(f"Enter new total target (current: {project['total_target']}): ") or project["total_target"]
            project["total_target"] = new_total_target
        elif field_choice == "4":
            while True:
                start_date = input(f"Enter new start date (current: {project['start_date']}): ") or project["start_date"]
                try:
                    start_date = datetime.strptime(start_date, "%Y-%m-%d")
                    project["start_date"] = start_date.strftime("%Y-%m-%d")
                    break
                except ValueError:
                    print("Invalid date format! Please use YYYY-MM-DD.")
        elif field_choice == "5":
            while True:
                end_date = input(f"Enter new end date (current: {project['end_date']}): ") or project["end_date"]
                try:
                    end_date = datetime.strptime(end_date, "%Y-%m-%d")
                    project["end_date"] = end_date.strftime("%Y-%m-%d")
                    break
                except ValueError:
                    print("Invalid date format! Please use YYYY-MM-DD.")
        elif field_choice == "6":
            print("Canceling editing.")
            break
        else:
            print("Invalid option! Please choose a valid option.")
            continue

        save_user_data(user_data)
        print(f"Project '{project['title']}' updated successfully!")

        # Option to continue editing or exit
        continue_edit = input("Do you want to edit another field? (y/n): ")
        if continue_edit.lower() != 'y':
            break





def delete_project(user):
    if not user["projects"]:
        print("No projects to delete.")
        return

    print("Select a project to delete:")
    for idx, project in enumerate(user["projects"], 1):
        print(f"{idx}. {project['title']}")

    project_index = int(input("Enter project number to delete: ")) - 1

    if project_index < 0 or project_index >= len(user["projects"]):
        print("Invalid project selection.")
        return

    project = user["projects"].pop(project_index)
    save_user_data(user_data)
    print(f"Project '{project['title']}' deleted successfully!")




print("Choose an option from the following:")
print("1-Registration")
print("2-Login")
print("3-Exit")


while True:
    option=int(input("Enter your choice: "))
    if option==1:
        print("Registration") 
       
        register()
    elif option==2:
        print("Login")
        user=login()
        while True:
            print("\nChoose an option:")
            print("1-Create Project")
            print("2-View Projects")
            print("3-Edit Project")
            print("4-Delete Project")
            print("5-Logout")

            project_option = int(input("Enter your choice: "))
            if project_option == 1:
                create_project(user)
            elif project_option == 2:
                view_projects(user)
            elif project_option == 3:
                edit_project(user)
            elif project_option == 4:
                delete_project(user)
            elif project_option == 5:
                  break
           
            else:
                print("Invalid option!")
    elif option==3:
        break    
    else:
        print("Invalid option")





