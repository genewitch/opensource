import sys
import os
import random
from bs4 import BeautifulSoup
from datetime import datetime

def process_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        html = file.read()
    
    soup = BeautifulSoup(html, "html.parser")
    messages = []
    current_date = None
    last_username = None  # Track the last known username
    username_padding = 0  # Track the length of the last username for alignment

    # Iterate through all elements in the message list.
    for element in soup.find_all(["div", "li"]):
        # Check for date separator.
        date_tag = element.find("h2", class_="mx_DateSeparator_dateHeading")
        if date_tag:
            # Parse and reformat the date into YYYY/MM/DD.
            raw_date = date_tag.get_text(strip=True)
            current_date = datetime.strptime(raw_date, "%a, %b %d, %Y").strftime("%Y/%m/%d")
            continue

        # Process message wrappers.
        if "mx_Export_EventWrapper" in element.get("class", []):
            # Extract username.
            username_tag = element.find("span", class_="mx_DisambiguatedProfile_displayName")
            if username_tag:
                last_username = username_tag.get_text(strip=True)
                username_padding = len(last_username)  # Update padding based on username length
                username = f"{last_username}:"
            else:
                # Align the `|` with spaces based on the last username's padding.
                username = " " * (username_padding) + "|"

            # Extract timestamp.
            timestamp_tag = element.find("span", class_="mx_MessageTimestamp")
            timestamp = timestamp_tag.get_text(strip=True) if timestamp_tag else "Unknown"

            # Extract message body.
            message_tag = element.find("div", class_="mx_EventTile_body")
            message = message_tag.get_text(strip=True) if message_tag else "No message"

            # Combine the date and time into a sortable format.
            if current_date:
                full_timestamp = f"{current_date} {timestamp}"
            else:
                full_timestamp = timestamp  # Fallback if no date is set.

            # Store the result.
            messages.append(f"{full_timestamp} {username} {message}")

    # Generate output filename with random 4 hex digits.
    output_filename = f"{os.path.splitext(filename)[0]}_out_x{random.randint(0x1000, 0xFFFF):04X}.dat"
    with open(output_filename, "w", encoding="utf-8") as output_file:
        output_file.write("\n".join(messages))
    print(f"Processed: {filename} -> {output_filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <filename>")
        sys.exit(1)
    
    process_file(sys.argv[1])
