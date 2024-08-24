from hotel_scrapper.scraper import Scraper


def main():
    # Example usage
    urls = [
        "https://www.ikyu.com/?are=120240&lgp=1039&ppc=2&rc=1",
        # Add more URLs as needed
    ]

    scraper = Scraper()
    scraper.run(urls)


if __name__ == "__main__":
    main()
