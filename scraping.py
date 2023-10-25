import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
from databases import create_database

def scrape_and_save_data(url_base, output_file, output_format):
    try:
        if output_format == "SQLite":
            db_file = "AppStoreData.db"
            engine = create_engine(f"sqlite:///{db_file}")
            conn = engine.connect()
            base_url = url_base
            page_num = 1
            reviews_per_page = 10
            rating_values = []
            review_dates = []
            review_contents = []

            while True:
                url = f"{base_url}&showAllReviews=true&page={page_num}"
                response = requests.get(url)
                soup = BeautifulSoup(response.content, "html.parser")
                ratings = soup.find_all("span", class_="F7XJmb")
                rating_values.extend([rating.get("data-number") for rating in ratings])
                dates = soup.find_all("span", class_="bp9Aid")
                review_dates extend([date.get_text() for date in dates])
                reviews = soup.find_all("div", class_="h3YV2d")
                review_contents.extend([review.get_text() if review else None for review in reviews])

                if len(ratings) == 0:
                    break
                page_num += 1
                if page_num == 20:
                    break

            min_length = min(len(rating_values), len(review_dates), len(review_contents))
            rating_values = rating_values[:min_length]
            review_dates = review_dates[:min_length]
            review_contents = review_contents[:min_length]

            comments_data = {
                "Date": review_dates,
                "Rating": rating_values,
                "Review": review_contents
            }
            comments_df = pd.DataFrame(comments_data)

            comments_df.to_sql("comments_data", conn, if_exists="replace", index=False)

            conn.close()

        elif output_format == "XLSX":
            # Código para coletar dados em formato XLSX
            pass

    except Exception as e:
        # Tratamento de erros
        pass
