import csv
import os

csv_file_path = os.path.join(os.getcwd(), '../data/scraped_data.csv')


def initialize_csv():
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Name', 'Location', 'Ratings', 'Category', 'Category Details', 'Points', 'Pricing'])


def save_to_csv(name, location, ratings, category, category_details, points, pricing):
    with open(csv_file_path, 'a', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([name, location, ratings, category, category_details, points, pricing])
