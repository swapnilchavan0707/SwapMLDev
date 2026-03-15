import os
import secrets
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

# Import our modular components
from database.models import db, Product, PriceLog
from engine.strategy import PricingStrategy
from engine.scraper import MarketScraper

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', secrets.token_hex(24))

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///aura_pricing.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB with App
db.init_app(app)

# Initialize Engine Components
strategy = PricingStrategy()
scraper = MarketScraper()


# --- ROUTES ---

@app.route('/')
def index():
    """Main Dashboard: Displays assets and runs live repricing logic."""
    products = Product.query.all()

    # Live Audit: Check market and update prices on page load
    for p in products:
        # 1. Simulate/Scrape new competitor price
        p.competitor_price = scraper.get_competitor_price(p.name)

        # 2. Apply ML-driven pricing strategy
        suggested_price = strategy.apply_rules(p)

        # 3. If price changes, log it for analytics history
        if suggested_price != p.current_price:
            p.current_price = suggested_price
            new_log = PriceLog(product_id=p.id, price=suggested_price)
            db.session.add(new_log)

    db.session.commit()
    return render_template('index.html', products=products)


@app.route('/analytics')
def analytics():
    """High-level Strategic Insights & Visualization."""
    products = Product.query.all()
    if not products:
        flash("No data available for analysis. Register assets first.")
        return redirect(url_for('index'))

    # Prepare Data for Chart.js
    names = [p.name for p in products]
    aura_prices = [p.current_price for p in products]
    comp_prices = [p.competitor_price for p in products]
    stocks = [p.stock_level for p in products]

    # Calculate Business KPIs
    total_inventory_value = sum(p.current_price * p.stock_level for p in products)
    total_units = sum(p.stock_level for p in products)

    # Calculate Avg Margin: ((Price - Cost) / Price)
    margins = [((p.current_price - p.base_cost) / p.current_price) * 100 for p in products if p.current_price > 0]
    avg_margin = round(sum(margins) / len(margins), 1) if margins else 0

    return render_template('analytics.html',
                           names=names,
                           aura_prices=aura_prices,
                           comp_prices=comp_prices,
                           stocks=stocks,
                           total_value=f"{total_inventory_value:,.2f}",
                           total_stock=total_units,
                           avg_margin=avg_margin)


@app.route('/add_product', methods=['POST'])
def add_product():
    """Register a new luxury asset into the engine."""
    try:
        name = request.form['name']
        cost = float(request.form['base_cost'])
        comp = float(request.form['competitor_price'])
        stock = int(request.form['stock'])

        new_asset = Product(
            name=name,
            base_cost=cost,
            competitor_price=comp,
            current_price=comp,
            stock_level=stock
        )
        db.session.add(new_asset)
        db.session.commit()

        # Initial log entry for the graph
        db.session.add(PriceLog(product_id=new_asset.id, price=comp))
        db.session.commit()

        flash(f"Asset '{name}' secured and pricing intelligence active.")
    except Exception as e:
        flash(f"Error integrating asset: {str(e)}")

    return redirect(url_for('index'))


@app.route('/update_competitor/<int:id>', methods=['POST'])
def update_competitor(id):
    """Manual override for market data."""
    product = Product.query.get_or_404(id)
    product.competitor_price = float(request.form['new_comp_price'])
    product.stock_level = int(request.form['new_stock'])
    db.session.commit()
    flash(f"Market update received for {product.name}.")
    return redirect(url_for('index'))


# --- INITIALIZATION ---

if __name__ == '__main__':
    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()
        print("Aura Database: Online")

    # Run server
    app.run(debug=True, port=5000)