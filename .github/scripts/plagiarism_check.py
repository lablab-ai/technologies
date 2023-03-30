import glob
import json
import os
import sys

import requests


class PlagiarismChecker:
    def __init__(self, api_key):
        self.api_key = api_key

        self.headers = {"apikey": api_key, "Content-Type": "application/json"}
        self.base_url = "https://api.copyleaks.com/v3/businesses/submit/url"

    def check_plagiarism(self, file_path):
        with open(file_path, "r") as file:
            content = file.read()

        data = {"base64": content.encode("utf-8").decode("utf-8")}

        response = requests.post(
            self.base_url,
            headers=self.headers,
            data=json.dumps(data),
        )

        if response.status_code != 200:
            print(f"Error checking plagiarism for {file_path}: {response.text}")
            print(f"this should print data: {data}")
            return False

        result = response.json()

        return result["found"]

    @staticmethod
    def get_content(file_path):
        with open(file_path, "r") as f:
            content = f.read()

        return content


if __name__ == "__main__":
    api_key = os.getenv("COPYLEAKS_API_KEY")

    plagiarism_checker = PlagiarismChecker(api_key=api_key)

    md_files = glob.glob("**/*.mdx", recursive=True)

    print("----\n\n")
    print("\n".join(md_files))
    print("\n\n----")

    flagged_files = []
    plagiarism_found = False
    for md_file in md_files:
        if plagiarism_checker.check_plagiarism(md_file):
            print(f"Plagiarism detected in {md_file}")

            plagiarism_found = True
            flagged_files.append(md_file)

    if plagiarism_found:
        print("Plagiarism check failed. Please review the flagged files.")

        # print flagged files
        print(f"Flagged files: {','.join(flagged_files)}")

        sys.exit(1)
    else:
        print("No plagiarism detected.")
