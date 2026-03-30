from flask import Flask, jsonify, request
from flask_cors import CORS
import yfinance as yf
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Ratios CEDEAR (1 CEDEAR = X acciones NYSE)
RATIOS = {
    'NVDA': 10, 'MSFT': 30, 'META': 10, 'GOOGL': 58, 'AAPL': 1,
    'TSLA': 10, 'ASML': 146, 'MELI': 120, 'NU': 2, 'QQQ': 45,
    'RIO': 3, 'SLV': 9, 'B': 2, 'XOM': 6, 'CVX': 16,
    'BMA': 10, 'BRKB': 22, 'RKLB': 15, 'ARKK': 8, 'XLV': 18,
    'SPY': 692, 'VIST': 1, 'TSM': 10, 'NIO': 1
}

@app.route('/api/precio/<ticker>', methods=['GET'])
def get_precio(ticker):
    """Obtiene precio NYSE y devuelve CEDEAR (NYSE / ratio)"""
    ticker = ticker.upper()
    ratio = RATIOS.get(ticker, 1)
    
    try:
        # Descarga precio en tiempo real
        data = yf.download(ticker, period='1d', progress=False)
        
        if data.empty:
            return jsonify({'error': f'Sin datos para {ticker}'}), 404
        
        nyse_price = float(data['Close'].iloc[-1])
        cedear_price = nyse_price / ratio
        
        return jsonify({
            'ticker': ticker,
            'nyse': round(nyse_price, 2),
            'cedear': round(cedear_price, 2),
            'ratio': ratio,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/precios', methods=['POST'])
def get_precios():
    """Obtiene múltiples precios. POST con ['NVDA', 'MSFT', ...]"""
    tickers = request.json.get('tickers', [])
    results = {}
    
    for ticker in tickers:
        ticker = ticker.upper()
        ratio = RATIOS.get(ticker, 1)
        
        try:
            data = yf.download(ticker, period='1d', progress=False, quiet=True)
            
            if not data.empty:
                nyse_price = float(data['Close'].iloc[-1])
                cedear_price = nyse_price / ratio
                results[ticker] = {
                    'nyse': round(nyse_price, 2),
                    'cedear': round(cedear_price, 2),
                    'ratio': ratio,
                    'status': 'ok'
                }
            else:
                results[ticker] = {'error': 'Sin datos', 'status': 'error'}
        
        except Exception as e:
            results[ticker] = {'error': str(e), 'status': 'error'}
    
    return jsonify(results)

@app.route('/api/health', methods=['GET'])
def health():
    """Health check para verificar que la API funciona"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
