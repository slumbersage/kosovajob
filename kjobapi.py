from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Dictionary mapping city option values to labels
city_options = {
    '1': 'Prishtinë',
    '2': 'Ferizaj',
    '3': 'Gjilan',
    '4': 'Gjakovë',
    '5': 'Mitrovicë',
    '6': 'Prizren',
    '7': 'Pejë',
    '11': 'Podujevë',
    '13': 'Skënderaj',
    '14': 'Burim',
    '15': 'Klinë',
    '16': 'Drenas',
    '17': 'Kastriot',
    '18': 'Fushë Kosovë',
    '19': 'Artanë',
    '20': 'Dardanë',
    '21': 'Deçan',
    '22': 'Malishevë',
    '23': 'Lipjan',
    '24': 'Rahovec',
    '25': 'Shtime',
    '26': 'Therandë',
    '27': 'Viti',
    '33': 'Gjithë Kosovën',
    '34': 'Hani i Elezit',
    '38': 'Graçanicë',
    '43': 'Mitrovicë e Veriut'
}

# Dictionary mapping industry option values to labels
industry_options = {
    '1': 'Administratë',
    '40': 'Arkitekturë',
    '3': 'Art dhe Kulturë',
    '4': 'Banka',
    '5': 'Industria Automobilistike',
    '7': 'Retail dhe Distribuim',
    '8': 'Ndërtimtari & Patundshmëri',
    '9': 'Mbështetje e Konsumatorëve, Call Center',
    '10': 'Ekonomi, Financë, Kontabilitet',
    '11': 'Edukim, Shkencë & Hulumtim',
    '13': 'Punë të Përgjithshme',
    '14': 'Burime Njerëzore',
    '15': 'Teknologji e Informacionit',
    '16': 'Sigurim',
    '17': 'Gazetari, Shtyp & Media',
    '18': 'Ligj & Legjislacion',
    '20': 'Menaxhment',
    '21': 'Marketing, Reklamim & PR',
    '22': 'Inxhinieri',
    '23': 'Shëndetësi, Medicinë',
    '25': 'Industri Farmaceutike',
    '26': 'Prodhim',
    '29': 'Siguri & Mbrojtje',
    '30': 'Industri të Shërbimit',
    '32': 'Telekomunikim',
    '33': 'Tekstil, Lëkurë, Industri Veshëmbathjeje',
    '34': 'Menaxhment Ekzekutiv',
    '35': 'Gastronomi, Hoteleri, Turizëm',
    '37': 'Transport, Logjistikë'
}

# Function to scrape the website and extract job data
def scrape_jobs(city=None, industry=None, query=None):
    base_url = 'https://kosovajob.com'
    params = {}
    
    # Convert city to integer if it's a valid city name
    if city and city in city_options.values():
        city = list(city_options.keys())[list(city_options.values()).index(city)]
    
    # Add parameters to the request if provided
    if city:
        params['jobCity'] = city
    if industry:
        params['jobIndustry'] = industry
    if query:
        params['jobTitle'] = query
    
    # Make the request to the website
    response = requests.get(base_url, params=params)
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract job data
    job_listings = soup.find_all('div', class_='jobListCnts')
    
    jobs = []
    for job in job_listings:
        title = job.find('div', class_='jobListTitle').text.strip()
        city = job.find('div', class_='jobListCity').text.strip()
        expires = job.find('div', class_='jobListExpires').text.strip()
        link = job.find('a')['href']
        image_url = job.find('div', class_='jobListImage')['data-background-image']
        
        jobs.append({
            'title': title,
            'city': city,
            'expires': expires,
            'link': link,
            'image_url': image_url
        })
    
    return jobs

# Route to fetch jobs
@app.route('/jobs')
def get_jobs():
    # Get query parameters from the request
    city = request.args.get('city')
    industry = request.args.get('industry')
    query = request.args.get('query')
    
    # Scrape jobs based on parameters
    jobs = scrape_jobs(city, industry, query)
    
    # Return JSON response
    return jsonify(jobs)


# Route to fetch job details
@app.route('/job_details')
def get_job_details():
    # Get job URL from the query parameters
    job_url = request.args.get('url')
    
    # Parse job details
    job_details = parse_job_details(job_url)
    
    # Return JSON response
    return jsonify(job_details)




def parse_job_details(job_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }
    
    response = requests.get(job_url, headers=headers)
    html_content = response.text
    
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove specific unwanted elements
    unwanted_elements = soup.find_all(['footer', 'div', 'a'], class_=['contactLinks', 'socialLinks', 'footerLink', 'fbLinks'])
    for element in unwanted_elements:
        element.extract()
    
    # Remove div elements with class containing 'footer'
    footer_divs = soup.find_all('div', class_=lambda value: value and 'footer' in value)
    for div in footer_divs:
        div.extract()
    
    # Merge paragraphs and lists into a single content string with Discord markdown formatting
    content = ''
    for element in soup.find_all(['p', 'ul']):
        if element.name == 'ul':
            content += '\n' + '\n'.join(['- ' + li.get_text(strip=True) for li in element.find_all('li')]) + '\n'
        else:
            content += '**' + element.get_text(strip=True) + '**\n\n'
    
    # Remove excessive whitespace characters at the end of the content string
    content = content.rstrip()
    
    # Extract additional job details
    additional_details = soup.find('div', class_='containerRightArea')
    categories = additional_details.find_all('div', class_='listingArea')

    details = {}
    for category in categories:
        label = category.find('b', class_='listingAreaInfo')
        if label:
            details[label.get_text(strip=True)] = category.get_text(strip=True).replace(label.get_text(strip=True), '')
    
    # Create a dictionary to hold the extracted job details
    job_details = {
        "content": content,
        **details  # Include additional details
    }
    
    # Return the dictionary of job details
    return job_details


if __name__ == '__main__':
    app.run(debug=True)
