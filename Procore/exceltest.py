import pandas as pd
import json
import os
from pprint import pprint
from getRoles import projectID

# Define file paths
script_dir = os.path.dirname(__file__)  # Current script directory
projects_file = os.path.join(script_dir, "projects.json")
roles_file = os.path.join(script_dir, "roles.json")
excel_file = os.path.join(script_dir, "projects.xlsx")

# -----------------------------
# Process projects.json
# -----------------------------
with open(projects_file, "r", encoding="utf-8") as file:
    projects_data = json.load(file)

# Extract nested fields for projects
projects_processed = []
for project in projects_data:
    projects_processed.append({
        "id": project.get("id"),
        "project_name": project.get("name"),
        "active": project.get("active"),
        "company_name": project.get("company", {}).get("name")  # Extract nested field
    })

# Convert projects to DataFrame
df_projects = pd.DataFrame(projects_processed)
pprint(projects_processed)

# -----------------------------
# Process roles.json and inject projectID
# -----------------------------
with open(roles_file, "r", encoding="utf-8") as file:
    roles_data = json.load(file)

# Inject the project ID into each role entry
for role in roles_data:
    role["project_id"] = projectID

# Optionally, write the updated data back to the JSON file
with open("roles.json", "w", encoding="utf-8") as file:
    json.dump(roles_data, file, indent=2)

# Extract fields for roles DataFrame
roles_processed = []
for role in roles_data:
    roles_processed.append({
        "project_id": role.get("project_id"),
        "name": role.get("name"),
        "role": role.get("role")
    })

# Convert roles to DataFrame
df_roles = pd.DataFrame(roles_processed)
pprint(roles_processed)

# Convert roles 'project_id' to integer (if not already)
df_roles['project_id'] = df_roles['project_id'].astype(int)

# -----------------------------
# Merge DataFrames
# -----------------------------
# Merge projects and roles using projects 'id' and roles 'project_id'
df_combined = pd.merge(df_projects, df_roles, left_on="id", right_on="project_id", how="inner")

# Rename columns for clarity
df_combined = df_combined.rename(columns={
    "company_name": "Company Name",
    "id": "Job Number",
    "project_name": "Project Name",
    "name": "Name",
    "role": "Job Title",
    "active": "Is Active"
})

# -----------------------------
# Group by project and aggregate roles conditionally
# -----------------------------
# Define the grouping columns (each unique project)
group_cols = ["Job Number", "Project Name", "Company Name", "Is Active"]

# Function to extract names for a specific role within a group
def aggregate_role(group, role):
    names = group.loc[group["Job Title"] == role, "Name"]
    # Return a comma-separated string of unique names for this role
    return ", ".join(names.unique()) if not names.empty else ""

# Group and create new columns for the roles of interest
df_grouped = df_combined.groupby(group_cols).apply(lambda group: pd.Series({
    "Architect": aggregate_role(group, "Architect"),
    "Project Manager": aggregate_role(group, "Project Manager"),
    "Superintendent": aggregate_role(group, "Superintendent")
})).reset_index()


# Export to Excel
df_grouped.to_excel(excel_file, index=False, engine="openpyxl")
print(f"✅ Data successfully saved to {excel_file}")
