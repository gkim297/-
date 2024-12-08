import streamlit as st
import yfinance as yf
from datetime import datetime
import pandas as pd

def localCss(fn):
    with open(fn) as f:
        st.sidebar.markdown(f'<style>{f.read()}<style>', unsafe_allow_html=True)

localCss('style.css')

st.sidebar.subheader("Stock Search Web App")
selectedStock = st.sidebar.text_input("Enter a valid stock ticker...", "META")
buttonClicked = st.sidebar.button("GO")

def main():
    try:
        stockData = yf.Ticker(selectedStock)
        info = stockData.info
        
        # Check if the stock info is empty, which means invalid ticker
        if 'regularMarketPrice' not in info or info['regularMarketPrice'] is None:
            st.error("Invalid ticker! Please enter a valid stock ticker.")
            return

        st.subheader(f"Daily **closing price** for {selectedStock}")
        stockDF = stockData.history(period='1d', start='2024-01-01', end=None)
        if stockDF.empty:
            st.write("No historical data available for this stock.")
        else:
            st.line_chart(stockDF.Close)

        st.subheader(f"Last **closing price** for {selectedStock}")
        today = datetime.today().strftime('%Y-%m-%d')
        stockLastPrice = stockData.history(period='1d', start=today, end=today)
        lastPrice = stockLastPrice.Close
        if lastPrice.empty:
            st.write("No data available for today.")
        else:
            st.write(lastPrice)

        st.subheader(f"Daily **volume** for {selectedStock}")
        st.line_chart(stockDF.Volume)

        st.sidebar.subheader("Display Additional Information")
        actions = st.sidebar.checkbox("Stock Actions")
        if actions:
            st.subheader(f"Stock **actions** for {selectedStock}")
            displayAction = stockData.actions
            if displayAction.empty:
                st.write("No data available.")
            else:
                st.write(displayAction)

        majorShareholders = st.sidebar.checkbox("Institutional Shareholders")
        if majorShareholders:
            st.subheader(f"**Institutional Investors** for {selectedStock}")
            displayShareholders = stockData.institutional_holders
            if displayShareholders is None or displayShareholders.empty:
                st.write("No data available.")
            else:
                st.write(displayShareholders)

        balanceSheet = st.sidebar.checkbox("Quarterly Balance Sheet")
        if balanceSheet:
            st.subheader(f"**Quarterly Balance Sheet** for {selectedStock}")
            displayBalanceSheet = stockData.quarterly_balance_sheet
            if displayBalanceSheet.empty:
                st.write("No data available.")
            else:
                st.write(displayBalanceSheet)

        cashflow = st.sidebar.checkbox("Quarterly Cashflow")
        if cashflow:
            st.subheader(f"**Quarterly Cashflow** for {selectedStock}")
            displayCashflow = stockData.quarterly_cashflow
            if displayCashflow.empty:
                st.write("No data available.")
            else:
                st.write(displayCashflow)

        analystRecommendations = st.sidebar.checkbox("Analyst Recommendation")
        if analystRecommendations:
            st.subheader(f"**Analyst Recommendations** for {selectedStock}")
            displayAnalyst = stockData.recommendations
            if displayAnalyst.empty:
                st.write("No data available.")
            else:
                st.write(displayAnalyst)

        keyRatios = st.sidebar.checkbox("Ratios")
        if keyRatios:
            st.subheader(f"**Key Financial Ratios** for {selectedStock}")
            ratios = {
                "Price-to-Earnings (P/E)": info.get("trailingPE", "N/A"),
                "Price-to-Book (P/B)": info.get("priceToBook", "N/A"),
                "Earnings per Share (EPS)": info.get("trailingEps", "N/A"),
                "Dividend Yield": info.get('dividendYield', "N/A"),
                "Return on Equity (ROE)": info.get("returnOnEquity", "N/A"),
                "Return on Investment (ROI)": info.get("returnOnInvestment", "N/A"),
                "Debt-to-Equity (D/E)": info.get("debtToEquity", "N/A"),
                "Market Cap": info.get("marketCap", "N/A"),
                "Forward P/E": info.get('forwardPE', "N/A")
            }

            ratiosDF = pd.DataFrame(list(ratios.items()), columns=['Ratios', 'Value'])
            st.write(ratiosDF)

    except Exception as e:
        st.error(f"An error occurred: {e}. Please try again with a valid stock ticker.")

if buttonClicked:
    main()
