import os
import sys
import glob
import requests
import json

def check_plagiarism(file_path, api_key):
    with open(file_path, 'r') as file:
        content = file.read()

    headers = {
        'apikey': api_key,
        'Content-Type': 'application/json'
    }

    data = {
        'base64': content.encode('utf-8').decode('utf-8')
    }

    response = requests.post('https://api.copyleaks.com/v3/businesses/submit/url',
                             headers=headers, data=json.dumps(data))

    if response.status_code != 200:
        print(f'Error checking plagiarism for {file_path}: {response.text}')
        return False

    result = response.json()
    return result['found']

def main():
    api_key = os.environ['COPYLEAKS_API_KEY']
    md_files = glob.glob('**/*.mdx', recursive=True)

    plagiarism_found = False

    for md_file in md_files:
        if check_plagiarism(md_file, api_key):
            print(f'Plagiarism detected in {md_file}')
            plagiarism_found = True

    if plagiarism_found:
        print('Plagiarism check failed. Please review the flagged files.')
        sys.exit(1)
    else:
        print('No plagiarism detected.')

if __name__ == '__main__':
    main()