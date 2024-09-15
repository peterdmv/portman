# Copyright 2024 Peter Dimitrov
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pandas as pd
import plotly.express as px

USD_SEK = 10.24
DKK_SEK = 1.52

# Define your own portfolio:
# - number of shares owned
# - purchase price per stock (local currency)
# - current price (foreign currency)
# - sector
# - sub-sector
portfolio_data = {
    'StockA': {'shares': 15, 'purchase_price': 1000, 'current_price': 100, 'currency': 'USD', 'sector': 'Technology', 'subsector': 'Semiconductors'},
    'StockB': {'shares': 10, 'purchase_price': 1500, 'current_price': 1600, 'currency': 'DKK', 'sector': 'Real Estate', 'subsector': 'Retail'},
    'StockC': {'shares': 7, 'purchase_price': 1300, 'current_price': 1100, 'currency': 'SEK', 'sector': 'Real Estate', 'subsector': 'Retail'},
    # Add more stocks and their corresponding portfolio data...
}

# Initialize lists for data
tickers = []
sectors = []
subsectors = []
price_changes = []
total_values = []

def get_current_stock_price(ticker: str) -> float:
    """
    Get the latest stock price for the given ticker symbol.

    Parameters:
    - ticker (str): The stock ticker symbol (e.g., 'AAPL', 'MSFT').

    Returns:
    - float: The latest closing price of the stock.
    """
    current_price = portfolio_data[ticker]['current_price']
    currency = portfolio_data[ticker]['currency']
    if currency == 'USD':
        current_price = current_price * USD_SEK
    elif currency == 'DKK':
        current_price = current_price * DKK_SEK
    return current_price


# Loop through each ticker
for ticker in portfolio_data:
    tickers.append(ticker)

    # Append sector
    sectors.append(portfolio_data[ticker]['sector'])
    subsectors.append(portfolio_data[ticker]['subsector'])

    current_price = get_current_stock_price(ticker)

    # Get purchase data
    purchase_price = portfolio_data[ticker]['purchase_price']

    # Calculate the percentage change in the stock price
    price_change_percentage = (current_price - purchase_price) / purchase_price
    price_changes.append(price_change_percentage*100)
    total_values.append(portfolio_data[ticker]['shares']*current_price)

# Create DataFrame
df = pd.DataFrame({
    'ticker': tickers,
    'sector': sectors,
    'subsector': subsectors,
    'price_change': price_changes,
    'total_values': total_values,
})

# Convert to string and append '%' symbol
df['percent_change_text'] = df['price_change'].apply(lambda x: f"{x:.2f}%")

# Create custom data for hover and text display
df['custom_data'] = df[['ticker', 'percent_change_text']].values.tolist()

# Define custom color scale: Red -> Dark Gray -> Green
custom_color_scale = [
    (0.0, 'red'),       # Start at red (0%)
    (0.5, '#404040'),   # Middle at dark gray (50%)
    (1.0, 'green')      # End at green (100%)
]

# Create treemap with Plotly
fig = px.treemap(
    df,
    path=[px.Constant("Portfolio"), 'sector', 'subsector', 'ticker'],
    values='total_values',
    color='price_change',
    color_continuous_scale=custom_color_scale,  # Use the custom color scale
    color_continuous_midpoint=0.0,
    custom_data=['ticker', 'percent_change_text', 'total_values']
)

# Update the text inside the tiles using texttemplate with HTML-style formatting
fig.update_traces(texttemplate="<br><b style='font-size:20px'>%{customdata[0]}</b><br><b style='font-size:10px'>%{customdata[1]}</b>",
                  textposition="middle center",
                  hovertemplate=(
                      "<b>Total Value:</b> %{customdata[2]:.0f}<br>"
                      "<extra></extra>"  # Removes the default extra information
                  ))

# Show figure
fig.show()
#fig.write_html("plot.html")