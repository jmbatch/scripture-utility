import argparse
import requests
import json
import var

def get_lang_bibles(lang):
    """Fetch Bible translations by language."""
    url = var.BASE_URL + var.BIBLES
    params = {'language': lang}
    headers = var.HEADERS

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Raises an error for bad responses
        data = response.json()
        elements = data['data']
        for ele in elements:
            print(f"\nBible: {ele['nameLocal']} (ID: {ele['id']})")
            print(f"Description: {ele['descriptionLocal']}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    except KeyError as e:
        print(f"Unexpected response format: {e}")


def find_text_key(data):
    """Recursively search for 'text' keys in a dictionary or list."""
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'text':  # If the key is 'text', print its value
                print(value)
            # If the value is a dict or list, recursively search it
            elif isinstance(value, (dict, list)):
                find_text_key(value)
    
    elif isinstance(data, list):
        for item in data:
            # Recursively search each item in the list
            if isinstance(item, (dict, list)):
                find_text_key(item)


def get_passage(bible_id, passage, content_type="json", include_notes=False, include_titles=True,
                include_chapter_numbers=False, include_verse_numbers=True, include_verse_spans=False, use_org_id=False):
    """Fetch a specific passage from the Bible by bible_id and passage reference."""
    
    # Base URL for fetching the passage
    url = f"{var.BASE_URL}/bibles/{bible_id}/passages/{passage}"
    
    # Add parameters to the request
    params = {
        'content-type': content_type,
        'include-notes': str(include_notes).lower(),
        'include-titles': str(include_titles).lower(),
        'include-chapter-numbers': str(include_chapter_numbers).lower(),
        'include-verse-numbers': str(include_verse_numbers).lower(),
        'include-verse-spans': str(include_verse_spans).lower(),
        'use-org-id': str(use_org_id).lower(),
    }

    headers = var.HEADERS

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        find_text_key(data)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching passage: {e}")
    except KeyError as e:
        print(f"Unexpected response format: {e}")
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bible CLI API")
    parser.add_argument("--lang", type=str, help="ISO 639-3 three digit language code used to filter results")
    parser.add_argument("--passage", type=str, help="Provide a specific passage. For example: MAT.1.12-MAT.1.20")
    parser.add_argument("--bible", type=str, help="Provide a Bible ID from the scripture API. For example: 06125adad2d5898a-01")
    args = parser.parse_args()

    if args.lang:
        get_lang_bibles(args.lang)
    if args.passage:
        get_passage(args.bible, args.passage)
    else:
        print("Please provide a language using the --lang option.")
