import os
import csv
import json
from bs4 import BeautifulSoup

def extract_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        main_copy = soup.find('div', id='main-copy')
        content = []
        if main_copy:
            paragraphs = main_copy.find_all('p')
            for p in paragraphs:
                spans = p.find_all('span')
                if len(spans) >= 3:
                    title = spans[0].get_text(strip=True)
                    date = spans[1].get_text(strip=True)
                    # Remove the duplicated text and keep only the unique content
                    full_text = p.get_text(separator=" ", strip=True)
                    comments = full_text.replace(title, "").replace(date, "").replace("(comments)", "").strip()
                    content.append((title, date, comments))
        return content

def write_csv(output_path, data):
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Title', 'Date', 'Comments'])
        writer.writerows(data)

def write_json(output_path, data):
    with open(output_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=4)

def main(directory, output_format='csv'):
    all_content = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file == 'index.html':
                file_path = os.path.join(root, file)
                content = extract_content(file_path)
                all_content.extend(content)
    output_path = f'output.{output_format}'
    if output_format == 'csv':
        write_csv(output_path, all_content)
    elif output_format == 'json':
        write_json(output_path, all_content)

# Run the main function without if __name__ == '__main__':
main(r'd:\tmp\inputs', output_format='json')
