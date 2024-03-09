Made this in roughly 2-3 hours i still need to work more on it,

## API Documentation

### Fetch Jobs
- **URL:** `/jobs`
- **Method:** GET
- **Parameters:**
  - `city` (optional): City name to filter jobs by.
  - `industry` (optional): Industry name to filter jobs by.
  - `query` (optional): Query string to search for specific job titles.
- **Response:** Returns a JSON array of job listings with the following fields:
  - `title`: Title of the job.
  - `city`: City where the job is located.
  - `expires`: Expiry date of the job listing.
  - `link`: URL link to the job listing.
  - `image_url`: URL link to the image associated with the job listing.

### Fetch Job Details
- **URL:** `/job_details`
- **Method:** GET
- **Parameters:**
  - `url`: URL link to the job listing.
- **Response:** Returns a JSON object with the following fields:
  - `content`: Description of the job.
  - Additional fields representing job details extracted from the webpage.

### Example Usage

#### Fetch Jobs
```python
import requests

# Define the base URL of the API
base_url = 'http://localhost:5000'

# Define query parameters
params = {
    'city': 'Prishtinë',
    'industry': 'Teknologji e Informacionit',
    'query': 'Python Developer'
}

# Send GET request to fetch jobs
response = requests.get(f'{base_url}/jobs', params=params)
jobs = response.json()

# Print the job listings
for job in jobs:
    print(job)
```

#### Fetch Job Details
```python
import requests

# Define the URL of the job listing
job_url = 'https://kosovajob.com/agro-com-group/shitese-2-mirembajtese-e-objektit'

# Send GET request to fetch job details
response = requests.get(f'{base_url}/job_details', params={'url': job_url})
job_details = response.json()

# Print the job details
print(job_details)
```

## Usage
- Ensure the Flask application is running.
- Use the provided endpoints to fetch jobs and job details by sending GET requests with appropriate parameters.
- Handle the JSON responses returned by the API endpoints in your application.

Make sure to replace `'http://localhost:5000'` with the actual URL where your Flask application is hosted.

Feel free to customize and extend the API as needed for your project. If you have any further questions or need assistance, don't hesitate to ask!

### My specific use case for the api:

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/XuAqk3eZNGw/0.jpg)](https://www.youtube.com/watch?v=XuAqk3eZNGw)
