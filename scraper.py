from playwright.sync_api import sync_playwright
import pandas as pd
import time

def scrape():
    # Create an Excel writer with append mode
    filename = "Faculty_Academic_Interests.xlsx"

    # Create an empty DataFrame and save to Excel if the file doesn't exist
    if not pd.io.common.file_exists(filename):
        df = pd.DataFrame(columns=["Name", "Profile Link", "All Text"])
        df.to_excel(filename, index=False)

    with sync_playwright() as p:
        # Launch Chromium browser in headless mode
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Open the faculty page you want to scrape
        print("Navigating to the faculty list page...")
        page.goto("https://www.torontomu.ca/engineering-architectural-science/about/faculty-search/")
        page.wait_for_selector("a.name", timeout=10000)  # Wait for faculty links to appear (timeout is 10 seconds)

        # Find faculty name links on the page
        faculty_links = page.locator("a.name")
        names = faculty_links.all_inner_texts()  # Extract names
        hrefs = faculty_links.evaluate_all("els => els.map(el => el.href)")  # Extract links to profiles

        print(f"Found {len(names)} faculty members!")

        # Scrape all text from the individual profile pages
        data = []
        for name, link in zip(names, hrefs):
            try:
                print(f"Scraping profile of {name}...")
                prof_page = browser.new_page()
                prof_page.goto(link)
                prof_page.wait_for_load_state('domcontentloaded')  # Ensure the page loads completely before proceeding

                # Extract all text from the profile page
                all_text = prof_page.inner_text("body")  # Extract all text in the body

                # Add the data for this professor and append it to the Excel file
                new_entry = pd.DataFrame([[name, link, all_text]], columns=["Name", "Profile Link", "All Text"])

                # Append to the Excel file
                with pd.ExcelWriter(filename, mode="a", if_sheet_exists="overlay", engine="openpyxl") as writer:
                    new_entry.to_excel(writer, index=False, header=False, startrow=writer.sheets["Sheet1"].max_row)

                print(f"Saved data for {name} to Excel.")

                prof_page.close()
            except Exception as e:
                print(f"Error while processing {name}: {e}")
        
        # Close the browser
        browser.close()
        print(f"Scraping completed. Data saved to {filename}.")

if __name__ == "__main__":
    scrape()
