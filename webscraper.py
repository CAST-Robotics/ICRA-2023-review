import requests
from bs4 import BeautifulSoup

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


if __name__ == '__main__':

    path = "./Sessions/rl.html"

    # Open local HTML file
    with open(path, 'r') as f:
        html = f.read()
    
    papers = parse_html(html)
    markdown = format_markdown(papers)
    print(markdown)