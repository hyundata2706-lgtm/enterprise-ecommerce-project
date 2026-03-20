# config.py
from datetime import datetime, timedelta


class Config:
    #records
    NUM_USERS = 5000
    NUM_PRODUCTS = 2000
    NUM_ORDERS = 10000
    NUM_ORDER_ITEMS = 30000
    NUM_REVIEWS = 8000
    NUM_PAYMENTS = 9000

    # Time range (2 years)
    START_DATE = datetime(2023, 1, 1)
    END_DATE = datetime(2026, 3, 20)

    # Countries distribution
    COUNTRIES = [
        ('Vietnam', 0.45),
        ('USA', 0.20),
        ('Japan', 0.12),
        ('South Korea', 0.08),
        ('Singapore', 0.07),
        ('Thailand', 0.05),
        ('Malaysia', 0.03)
    ]

    # Product categories with price ranges
    CATEGORIES = {
        'Electronics': (100, 2000),
        'Clothing': (20, 200),
        'Books': (10, 50),
        'Home & Garden': (30, 500),
        'Sports': (25, 300),
        'Beauty': (15, 100),
        'Toys': (10, 150),
        'Food': (5, 80)
    }

    # Brands by category
    BRANDS = {
        'Electronics': ['Samsung', 'Apple', 'Sony', 'LG', 'Dell', 'HP', 'Xiaomi'],
        'Clothing': ['Nike', 'Adidas', 'Uniqlo', 'Zara', 'H&M', 'Gucci'],
        'Books': ['Penguin', 'HarperCollins', 'Simon & Schuster', 'Oxford'],
        'Home & Garden': ['IKEA', 'Philips', 'Dyson', 'Bosch'],
        'Sports': ['Nike', 'Adidas', 'Puma', 'Under Armour', 'Reebok'],
        'Beauty': ['L\'Oreal', 'Estee Lauder', 'Shiseido', 'Johnson'],
        'Toys': ['Lego', 'Hasbro', 'Mattel', 'Bandai'],
        'Food': ['Nestle', 'Unilever', 'Pepsi', 'Coca-Cola']
    }

    # Order status distribution
    ORDER_STATUS = [
        ('completed', 0.75),
        ('pending', 0.15),
        ('cancelled', 0.10)
    ]

    # Payment methods distribution
    PAYMENT_METHODS = [
        ('credit_card', 0.50),
        ('paypal', 0.25),
        ('bank_transfer', 0.15),
        ('cash_on_delivery', 0.10)
    ]

    # Payment status distribution
    PAYMENT_STATUS = [
        ('success', 0.85),
        ('failed', 0.10),
        ('pending', 0.05)
    ]
