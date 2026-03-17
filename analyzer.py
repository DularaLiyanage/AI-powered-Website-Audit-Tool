import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def analyze_page(url):
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Text + Word Count
    text = soup.get_text(separator=' ', strip=True)
    words = text.split()
    word_count = len(words)

    # Headings
    h1 = len(soup.find_all('h1'))
    h2 = len(soup.find_all('h2'))
    h3 = len(soup.find_all('h3'))

    # Links
    links = soup.find_all('a', href=True)
    parsed_url = urlparse(url).netloc

    internal = 0
    external = 0

    for link in links:
        href = link['href']
        full_href = urljoin(url, href)
        if parsed_url in urlparse(full_href).netloc:
            internal += 1
        else:
            external += 1

    # CTA Detection (simple heuristic)
    cta_keywords = ["buy", "contact", "get started", "sign up", "book", "try", "demo"]
    ctas = [
        a for a in links
        if any(k in a.get_text().lower() for k in cta_keywords)
    ]
    cta_count = len(ctas)

    # Images
    images = soup.find_all('img')
    total_images = len(images)
    missing_alt = sum(1 for img in images if not img.get('alt'))
    missing_alt_percent = (missing_alt / total_images * 100) if total_images else 0

    # Meta
    title = soup.title.string if soup.title else ""

    meta_desc = ""
    desc_tag = soup.find("meta", attrs={"name": "description"})
    if desc_tag:
        meta_desc = desc_tag.get("content", "")

    metrics = {
        "word_count": word_count,
        "headings": {
            "h1": [h.get_text(strip=True) for h in soup.find_all('h1')],
            "h2": [h.get_text(strip=True) for h in soup.find_all('h2')],
            "h3": [h.get_text(strip=True) for h in soup.find_all('h3')]
        },
        "cta_count": cta_count,
        "links": {"internal": internal, "external": external},
        "images": {
            "total": total_images,
            "missing_alt_percent": round(missing_alt_percent)
        },
        "meta": {
            "title": title,
            "description": meta_desc
        }
    }

    return metrics, text[:4000]