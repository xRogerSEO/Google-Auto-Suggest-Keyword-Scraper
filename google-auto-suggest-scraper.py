import requests
from bs4 import BeautifulSoup
import pandas as pd
from google.colab import files
import ipywidgets as widgets
from IPython.display import display

def get_google_suggestions(query, hl='en'):
    url = f"https://www.google.com/complete/search?hl={hl}&output=toolbar&q={query}"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'xml')
    suggestions = [suggestion['data'] for suggestion in soup.find_all('suggestion')]
    return suggestions

def get_extended_suggestions(base_query, hl='en'):
    extended_suggestions = set()
    extended_suggestions.update(get_google_suggestions(base_query, hl))
    for char in 'abcdefghijklmnopqrstuvwxyz':
        extended_suggestions.update(get_google_suggestions(base_query + ' ' + char, hl))
    return list(extended_suggestions)

def capture_suggestions(header, query, all_suggestions):
    print(f"\n{header}:")
    suggestions = get_extended_suggestions(query)
    all_suggestions[header] = suggestions
    for i, suggestion in enumerate(suggestions, 1):
        print(f"{i}. {suggestion}")

def download_csv(button):
    df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in all_suggestions.items()]))
    csv_filename = "google_suggestions.csv"
    df.to_csv(csv_filename, index=False)

    files.download(csv_filename)

base_query = input("Enter a search query: ")

all_suggestions = {}

capture_suggestions("Google Suggest completions", base_query, all_suggestions)

capture_suggestions("Can questions", "Can " + base_query, all_suggestions)

capture_suggestions("How questions", "How " + base_query, all_suggestions)

capture_suggestions("Where questions", "Where " + base_query, all_suggestions)

capture_suggestions("Versus", base_query + " versus", all_suggestions)

capture_suggestions("For", base_query + " for", all_suggestions)

# Create and display the download button
download_button = widgets.Button(description="Download CSV")
download_button.on_click(download_csv)
display(download_button)
