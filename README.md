# FinSight AI

FinSight AI is a Streamlit-based application that combines Yahoo Finance data with Google Generative AI to deliver tailored financial insights for various company stocks.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [File Structure](#file-structure)
- [Contributing](#contributing)
- [License](#license)

## Introduction

FinSight AI leverages Yahoo Finance API for fetching detailed company data including stock information, financial statements, holders information, and price history. It then uses Google Generative AI models to generate insights and analyses based on user queries and the fetched data.

## Features

- Fetch detailed company information including income statements, balance sheets, cash flow statements, major holders, institutional holders, mutual fund holders, insider purchases, recommendations, upgrades/downgrades, and price history.
- Interactive user interface powered by Streamlit.
- Integration with Google Generative AI for generating tailored company analyses based on user queries.
- Custom CSS for enhanced UI/UX.

## Setup

### Prerequisites

Before running the application, make sure you have the following installed:

- Python (version 3.6 or higher)
- Pip (Python package installer)
- Google Generative AI API key
- Streamlit

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your/repository.git
   cd repository
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure Google Generative AI:
   Obtain your Google API key from the Google Cloud Console and set it in the `GOOGLE_API_KEY` variable in `app.py`.

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Navigate to the provided URL (usually http://localhost:8501) in your web browser.

3. Select a company from the dropdown, enter your query, and click "Fetch Data" to retrieve detailed financial information and generated insights.

## Dependencies

- pandas
- json
- streamlit
- yfinance
- google.generativeai

## File Structure

```
├── app.py                   # Main Streamlit application code
├── symbols.csv              # CSV file containing stock symbols and tickers
├── README.md                # This README file
└── requirements.txt         # List of Python dependencies
```

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
