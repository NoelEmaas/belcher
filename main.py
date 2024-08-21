import json
import pandas as pd
import os


def load_sites(file_path):
    with open(file_path, 'r') as file:
        sites = json.load(file)
    return sites


def display_sites(sites):
    print("Select a site to scrape:")
    for index, site in enumerate(sites):
        print(f"{index + 1}. {site['name']}")


def get_user_choice(sites):
    display_sites(sites)
    choice = int(input("Enter the number of the site you want to scrape: ")) - 1
    if 0 <= choice < len(sites):
        return sites[choice]
    else:
        print("Invalid choice. Please try again.")
        return get_user_choice(sites)


def main():
    sites = load_sites('sites.json')
    selected_site = get_user_choice(sites)
    print(f"You selected: {selected_site['name']} with link: {selected_site['link']}")
    print("Scraping ...\n")

    if selected_site['name'] == "Internation Conference Alerts":
        from scripts.international_conference_alerts import scrape
        data = scrape()
    elif selected_site['name'] == "Dev.Events":
        from scripts.dev_events import scrape
        data = scrape()
    elif selected_site['name'] == "Hackathon":
        from scripts.hackathon import scrape
        data = scrape()
    elif selected_site['name'] == "e27":
        from scripts.e27 import get_events
        data = get_events()
    elif selected_site['name'] == "EventBrite":
        from scripts.event_brite import scrape
        data = scrape()
    elif selected_site['name'] == "10Times":
        from scripts.ten_times import scrape
        data = scrape()
    else:
        print("No scraping function available for the selected site.")
        data = None

    if data:
        output_dir = 'outputs'
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, "scraped_data.xlsx")
        
        with pd.ExcelWriter(file_path, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
            df = pd.DataFrame(data)
            df.to_excel(writer, sheet_name=selected_site['name'], index=False)

        print("Data has been saved to an excel file.")


if __name__ == "__main__":
  main()