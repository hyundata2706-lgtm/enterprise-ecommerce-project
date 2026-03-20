# generate_data.py
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from faker import Faker
import hashlib

from config import Config
from utils import *

# Initialize Faker
fake = Faker()
Faker.seed(42)
random.seed(42)
np.random.seed(42)


class EcommerceDataGenerator:
    def __init__(self):
        self.config = Config()
        self.users = []
        self.products = []
        self.orders = []
        self.order_items = []
        self.reviews = []
        self.payments = []

    def generate_users(self):
        """Generate users data"""
        print(f"Generating {self.config.NUM_USERS} users...")

        countries_list = [c[0] for c in self.config.COUNTRIES]
        countries_weights = [c[1] for c in self.config.COUNTRIES]

        # Convert dates to datetime for consistent operations
        start_datetime = datetime.combine(self.config.START_DATE, datetime.min.time())
        end_datetime = datetime.combine(self.config.END_DATE, datetime.min.time())

        for i in range(1, self.config.NUM_USERS + 1):
            # Generate realistic registration date (older users have earlier dates)
            if i < self.config.NUM_USERS * 0.3:  # 30% early adopters
                reg_datetime = generate_timestamp_between(
                    start_datetime,
                    start_datetime + timedelta(days=180)
                )
            else:
                reg_datetime = generate_timestamp_between(
                    start_datetime + timedelta(days=180),
                    end_datetime
                )

            # Last login is after registration
            last_login = generate_timestamp_between(reg_datetime, end_datetime)

            # Active status: users with recent login (last 30 days) are active
            is_active = (end_datetime - last_login).days <= 30

            user = {
                'user_id': i,
                'email': fake.email(),
                'country': random.choices(countries_list, weights=countries_weights)[0],
                'registration_date': reg_datetime.date(),
                'last_login': last_login,
                'is_active': is_active
            }
            self.users.append(user)

        print(f"✓ Generated {len(self.users)} users")
        return pd.DataFrame(self.users)

    def generate_products(self):
        """Generate products data"""
        print(f"Generating {self.config.NUM_PRODUCTS} products...")

        categories = list(self.config.CATEGORIES.keys())
        start_datetime = datetime.combine(self.config.START_DATE, datetime.min.time())
        end_datetime = datetime.combine(self.config.END_DATE, datetime.min.time())

        for i in range(1, self.config.NUM_PRODUCTS + 1):
            category = random.choice(categories)
            brand = random.choice(self.config.BRANDS[category])
            price = generate_price(category, self.config)
            stock = generate_stock_quantity()

            product = {
                'product_id': i,
                'product_name': f"{brand} {fake.catch_phrase()} {category}",
                'category': category,
                'brand': brand,
                'price': price,
                'stock_quantity': stock,
                'created_at': generate_timestamp_between(
                    start_datetime,
                    end_datetime
                ).date()
            }
            self.products.append(product)

        print(f"✓ Generated {len(self.products)} products")
        return pd.DataFrame(self.products)

    def generate_orders(self):
        """Generate orders data"""
        print(f"Generating {self.config.NUM_ORDERS} orders...")

        # Users who have orders (some users may have no orders)
        active_users = [u for u in self.users if u['is_active'] or random.random() < 0.3]

        order_statuses = [s[0] for s in self.config.ORDER_STATUS]
        status_weights = [s[1] for s in self.config.ORDER_STATUS]

        end_datetime = datetime.combine(self.config.END_DATE, datetime.min.time())

        for i in range(1, self.config.NUM_ORDERS + 1):
            user = random.choice(active_users)

            # Convert registration_date (date) to datetime for comparison
            reg_datetime = datetime.combine(user['registration_date'], datetime.min.time())
            order_date = generate_timestamp_between(reg_datetime, end_datetime)

            status = random.choices(order_statuses, weights=status_weights)[0]

            # Total amount will be updated later from order_items
            order = {
                'order_id': i,
                'user_id': user['user_id'],
                'order_date': order_date,
                'status': status,
                'total_amount': 0  # placeholder
            }
            self.orders.append(order)

        print(f"✓ Generated {len(self.orders)} orders")
        return pd.DataFrame(self.orders)

    def generate_order_items(self):
        """Generate order items data"""
        print(f"Generating {self.config.NUM_ORDER_ITEMS} order items...")

        # Each order has 1-5 items on average
        order_item_id = 1

        for order in self.orders:
            if order['status'] == 'cancelled':
                num_items = random.randint(0, 2)  # Cancelled orders have fewer items
            else:
                # Poisson distribution for number of items
                num_items = min(10, np.random.poisson(2.5) + 1)

            # Randomly select products for this order
            selected_products = random.sample(self.products, min(num_items, len(self.products)))

            order_total = 0

            for product in selected_products:
                quantity = random.randint(1, 3)
                unit_price = product['price']

                # Apply discount for some items (10% chance)
                if random.random() < 0.1:
                    unit_price = round(unit_price * random.uniform(0.7, 0.95), 2)

                item_total = quantity * unit_price
                order_total += item_total

                order_item = {
                    'order_item_id': order_item_id,
                    'order_id': order['order_id'],
                    'product_id': product['product_id'],
                    'quantity': quantity,
                    'unit_price': unit_price
                }
                self.order_items.append(order_item)
                order_item_id += 1

            # Update order total
            order['total_amount'] = round(order_total, 2)

        print(f"✓ Generated {len(self.order_items)} order items")
        return pd.DataFrame(self.order_items)

    def generate_reviews(self):
        """Generate reviews data"""
        print(f"Generating {self.config.NUM_REVIEWS} reviews...")

        # Only users who have completed orders can review
        users_with_orders = set([o['user_id'] for o in self.orders if o['status'] == 'completed'])

        # Products that have been ordered
        ordered_product_ids = set([item['product_id'] for item in self.order_items])

        review_id = 1
        used_combinations = set()  # Prevent duplicate user-product reviews

        end_datetime = datetime.combine(self.config.END_DATE, datetime.min.time())

        while len(self.reviews) < self.config.NUM_REVIEWS:
            user_id = random.choice(list(users_with_orders))
            product_id = random.choice(list(ordered_product_ids))

            # Check if user already reviewed this product
            if (user_id, product_id) in used_combinations:
                continue

            used_combinations.add((user_id, product_id))

            rating = generate_rating()
            review_text = generate_review_text(rating)

            # Review date after order completion
            user_orders = [o for o in self.orders if o['user_id'] == user_id and o['status'] == 'completed']
            if user_orders:
                latest_order = max(user_orders, key=lambda x: x['order_date'])
                review_date = generate_timestamp_between(latest_order['order_date'], end_datetime)
            else:
                start_datetime = datetime.combine(self.config.START_DATE, datetime.min.time())
                review_date = generate_timestamp_between(start_datetime, end_datetime)

            review = {
                'review_id': review_id,
                'user_id': user_id,
                'product_id': product_id,
                'rating': rating,
                'review_text': review_text,
                'created_at': review_date
            }
            self.reviews.append(review)
            review_id += 1

        print(f"✓ Generated {len(self.reviews)} reviews")
        return pd.DataFrame(self.reviews)

    def generate_payments(self):
        """Generate payments data"""
        print(f"Generating {self.config.NUM_PAYMENTS} payments...")

        payment_methods = [m[0] for m in self.config.PAYMENT_METHODS]
        method_weights = [m[1] for m in self.config.PAYMENT_METHODS]

        payment_statuses = [s[0] for s in self.config.PAYMENT_STATUS]
        status_weights = [s[1] for s in self.config.PAYMENT_STATUS]

        # Only completed orders have payments (some may fail)
        eligible_orders = [o for o in self.orders if o['status'] in ['completed', 'pending']]

        payment_id = 1
        end_datetime = datetime.combine(self.config.END_DATE, datetime.min.time())

        # Generate payments for eligible orders (some orders may have multiple payment attempts)
        for order in eligible_orders[:self.config.NUM_PAYMENTS]:
            # Some orders might have multiple payment attempts
            num_attempts = 1 if random.random() < 0.8 else random.randint(2, 3)

            for attempt in range(num_attempts):
                payment_method = random.choices(payment_methods, weights=method_weights)[0]
                payment_status = random.choices(payment_statuses, weights=status_weights)[0]

                # Payment date after order date
                max_payment_date = min(order['order_date'] + timedelta(days=7), end_datetime)
                payment_date = generate_timestamp_between(order['order_date'], max_payment_date)

                payment = {
                    'payment_id': payment_id,
                    'order_id': order['order_id'],
                    'payment_method': payment_method,
                    'payment_status': payment_status,
                    'amount': order['total_amount'] if payment_status == 'success' else round(
                        order['total_amount'] * random.uniform(0.5, 1), 2),
                    'payment_date': payment_date
                }
                self.payments.append(payment)
                payment_id += 1

                # If payment successful, stop attempting
                if payment_status == 'success':
                    break

        print(f"✓ Generated {len(self.payments)} payments")
        return pd.DataFrame(self.payments)

    def save_to_csv(self, output_dir='data'):
        """Save all data to CSV files"""
        import os

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        print(f"\nSaving data to {output_dir}/...")

        pd.DataFrame(self.users).to_csv(f'{output_dir}/users.csv', index=False)
        pd.DataFrame(self.products).to_csv(f'{output_dir}/products.csv', index=False)
        pd.DataFrame(self.orders).to_csv(f'{output_dir}/orders.csv', index=False)
        pd.DataFrame(self.order_items).to_csv(f'{output_dir}/order_items.csv', index=False)
        pd.DataFrame(self.reviews).to_csv(f'{output_dir}/reviews.csv', index=False)
        pd.DataFrame(self.payments).to_csv(f'{output_dir}/payments.csv', index=False)

        print("✓ All data saved successfully!")

        # Print file sizes
        for file in os.listdir(output_dir):
            if file.endswith('.csv'):
                size = os.path.getsize(f'{output_dir}/{file}') / 1024  # KB
                print(f"  {file}: {size:.2f} KB")

    def generate_all(self):
        """Generate all data"""
        print("=" * 60)
        print("E-COMMERCE DATA GENERATOR")
        print("=" * 60)

        self.generate_users()
        self.generate_products()
        self.generate_orders()
        self.generate_order_items()
        self.generate_reviews()
        self.generate_payments()

        print("\n" + "=" * 60)
        print("DATA GENERATION COMPLETE!")
        print("=" * 60)
        self.print_summary()

    def print_summary(self):
        """Print summary statistics"""
        print("\n📊 SUMMARY STATISTICS:")
        print(f"  Users: {len(self.users)}")
        print(f"  Products: {len(self.products)}")
        print(f"  Orders: {len(self.orders)}")
        print(f"  Order Items: {len(self.order_items)}")
        print(f"  Reviews: {len(self.reviews)}")
        print(f"  Payments: {len(self.payments)}")

        # Additional stats
        completed_orders = len([o for o in self.orders if o['status'] == 'completed'])
        total_revenue = sum([o['total_amount'] for o in self.orders if o['status'] == 'completed'])

        print(f"\n💰 Business Metrics:")
        print(f"  Completed Orders: {completed_orders}")
        print(f"  Total Revenue: ${total_revenue:,.2f}")
        if completed_orders > 0:
            print(f"  Average Order Value: ${total_revenue / completed_orders:,.2f}")

        if self.reviews:
            avg_rating = sum([r['rating'] for r in self.reviews]) / len(self.reviews)
            print(f"  Average Product Rating: {avg_rating:.2f}/5.0")

        # Check data integrity
        print(f"\n🔍 Data Integrity Check:")
        orders_with_items = len(set([item['order_id'] for item in self.order_items]))
        print(f"  Orders with items: {orders_with_items}/{len(self.orders)}")

        payments_for_completed = len([p for p in self.payments if p['payment_status'] == 'success'])
        print(f"  Successful payments: {payments_for_completed}/{len(self.payments)}")


def main():
    # Initialize generator
    generator = EcommerceDataGenerator()

    # Generate all data
    generator.generate_all()

    # Save to CSV
    generator.save_to_csv('data')

    # Show sample of each table
    print("\n📋 Sample Data (first 3 rows of each table):")
    print("\nUsers:")
    print(pd.DataFrame(generator.users).head(3))
    print("\nProducts:")
    print(pd.DataFrame(generator.products).head(3))
    print("\nOrders:")
    print(pd.DataFrame(generator.orders).head(3))
    print("\nOrder Items:")
    print(pd.DataFrame(generator.order_items).head(3))
    print("\nReviews:")
    print(pd.DataFrame(generator.reviews).head(3))
    print("\nPayments:")
    print(pd.DataFrame(generator.payments).head(3))


if __name__ == "__main__":
    main()
