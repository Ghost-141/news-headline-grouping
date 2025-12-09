# Breaking News Scraper

A Python-based news scraping system that collects articles from Bangladeshi news websites and automatically detects breaking news using AI-powered similarity analysis.

## Features

- **Multi-source scraping**: Jamuna TV, Somoy TV, Independent TV
- **Breaking news detection**: AI-powered classification using Ollama embeddings
- **Database storage**: MySQL integration with duplicate prevention

## Project Structure

```
Scrapping Codes/
├── scrappers/           # News scraper modules
│   ├── chrome_driver.py # Selenium WebDriver utilities
│   ├── scrape_jamuna.py # Jamuna TV scraper
│   ├── scrape_somoy.py  # Somoy TV scraper
│   ├── scrape_independent.py # Independent TV scraper
│   └── scrape_channel24.py # Channel 24 scraper
├── utils/               # Utility functions
│   ├── db.py           # Database operations
│   ├── news_detector.py # Breaking news detection logic
│   ├── send_breaking_news.py # Breaking news sender
│   └── send_message.py # WhatsApp message utilities
├── main.py             # Main application entry point
├── query_db.py         # Database query utilities
├── test_breaking_news.py # Breaking news testing
├── news_automation.sql # Database schema
└── pyproject.toml      # Project dependencies
```

## Setup

### Prerequisites

- Python 3.13+
- MySQL Server
- Chrome Browser
- Ollama (for Vector Embeddings)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "Scrapping Codes"
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Setup MySQL database**
   ```bash
   mysql -u root -p < news_automation.sql
   ```

4. **Install Ollama and embedding model**
   ```bash
   # Install Ollama (https://ollama.ai)
   ollama pull embeddinggemma:300m
   ```

5. **Configure database connection**
   Update `utils/db.py` with your MySQL credentials:
   ```python
   conn = mysql.connector.connect(
       host="localhost",
       user="your_username", 
       password="your_password",
       database="news_automation"
   )
   ```

## Usage

### Run All Scrapers with Breaking News Detection
```bash
python main.py
```

### Run Individual Scrapers
```bash
python -m scrappers.scrape_somoy
python -m scrappers.scrape_jamuna
python -m scrappers.scrape_independent
```

### Send Breaking News to WhatsApp
```bash
python -m utils.send_breaking_news
```

### Query Database
```bash
python query_db.py
```

## Breaking News Detection

The system uses AI-powered similarity analysis to detect breaking news:

- **Threshold**: Similarity score > 0.50 = Breaking news
- **Keywords**: Predefined Bengali keywords for critical events
- **Model**: Ollama embeddinggemma:300m for text embeddings
- **Output**: Returns 1 (breaking) or 0 (normal)

### Breaking News Keywords
- হত্যা (murder), দুর্ঘটনা (accident), মৃত্যু (death)
- আগুন (fire), বিস্ফোরণ (explosion), ভূমিকম্প (earthquake)
- গ্রেফতার (arrest), বিক্ষোভ (protest), সংঘর্ষ (clash)
- বন্যা (flood), ঝড় (storm), জরুরি (emergency)

## Database Schema

```sql
CREATE TABLE news (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source VARCHAR(100),
    title TEXT,
    summary TEXT,
    category VARCHAR(100),
    link TEXT,
    publish_time VARCHAR(100),
    is_breaking TINYINT DEFAULT 0,
    sent_status TINYINT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Dependencies

- **selenium**: Web scraping automation
- **mysql-connector**: Database connectivity
- **ollama**: AI embeddings for breaking news detection
- **numpy**: Numerical computations
- **beautifulsoup4**: HTML parsing
- **requests**: HTTP requests



