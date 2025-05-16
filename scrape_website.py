import requests
from bs4 import BeautifulSoup
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# List of website URLs (subpages)
websites = [
    'https://furbulousstyles.com/services/',
    'https://furbulousstyles.com/',
    'https://furbulousstyles.com/about-us/',
    'https://furbulousstyles.com/membership/',
    'https://furbulousstyles.com/blog/',
    'https://furbulousstyles.com/contacts-1/',
    #Change these URLs
    
    # Add more URLs here
    # 'https://example.com/page1',
    # 'https://example.com/page2',
]

all_text = ''

for website in websites:
    print(f"Scraping: {website}")
    response = requests.get(website)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text(separator='\n', strip=True)
    all_text += f"\n--- Content from {website} ---\n"
    all_text += text + '\n'

output_filename = 'website_data.txt'
output_path = os.path.join(os.path.dirname(__file__), output_filename)
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(all_text)

print(f"Scraped data from {len(websites)} pages saved to {output_path}")

# Use environment variable for API key (recommended for security)
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Read the scraped website data
with open(output_path, 'r', encoding='utf-8') as f:
    website_text = f.read()

# Compose the prompt
prompt = (
    "You are an expert at organizing website content for AI knowledge bases. "
    "Given the following raw website text, extract and clearly outline the main components of the website, "
    "such as 'About Us', 'Services', 'Testimonials', 'Contact', 'Membership', 'Blog', etc. "
    "For each section, summarize the relevant information in a clear, concise way, suitable for an AI agent to answer FAQs. "
    "Format the output as a knowledge base with clear section headers.\n\n"
    "Website text:\n"
    "'''\n"
    f"{website_text}\n"
    "'''\n"
    "Knowledge base:"
)

# Call OpenAI API (using GPT-4o or GPT-4.1)
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ],
    max_tokens=4096,
    temperature=0.2
)

knowledge_base = response.choices[0].message.content

# Save the knowledge base to a file
knowledge_base_path = os.path.join(os.path.dirname(__file__), 'knowledge_base.txt')
with open(knowledge_base_path, 'w', encoding='utf-8') as f:
    f.write(knowledge_base)

print(f"Knowledge base generated and saved to {knowledge_base_path}") 