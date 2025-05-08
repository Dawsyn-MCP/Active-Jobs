import json
import os

file_path = os.path.join(os.path.join("Procore", "projects.json"))

with open(file_path, 'r') as file:
    data = json.load(file) 

def header_print():
    #Printing header
    print("=" * 80)
    print(f"{'ID':<10} {'Name':<25} {'Status':<15} {'Company Name':<15} {'Company ID':<15}")
    print("=" * 80)

#Project Class
class Project:
    def __init__(self, project_id, name, status, company_name, company_id):
        self.project_id = project_id
        self.name = name
        self.status = status
        self.company_name = company_name
        self.company_id = company_id

    def display_info(self):
        #Printing project details
        print(f"{self.project_id:<10} {self.name:<25} {self.status:<15} {self.company_name:<15} {self.company_id:<15}")

        #printing spaces between objects
        print('\n')


# Convert JSON data to objects
projects = [Project(d["id"], d["name"], d["active"], d["company"]["name"], d["company"]["id"]) for d in data]

# Display header
header_print()

# Display project details
for project in projects:
    project.display_info()

