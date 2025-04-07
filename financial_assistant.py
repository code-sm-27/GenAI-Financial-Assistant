import os
import json
import logging
import yfinance as yf
import numpy as np
from datetime import datetime
from google import genai
from google.genai import types

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    filename="trading_platform.log",
    format="%(asctime)s - %(levelname)s - %(message)s"
)

PORTFOLIO_FILE = "portfolio.json"

class TradingPlatform:
    def __init__(self):
        self.portfolio = self.load_portfolio()
        self.conversation_history = []
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY")
        self.model = "gemini-2.0-flash"  # Adjust if necessary
        
        # Inject constant context to ensure responses are tailored exclusively to the Indian market.
        india_context = (
            "All responses and advice must be tailored exclusively to the Indian market and investment options available in India."
        )
        self.conversation_history.append(
            types.Content(role="model", parts=[types.Part.from_text(text=india_context)])
        )

    def load_portfolio(self):
        if os.path.exists(PORTFOLIO_FILE):
            try:
                with open(PORTFOLIO_FILE, "r") as f:
                    portfolio = json.load(f)
                logging.info("Portfolio loaded successfully.")
                return portfolio
            except Exception as e:
                logging.error("Error loading portfolio: %s", e)
        return {}

    def save_portfolio(self):
        try:
            with open(PORTFOLIO_FILE, "w") as f:
                json.dump(self.portfolio, f, indent=4)
            logging.info("Portfolio saved successfully.")
        except Exception as e:
            logging.error("Error saving portfolio: %s", e)

    def generate_response(self):
        try:
            client = genai.Client(api_key=self.gemini_api_key)
            config = types.GenerateContentConfig(
                temperature=0.9,
                top_p=0.95,
                top_k=40,
                max_output_tokens=4096,
                response_mime_type="text/plain",
            )
            response = client.models.generate_content(
                model=self.model,
                contents=self.conversation_history,
                config=config,
            )
            logging.info("Gen-AI response generated successfully.")
            return response.text
        except Exception as e:
            logging.error("Gen-AI error: %s", e)
            return f"An error occurred while generating the response: {str(e)}"

    def fetch_market_data(self):
        # Popular Indian stocks (Yahoo Finance uses the .NS suffix)
        stocks = {
            "TCS": "TCS.NS",
            "Reliance Industries": "RELIANCE.NS",
            "Infosys": "INFY.NS",
            "HDFC Bank": "HDFCBANK.NS",
            "ICICI Bank": "ICICIBANK.NS",
            "Larsen & Toubro": "LT.NS",
            "Bharti Airtel": "BHARTIARTL.NS",
            "Kotak Mahindra Bank": "KOTAKBANK.NS",
            "Hindustan Unilever": "HINDUNILVR.NS",
            "State Bank of India": "SBIN.NS"
        }
        etfs = {"NIFTYBEES": "NIFTYBEES.NS"}
        data_str = "=== Current Equity Market Data (India) ===\n"
        for name, ticker in {**stocks, **etfs}.items():
            try:
                stock = yf.Ticker(ticker)
                data = stock.history(period="1d")
                if not data.empty:
                    current_price = data['Close'].iloc[-1]
                    data_str += f"- {name} (Ticker: {ticker}): ₹{current_price:.2f}\n"
                else:
                    data_str += f"- {name} (Ticker: {ticker}): Data not available\n"
            except Exception as e:
                logging.error("Error fetching data for %s: %s", name, e)
                data_str += f"- {name} (Ticker: {ticker}): Error retrieving data\n"
        return data_str

    def analyze_equity_data(self):
        stocks = {
            "TCS": "TCS.NS",
            "Reliance Industries": "RELIANCE.NS",
            "Infosys": "INFY.NS",
            "HDFC Bank": "HDFCBANK.NS",
            "ICICI Bank": "ICICIBANK.NS",
            "Larsen & Toubro": "LT.NS",
            "Bharti Airtel": "BHARTIARTL.NS",
            "Kotak Mahindra Bank": "KOTAKBANK.NS",
            "Hindustan Unilever": "HINDUNILVR.NS",
            "State Bank of India": "SBIN.NS"
        }
        results = {}
        for name, ticker in stocks.items():
            try:
                stock = yf.Ticker(ticker)
                data = stock.history(period="1mo")
                if not data.empty and len(data) > 1:
                    data['Daily Return'] = data['Close'].pct_change()
                    avg_return = data['Daily Return'].mean()
                    volatility = data['Daily Return'].std()
                    results[name] = {
                        "avg_return": avg_return,
                        "volatility": volatility,
                        "last_price": data['Close'].iloc[-1]
                    }
            except Exception as e:
                logging.error("Error analyzing data for %s: %s", name, e)
        return results

    def generate_equity_advice(self):
        analysis = self.analyze_equity_data()
        if not analysis:
            return "Insufficient equity data for analysis."
        safest = min(analysis.items(), key=lambda x: x[1]["volatility"])
        best_return = max(analysis.items(), key=lambda x: x[1]["avg_return"])
        advice = "=== Equity Analysis (Indian Market - High Risk) ===\n"
        advice += f"- Safest stock (lowest volatility): {safest[0]} (Volatility: {safest[1]['volatility']:.4f}, Last Price: ₹{safest[1]['last_price']:.2f})\n"
        advice += f"- Highest average daily return: {best_return[0]} (Avg Return: {best_return[1]['avg_return']*100:.2f}%)\n"
        if safest[0] != best_return[0]:
            advice += "A balanced allocation to both may help capture stability and growth.\n"
        else:
            advice += "This stock shows strength on both metrics and could be a strong candidate.\n"
        return advice

    def generate_comprehensive_advice(self):
        low_risk = (
            "Low-Risk Options (India):\n"
            "1. Fixed Deposits – Secure returns from Indian banks (typically 6-7% p.a.).\n"
            "2. Public Provident Fund (PPF) – Government-backed with attractive tax benefits (around 7-8% p.a.).\n"
            "3. Money Market Funds – Short-term debt instruments with high liquidity.\n"
            "4. Treasury Bills – Very safe, though with lower returns.\n"
            "5. Certificate of Deposit – Fixed-term deposits with negotiated returns.\n"
        )
        medium_risk = (
            "Medium-Risk Options (India):\n"
            "1. Balanced Mutual Funds – A mix of Indian equities and debt instruments.\n"
            "2. Debt Funds – Invest in bonds and treasury bills for stable income.\n"
            "3. Dividend-Paying Stocks – Blue-chip stocks that provide regular dividend payouts.\n"
            "4. Exchange-Traded Funds (ETFs) – Diversified exposure to Indian market indices.\n"
            "5. Corporate Bonds – Fixed-income securities from established Indian companies.\n"
        )
        high_risk = (
            "High-Risk Options (India):\n"
            "1. Direct Equities – Investing directly in Indian stocks for high returns (with high volatility).\n"
            "2. Equity Mutual Funds – Investments in Indian stocks via SIPs or lump sums for aggressive growth.\n"
            "3. FOREX Trading – Trading in Indian Rupee and other currencies (with significant risks).\n"
            "4. Hedge Funds – Alternative strategies with high return potential.\n"
        )
        equity_advice = self.generate_equity_advice()
        comprehensive = (
            "=== Comprehensive Investment Strategy (Tailored for India) ===\n\n"
            "1. **Equity Investments (High-Risk):**\n" + equity_advice + "\n\n"
            "2. **Low-Risk Investments:**\n" + low_risk + "\n\n"
            "3. **Medium-Risk Investments:**\n" + medium_risk + "\n\n"
            "A diversified portfolio across these categories can balance high returns with stability. "
            "Always consider your risk tolerance, investment horizon, and personal financial goals.\n\n"
            "Disclaimer: This advice is based on simplified models and publicly available data in India. "
            "I am not a licensed financial advisor; this information is for educational purposes only."
        )
        return comprehensive

    def handle_investment_query(self):
        """
        For queries like:
        "Okay give me real time examples for various investment options and what are their returns and risks which is the best option available"
        This method fetches real time market data, analyzes returns and risks, and provides tailored strategy examples.
        """
        # Fetch real-time market data for equities.
        market_data = self.fetch_market_data()
        # Perform equity analysis for high-risk options.
        equity_analysis = self.generate_equity_advice()
        # Combine with static examples for low and medium risk.
        static_low_medium = (
            "Additional Investment Options (Static Examples):\n"
            "Low-Risk: Fixed Deposits (6-7% p.a.), PPF (7-8% p.a.)\n"
            "Medium-Risk: Balanced Mutual Funds, Debt Funds, Dividend-Paying Stocks, ETFs, and Corporate Bonds.\n"
        )
        response = (
            "Here are real-time examples of various investment options available in India:\n\n"
            f"{market_data}\n\n"
            "Equity (High-Risk) Analysis:\n" + equity_analysis + "\n\n" +
            static_low_medium +
            "Based on the current data, a diversified approach combining these asset classes may offer the best balance of returns and risk. "
            "For example, you could allocate 40% in high-growth equities, 30% in medium-risk mutual funds/ETFs, and 30% in low-risk fixed income instruments. "
            "This allocation can be adjusted based on your risk appetite and financial goals.\n\n"
            "Disclaimer: The information provided here is based on a simplified model and publicly available data from India. "
            "I am not a licensed financial advisor; please consult a professional for personalized advice."
        )
        return response

    def place_order(self, order_type, symbol, quantity):
        symbol = symbol.upper()
        try:
            ticker = f"{symbol}.NS"
            current_data = yf.Ticker(ticker).history(period="1d")
            if not current_data.empty:
                price = current_data['Close'].iloc[-1]
            else:
                price = 0.0
            if order_type == "buy":
                if symbol in self.portfolio:
                    prev_qty = self.portfolio[symbol]["quantity"]
                    prev_avg = self.portfolio[symbol]["avg_price"]
                    new_qty = prev_qty + quantity
                    new_avg = ((prev_qty * prev_avg) + (quantity * price)) / new_qty
                    self.portfolio[symbol]["quantity"] = new_qty
                    self.portfolio[symbol]["avg_price"] = new_avg
                else:
                    self.portfolio[symbol] = {"quantity": quantity, "avg_price": price}
                result = f"Order Executed: Bought {quantity} shares of {symbol} at ₹{price:.2f}."
            elif order_type == "sell":
                if symbol in self.portfolio and self.portfolio[symbol]["quantity"] >= quantity:
                    self.portfolio[symbol]["quantity"] -= quantity
                    result = f"Order Executed: Sold {quantity} shares of {symbol} at ₹{price:.2f}."
                    if self.portfolio[symbol]["quantity"] == 0:
                        del self.portfolio[symbol]
                else:
                    result = f"Order Failed: Insufficient holdings in {symbol} to sell {quantity} shares."
            else:
                result = "Invalid order type. Use 'buy' or 'sell'."
            self.save_portfolio()
            return result
        except Exception as e:
            logging.error("Error placing order for %s: %s", symbol, e)
            return f"An error occurred: {str(e)}"

    def view_portfolio(self):
        if not self.portfolio:
            return "Your portfolio is currently empty."
        view_str = "=== Your Portfolio ===\n"
        for symbol, details in self.portfolio.items():
            view_str += f"- {symbol}: {details['quantity']} shares, Average Price: ₹{details['avg_price']:.2f}\n"
        return view_str

    def run(self):
        welcome_message = (
            "Namaste! Welcome to our GenAI-Powered Financial Assistant and Trading Platform, tailored exclusively for the Indian market. "
            "You can ask about Indian investing, view market data, receive comprehensive investment advice, "
            "or simulate order placements to build your portfolio.\n"
            "Commands:\n"
            "  • To place an order, type: 'order: buy SYMBOL QUANTITY' or 'order: sell SYMBOL QUANTITY'\n"
            "  • To view your portfolio, type: 'portfolio'\n"
            "  • To view market data, type: 'market data'\n"
            "  • To view a comprehensive investment strategy, type: 'investment strategy'\n"
            "  • For real-time examples and analysis (returns & risks), type: 'real time examples'\n"
            "Otherwise, just ask your questions.\n"
            "Please note: This is a simulation for educational purposes only, and I am not a licensed financial advisor."
        )
        print("Assistant:", welcome_message)
        self.conversation_history.append(
            types.Content(role="model", parts=[types.Part.from_text(text=welcome_message)])
        )
        
        while True:
            user_input = input("You: ").strip()
            if user_input.lower() in ["exit", "quit"]:
                goodbye = (
                    "Thank you for using our trading platform simulation. "
                    "Always do your own research and consult a professional for personalized advice. Goodbye!"
                )
                print("Assistant:", goodbye)
                self.conversation_history.append(
                    types.Content(role="model", parts=[types.Part.from_text(text=goodbye)])
                )
                break
            
            # Handle order commands.
            if user_input.lower().startswith("order:"):
                try:
                    parts = user_input.split()
                    order_type = parts[1].lower()
                    symbol = parts[2]
                    quantity = int(parts[3])
                    order_result = self.place_order(order_type, symbol, quantity)
                    print("Assistant:", order_result)
                    self.conversation_history.append(
                        types.Content(role="model", parts=[types.Part.from_text(text=order_result)])
                    )
                except Exception as e:
                    error_msg = f"Order parsing error. Please use format: 'order: buy/sell SYMBOL QUANTITY'. Error: {str(e)}"
                    print("Assistant:", error_msg)
                    self.conversation_history.append(
                        types.Content(role="model", parts=[types.Part.from_text(text=error_msg)])
                    )
                continue
            elif user_input.lower() == "portfolio":
                port_view = self.view_portfolio()
                print("Assistant:", port_view)
                self.conversation_history.append(
                    types.Content(role="model", parts=[types.Part.from_text(text=port_view)])
                )
                continue
            elif "market data" in user_input.lower():
                market_data = self.fetch_market_data()
                print("Assistant:", market_data)
                self.conversation_history.append(
                    types.Content(role="model", parts=[types.Part.from_text(text=market_data)])
                )
                continue
            elif "investment strategy" in user_input.lower():
                comp_advice = self.generate_comprehensive_advice()
                print("Assistant:", comp_advice)
                self.conversation_history.append(
                    types.Content(role="model", parts=[types.Part.from_text(text=comp_advice)])
                )
                continue
            elif "real time examples" in user_input.lower():
                # Handle queries like: "give me real time examples for various investment options and what are their returns and risks which is the best option available"
                detailed_response = self.handle_investment_query()
                print("Assistant:", detailed_response)
                self.conversation_history.append(
                    types.Content(role="model", parts=[types.Part.from_text(text=detailed_response)])
                )
                continue
            
            # General query: add to conversation history and generate a Gen-AI response.
            self.conversation_history.append(
                types.Content(role="user", parts=[types.Part.from_text(text=user_input)])
            )
            ai_response = self.generate_response()
            self.conversation_history.append(
                types.Content(role="model", parts=[types.Part.from_text(text=ai_response)])
            )
            print("Assistant:", ai_response)
        
        self.save_portfolio()

    def handle_investment_query(self):
        """
        Handles queries asking for real time examples, returns, risks, and best options.
        Combines real-time equity data, analysis of returns and volatility,
        and static recommendations for low and medium risk options.
        """
        market_data = self.fetch_market_data()
        equity_analysis = self.generate_equity_advice()
        static_options = (
            "Other Investment Options (Static Examples for India):\n"
            "• Fixed Deposits: ~6-7% annual return, very low risk.\n"
            "• Public Provident Fund (PPF): ~7-8% annual return, government-backed and low risk.\n"
            "• Balanced Mutual Funds: Moderate risk with potential for steady returns.\n"
        )
        response = (
            "Here are real-time examples of various Indian investment options along with their estimated returns and risks:\n\n"
            f"{market_data}\n\n"
            "Equity (High-Risk) Analysis:\n" + equity_analysis + "\n\n" +
            static_options +
            "Based on this information, a diversified portfolio may be ideal. For instance, allocating 40% in high-growth equities, "
            "30% in medium-risk balanced funds/ETFs, and 30% in low-risk fixed income instruments could provide a good balance between risk and return.\n\n"
            "Disclaimer: This information is based on simplified models and publicly available data in India. "
            "I am not a licensed financial advisor; please consult a professional for personalized advice."
        )
        return response

if __name__ == "__main__":
    platform = TradingPlatform()
    platform.run()
