#stikk to test 
import requests
import json
#DeepSeek API Key
DEEPSEEK_API_KEY = "YOUR_DEEPSEEK_API_KEY"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/completion"
def categorise_expense(description):
   """Sends a transaction description to DeepSeek and returns a category."""
   prompt = f"Categorise this transaction: '{description}'. Possible categories: Groceries, Entertainment, Transportation, Food & Drink, Housing, Shopping, Utilities, Health & Fitness, Travel and anything else you deem useful"
   headers = {
       'Authorisation': f'Bearer {DEEPSEEK_API_KEY}',
       'Content-Type': 'application/json'
   }
   data = {
       'model': 'deepseek-llm',
       'prompt': prompt,
       'max_tokens': 10,
       'temperature': 0
   }
   response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
   if response.status_code == 200:
       category = response.json().get('choices', [{}])[0].get('text', '').strip()
       return category
   else:
       return "Uncategorised"