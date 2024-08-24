from hotel_scrapper.scraper import Scraper
from hotel_scrapper.csv_utils import  initialize_csv


def main():
    # Example usage
    urls = [
        "https://www.ikyu.com/?are=120240&lgp=1039&ppc=2&rc=1",
        # Add more URLs as needed
    ]

    # initialize the CVS with the header
    initialize_csv()

    scraper = Scraper()
    scraper.run(urls)


if __name__ == "__main__":
    main()
