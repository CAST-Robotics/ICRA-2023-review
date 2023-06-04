import requests
from bs4 import BeautifulSoup
import os

def parse_html(html_file):
    """
    Parse the given html file for a session page

    Args:
        html_file: File-like object containing the raw HTML data ,
    
    Returns: 
        list: all papers in that session and their abstract url
    """
    # Parse the HTML code using BeautifulSoup
    soup = BeautifulSoup(html_file, 'html.parser')

    # Find all the papers elements
    paper_elements = soup.find_all('h5', {'class': 'semi'})

    output_papers = []

    for element in paper_elements:
        paper_title = element.text
        paper_url = element.parent.parent['href']
        paper_data = (paper_title, paper_url)
        output_papers.append(paper_data)

    return output_papers

def format_markdown(papers):
    """
    Formats the given list of paper titles and abstract URLs as a Markdown list.

    Args:
        papers (list): A list of tuples containing the title and abstract URL of each paper.

    Returns:
        str: The formatted Markdown string.
    """
    markdown = "## Paper List\n\n"
    
    for title, url in papers:
        markdown += f"- {title}\n"
        markdown += f"[[Abstract]]({url})\n\n"

    return markdown

def process_session_file(html_path):
    """
    Process a single HTML file containing information about a session.

    Args:
        html_path (str): The path to the HTML file.

    Returns:
        str: The formatted Markdown string.
    """
    # Open the HTML file and read its contents
    with open(html_path, 'r') as f:
        html = f.read()

    # Parse the HTML and extract the paper information
    papers = parse_html(html)

    # Format the paper information as a Markdown list
    markdown = format_markdown(papers)
    
    # Create a directory with the same name as the HTML file
    dir_path = os.path.splitext(html_path)[0]
    os.makedirs(dir_path, exist_ok=True)

    # Write the formatted Markdown to a README.md file in the new directory
    with open(os.path.join(dir_path, 'README.md'), 'w') as f:
        f.write(markdown)

    return markdown

if __name__ == '__main__':

    session_files = sorted([f for f in os.listdir('./Sessions') if f.endswith('.html')])
    
    readme = ""
    for session_file in session_files:
        # Process each HTML file and write the formatted Markdown to a README.md file in a new directory
        markdown = process_session_file(os.path.join('./Sessions', session_file))
        # Process main README file
        with open(os.path.join('./Sessions', session_file), 'r') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            page_title = soup.find('h1', {'class': 'm-bottom-25'})
            readme += f"- [{page_title.text}](./{os.path.splitext(session_file)[0]})\n"
    
    print (readme)