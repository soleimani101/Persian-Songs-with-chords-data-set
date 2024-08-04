import requests
from bs4 import BeautifulSoup
import re
import os

def scrape_url(url):
    # Make a request to the webpage
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the <pre> element with the specific id
        pre_tag = soup.find('pre', {'id': 'main-chord'})
        
        if pre_tag:
            # Extract the text content from the <pre> tag
            content = pre_tag.get_text()

            # Remove all '*' characters
            content = content.replace('*', '')

            # Split text by lines to keep original structure
            text_lines = content.split('\n')

            # Regex pattern for chords
            chord_pattern = re.compile(r'[A-Ga-g][#b]?m?7?|[A-Ga-g]maj7?|[A-Ga-g]7?|[A-Ga-g]sus2?|[A-Ga-g]sus4?|[A-Ga-g]add9?|[A-Ga-g]dim?|[A-Ga-g]aug?|[A-Ga-g]7sus4?')

            # Collect the content
            
            collected_content = '<[SOP]>\n'  # Start tag for the main content
            collected_content += '<[RHYTHM]>\n6/8S\n<[RHYTHM]>\n'  # Add rhythm tag

            for line in text_lines:
                if line.strip():  # Only process non-empty lines
                    chords = chord_pattern.findall(line)
                    lyrics = re.sub(chord_pattern, '', line).strip()
                    
                    # Collect chords with tags
                    if chords:
                        collected_content += '<[SOC]>\n'
                        collected_content += ' '.join(chords).strip() + '\n'
                        collected_content += '<[EOC]>\n'
                    
                    # Collect lyrics with tags
                    if lyrics:
                        collected_content += '<[SOB]>\n'
                        collected_content += lyrics + '\n'
                        collected_content += '<[EOB]>\n'
            
            collected_content += '<[EOP]>\n'  # End tag
            
            return collected_content
        else:
            print(f"Could not find the <pre> tag with id 'main-chord' for URL: {url}")
            return ''
    else:
        print(f"Failed to retrieve the webpage for URL: {url}. Status code: {response.status_code}")
        return ''

def process_urls(input_file, output_file):
    # Read URLs from the input file
    with open(input_file, 'r') as file:
        urls = [line.strip() for line in file if line.strip()]

    # Open the output file for writing
    with open(output_file, 'w', encoding='utf-8') as file:
        # Process each URL
        for index, url in enumerate(urls):
            try:
                print(f"Processing URL:{input_file} {index + 1} / {len(urls)}")
                content = scrape_url(url)  # Scrape the content of the URL
                file.write(content)  # Write the content to the file
            except Exception as e:
                print(f"Error processing URL {url}: {e}")
    
    print(f"All poems have been scraped and saved to '{output_file}'.")

# Specify the input file with URLs and the final output file
input_file = 'urlfolder/extracted_urls_heavy68.txt'  # Change this to the name of your file containing URLs
output_file = 'database/final_scraped_poems_68_heavy.txt'  # Output file name

# Process the URLs and save the combined content
process_urls(input_file, output_file)
