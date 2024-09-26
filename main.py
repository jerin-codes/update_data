import tabula
import requests
import json
import pycountry
import re

def get_teamID(team):
    if team == "Kannur Warriors FC" or team == "Kannur Warriors" or team== "Kannur":
        return 27
    elif team == " KOCHI FORCA FC" or team=="KOCHI FORCA" or team=="KOCHI":
        return 20
    elif team == "Calicut FC" or team =="Calicut":
        return 22
    elif team == "THIRUVANANTHAPURAM KOMBANS" or team =="THIRUVANANTHAPURAM":
        return 24
    elif team == "Malappuram Football Club" or team=="Malappuram Football" or team =="Malappuram":
        return 21
    elif team == "Thrissur Magic FC" or team =="Thrissur Magic" or team =="Thrissur":
        return 25
    else:
        print("Hello world,",team)
def get_country(country):
     try:
        if pycountry.countries.lookup(country):
            return country
     except LookupError:
        return "India"


def process_pdf_and_send_to_api_team1(pdf_path, team_name,index_one,index_two):
    
    
    tables = tabula.read_pdf(pdf_path, pages="all", multiple_tables=True)
    
    print(f"Number of tables extracted: {len(tables)}")
    for i, table in enumerate(tables):
        if(i+1)==1:
             team_1 = table.iloc[1]["Match"].split("\r")[0].strip()  # Extract team 1 name
             team_2 = table.iloc[1]["Attendance"].split("\r")[0].strip()  # Extract team 2 name

       
             print(f"Team 1: {team_1}")
             print(f"Team 2: {team_2}")

        if index_one == 2 and index_two==4:
            original_team_name=team_1
        elif index_one == 3 and index_two==5:
            original_team_name=team_2

    structured_data = []
    #print(tables)

   
    for i, table in enumerate(tables):
        country_lit=[]
        if (i + 1) == index_one or (i + 1) == index_two:
            print(f"\nExtracting data from Table {i + 1}:")
            print(table)
            table = table[['No', 'Pos', 'Name']].dropna()
            team_id=get_teamID(original_team_name)
            for index, row in table.iterrows():
                 match = re.search(r'\((.*?)\)', row['Name'])
                 bracket_content = match.group(1).strip()
                 print("First data is",bracket_content)
                 temp_country=get_country(bracket_content)
                 country_lit.append(temp_country)
                 
            for index, row in table.iterrows():
               
                player_data = {
                    "team_id": team_id, 
                    "jersey_number": int(row["No"]),
                    "correct_player_name": row["Name"].split('(')[0].strip(),
                    "position_actual": row["Pos"],
                    "photo": "/asset/.jpg",  
                    "country": country_lit[index],  
                }
                structured_data.append(player_data)

    # Send data to the API
    url = "http://20.193.132.108:8004/api/update_slk_players"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Cookie": "XSRF-TOKEN=eyJpdiI6ImNrbEdxczZXYURSRU84NkZvT3ZpMWc9PSIsInZhbHVlIjoiR3BOOXpLZHc3R21jdHk2VE05TE9McDdreDNrai9QK203UVI0VHRsL2g2ZEFmZGRXNmVDUEJIZzNzSWtsWko2SWJtQjBycE52dERIVldyYUJMVzZQd0U1SjV0ODB4K0FWTkthUVVKVU1odURoZmI5RG5GNXVBUllmTDNMTWFXeUMiLCJtYWMiOiIyYjk0NGMwMDM5MDcyOWYyZmJmM2MzM2Y0MTVjZGY3NmM3NGEzZTEyZWI5NjU2NjY0NWYzNTllM2ExZDc3NDc3IiwidGFnIjoiIn0%3D; laravel_session=eyJpdiI6IjJObThFaHhjcDI1dHNIK0RDcXhNVWc9PSIsInZhbHVlIjoiS2h6bklVWjVSWnh4SjBiK1ZUY0I4Ty9BZDdvWExkVXQ5N0x6anZOeTJxQWVzb1FPMUFTdW40d2RCK3YyZmZXK3lWNEMwWE1kTnpvRUFkQUVYRzVOM1llaUhjNnBGOGhxUFUxS29RWTFRYjBTK05JWElVUGxXQW1WMjBYM1lSNmUiLCJtYWMiOiI2ZjgwMmVlYzgyMGY3MWFhZjc2MmVlOTZhZGI2N2RlYzI1ODhkZmMzYTc3YWNkOGE4MDkwN2I0N2FlYjI5NDE4IiwidGFnIjoiIn0%3D"
    }

    for player in structured_data:
        print(player)
        try:
            response = requests.post(url, json=player, headers=headers)
            if response.status_code == 200:
                print("Updated successfully")
            else:
           
                print("Something went wrong")
        except requests.exceptions.RequestException as e:
            print(f"Error sending data for jersey number {player['jersey_number']}: {e}")

# Example usage
process_pdf_and_send_to_api_team1(pdf_path="malappuram vs calicut.pdf",team_name="Kannur Warriors FC",index_one=2,index_two=4)#Scraping the first team players details from the pdf
process_pdf_and_send_to_api_team1(pdf_path="malappuram vs calicut.pdf",team_name="Kannur Warriors FC",index_one=3,index_two=5)#Scraping the secong team players details from the pdf
