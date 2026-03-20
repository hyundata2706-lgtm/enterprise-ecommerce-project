# utils.py
import random
from datetime import datetime, timedelta
import numpy as np


def weighted_choice(choices):
    """Chọn một item dựa trên weight"""
    items, weights = zip(*choices)
    return random.choices(items, weights=weights)[0]


def generate_timestamp_between(start_datetime, end_datetime):
    """Tạo timestamp ngẫu nhiên giữa 2 datetime objects"""
    if start_datetime > end_datetime:
        # Swap if start is after end
        start_datetime, end_datetime = end_datetime, start_datetime

    delta = end_datetime - start_datetime
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start_datetime + timedelta(seconds=random_seconds)


def generate_price(category, config):
    """Tạo price dựa trên category"""
    min_price, max_price = config.CATEGORIES[category]
    # Tạo phân phối skew về giá thấp hơn (realistic)
    price = np.random.exponential(scale=(max_price - min_price) / 3) + min_price
    return round(min(max_price, price), 2)


def generate_stock_quantity():
    """Tạo stock quantity ngẫu nhiên"""
    # Most products have stock, some are low or out
    if random.random() < 0.1:  # 10% out of stock
        return 0
    elif random.random() < 0.2:  # 20% low stock
        return random.randint(1, 10)
    else:
        return random.randint(50, 500)


def generate_rating():
    """Tạo rating với bias về rating cao (realistic)"""
    # Most reviews are 4-5 stars
    ratings = [1, 2, 3, 4, 5]
    weights = [0.05, 0.10, 0.20, 0.35, 0.30]
    return random.choices(ratings, weights=weights)[0]


def generate_review_text(rating):
    """Tạo review text đơn giản dựa trên rating"""
    templates = {
        1: ["Very disappointed", "Poor quality", "Not worth it", "Terrible product", "Waste of money"],
        2: ["Not satisfied", "Could be better", "Below expectations", "Disappointing", "Average at best"],
        3: ["Average", "Okay", "Not bad", "Decent product", "Fair quality"],
        4: ["Good product", "Satisfied", "Nice quality", "Worth the price", "Would recommend"],
        5: ["Excellent!", "Perfect!", "Amazing product", "Highly recommended", "Best purchase ever!"]
    }
    return random.choice(templates.get(rating, ["No comment"]))
