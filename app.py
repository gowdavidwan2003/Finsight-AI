import pandas as pd
import json
import streamlit as st
import yfinance as yf
import time
import google.generativeai as genai
import os
import pyperclip
from dotenv import load_dotenv

# Configure Google Generative AI
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize generative models
model_vision = genai.GenerativeModel('gemini-pro-vision')
model_text = genai.GenerativeModel("gemini-1.5-pro-latest")

# Function to fetch and store stock data
def get_and_store_info(ticker_symbol):
    # Fetching data from Yahoo Finance API
    stock = yf.Ticker(ticker_symbol)
    
    try:
        information = stock.info
        information_json = json.dumps(information, indent=4)
    except Exception as e:
        print(f"Error fetching information: {e}")
        information_json = ""

    try:
        income_statement = stock.income_stmt
        income_statement_json = income_statement.to_json(orient='split')
    except Exception as e:
        print(f"Error fetching income statement: {e}")
        income_statement_json = ""

    try:
        balance_sheet = stock.balance_sheet
        balance_sheet_json = balance_sheet.to_json(orient='split')
    except Exception as e:
        print(f"Error fetching balance sheet: {e}")
        balance_sheet_json = ""

    try:
        cash_flow = stock.cashflow
        cash_flow_json = cash_flow.to_json(orient='split')
    except Exception as e:
        print(f"Error fetching cash flow statement: {e}")
        cash_flow_json = ""

    try:
        major_holders = stock.major_holders
        major_holders_json = major_holders.to_json(orient='split')
    except Exception as e:
        print(f"Error fetching major holders: {e}")
        major_holders_json = ""

    try:
        institutional_holders = stock.institutional_holders
        institutional_holders_json = institutional_holders.to_json(orient='split')
    except Exception as e:
        print(f"Error fetching institutional holders: {e}")
        institutional_holders_json = ""

    try:
        mutualfunds_holder = stock.mutualfund_holders
        mutualfunds_holder_json = mutualfunds_holder.to_json(orient='split')
    except Exception as e:
        print(f"Error fetching mutual funds holders: {e}")
        mutualfunds_holder_json = ""

    try:
        insider_purchases = stock.insider_purchases
        insider_purchases_json = insider_purchases.to_json(orient='split')
    except Exception as e:
        print(f"Error fetching insider purchases: {e}")
        insider_purchases_json = ""

    try:
        recommendation = stock.recommendations
        recommendation_json = recommendation.to_json(orient='split')
    except Exception as e:
        print(f"Error fetching recommendations: {e}")
        recommendation_json = ""

    try:
        upgrades_downgrades = stock.upgrades_downgrades
        upgrades_downgrades_json = upgrades_downgrades.to_json(orient='split')
    except Exception as e:
        print(f"Error fetching upgrades/downgrades: {e}")
        upgrades_downgrades_json = ""

    try:
        price_history = stock.history(period="1y")
        price_history = price_history[['Close']]
        price_history.index = price_history.index.astype(str)
        price_history_json = price_history.to_json(orient='split')
    except Exception as e:
        print(f"Error fetching price history: {e}")
        price_history_json = ""


    # Building context for generative model
    context = (
        "Here are the details of the company: " + information_json +
        " Here is the data related to the income statement: " + income_statement_json +
        " Here is the data related to the balance sheet: " + balance_sheet_json +
        " Here is the data related to the cash flow: " + cash_flow_json +
        " Here are the major holders of the company: " + major_holders_json +
        " Here are the institutional holders of the company: " + institutional_holders_json +
        " Here are the mutual fund holders of the company: " + mutualfunds_holder_json +
        " Here are the insider purchases of the company: " + insider_purchases_json +
        " Here are the recommendations for the company: " + recommendation_json +
        " Here are the upgrades and downgrades for the company: " + upgrades_downgrades_json +
        " Here is the price history of the company: " + price_history_json+
        " This concludes the dataset and here the context ends."
    )
    return context

# Dictionary of stock options
df = pd.read_csv('symbols.csv')
options = {}
for index, row in df.iterrows():
    options[row['SYMBOL \n']] = row['Ticker_NS']

# Main function to run the Streamlit app
def main():
    # Set Streamlit page configuration and custom CSS
    st.set_page_config(
        page_title="FinSight AI",
        page_icon="📈",
        layout="wide",  # Adjusted width here
        initial_sidebar_state="expanded"
    )

    # Custom CSS for better UI
    st.markdown(
        """
       <style>
        .main {
            
            max-width: 70%;  /* Adjusted width */
            margin: auto;    /* Center align */
            padding: 20px;
            text-align: center;  /* Center align text */
            overflow-y: auto;   /* Enable vertical scroll */
            height: 100vh;      /* Set full viewport height */
        }
        .stButton button {
            background-color: transparent;
            color: #66FCF1;
            border: 2px solid #66FCF1;
            padding: 12px 28px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 4px;
            transition-duration: 0.4s;
        }
        .stButton button:hover {
            background-color: #66FCF1;
            color: black;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )

    # Streamlit UI components
    st.title('📈 FinSight AI 📈')

    st.markdown("Delivers tailored financial insights by combining Yahoo Finance data with Google Generative AI. Users can fetch and analyze comprehensive company data, aiding informed investment decisions. Currently, there are 1000 stocks available, with 500 from the S&P 500 and 500 from the Nifty 500.")
    st.markdown("""
        ### Developed by Vidwan Gowda H M
        [GitHub](https://github.com/gowdavidwan2003) | [LinkedIn](https://www.linkedin.com/in/gowdavidwan2003/) | [Phone](tel:+917975045560) | [Email](mailto:gowdavidwan2003@gmail.com)
        """)

    # Select company from dropdown
    stock_name = st.selectbox('Select Company', list(options.keys()))
    ticker_symbol = options[stock_name]

    # User input query
    user_query = st.text_input("Enter your query", "")

    st.write("Due to API rate limits, please allow a 1-minute interval between queries.")
    # Fetch data button
    if st.button('Fetch Data'):
        
        # Placeholder for loading message
        loading_message = st.empty()
        loading_message.text('Fetching data, please wait...')

        # Fetching data for selected stock
        data = get_and_store_info(ticker_symbol)

        # Update loading message to show completion
        loading_message.text('Data fetched successfully!')
        time.sleep(2)

        # Generating content using generative model
        loading_message.text('Processing your data — please hold tight!')
        
        prompt = (
            "The role of this model is to provide tailored company analysis. It leverages detailed company data to provide insights only from the data provided with this prompt."
            " If specific data context is absent, respond with: 'I am not equipped with data to address that issue.'"+ data +
            " USER QUERY Begins :" + user_query + " USER QUERY Ends"
            " Instructions to follow:"
            " 1. Do not generate predictions."
            " 2. Along with outputting raw data; focus on summarizing insights."
            " 3. Format all output in a clear, human-readable manner."
            " 4. Ensure data accuracy and prioritize sorting by the latest year first."
            " 5. Provide clear guidance on interpreting and processing the dataset."
            " 6. Offer actionable insights without speculative analysis."
            " 7. If data is missing or incomplete, inform the user and suggest alternative sources or actions."
            " 8. Clearly go through data and provide the most relevant data (not necessarily the exact one needed)."
        )
        
        try:
            responses = model_text.generate_content(prompt)
        except:
            responses = "API rate limit reached. Please try after 1 minute"
        loading_message.empty()
        st.write(responses.text)
        
        

if __name__ == '__main__':
    main()
