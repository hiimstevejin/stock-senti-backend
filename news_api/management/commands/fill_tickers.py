import pandas as pd
from django.core.management.base import BaseCommand
from news_api.models import Ticker


class Command(BaseCommand):
    help = "Populate Ticker table with S&P 500 compnaies from Wikipedia"

    def handle(self, *args, **kwargs):
        url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        table = pd.read_html(url)[0]

        count = 0

        for _, row in table.iterrows():
            symbol = row["Symbol"].strip().upper()
            name = row["Security"].strip()
            Ticker.objects.update_or_create(symbol=symbol, defaults={"name": name})
            count += 1
        self.stdout.write(self.style.SUCCESS(f"Loaded {count} tickers into DB"))
