import requests
import json
from typing import Dict, Any

class TokenInfoAgent:
    """
    Autonomous agent that fetches real-time cryptocurrency prices using CoinGecko API
    """
    
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.supported_tokens = {
            'btc': 'bitcoin',
            'eth': 'ethereum',
            'sol': 'solana',
            'near': 'near',
            'usdt': 'tether',
            'usdc': 'usd-coin'
        }
    
    def get_token_price(self, token_id: str, vs_currency: str = 'usd') -> Dict[str, Any]:
        """
        Fetch current price of a token
        """
        url = f"{self.base_url}/simple/price"
        params = {
            'ids': token_id,
            'vs_currencies': vs_currency,
            'include_market_cap': 'false',
            'include_24hr_vol': 'false',
            'include_24hr_change': 'false',
            'include_last_updated_at': 'true'
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def process_query(self, query: str) -> str:
        """
        Parse natural language query and return formatted price info
        """
        query = query.lower()
        
        # Extract token symbol
        token_symbol = None
        for symbol in self.supported_tokens:
            if symbol in query:
                token_symbol = symbol
                break
        
        if not token_symbol:
            return "Sorry, I couldn't identify a supported token in your query."
        
        # Extract vs currency (default to USD)
        vs_currency = 'usd'
        if 'eur' in query:
            vs_currency = 'eur'
        elif 'gbp' in query:
            vs_currency = 'gbp'
        
        # Get token price
        token_id = self.supported_tokens[token_symbol]
        price_data = self.get_token_price(token_id, vs_currency)
        
        if 'error' in price_data:
            return f"Error fetching price: {price_data['error']}"
        
        if token_id not in price_data:
            return "Sorry, I couldn't fetch the price for that token."
        
        price = price_data[token_id][vs_currency]
        last_updated = price_data[token_id].get('last_updated_at', 'unknown')
        
        return f"Current price of 1 {token_symbol.upper()}: {price} {vs_currency.upper()}\n(Last updated at: {last_updated})"

# Example usage
if __name__ == "__main__":
    agent = TokenInfoAgent()
    
    print("Token Info Agent - Ready to answer your queries!")
    print("Supported tokens: BTC, ETH, SOL, NEAR, USDT, USDC")
    print("Example queries: 'price of SOL', 'how much is 1 ETH in EUR'")
    print("Type 'exit' to quit\n")
    
    while True:
        query = input("Your query: ").strip()
        if query.lower() == 'exit':
            break
        
        response = agent.process_query(query)
        print("\n" + response + "\n")
