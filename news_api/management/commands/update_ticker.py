# news_api/management/commands/update_ticker_info.py
import yfinance as yf
from django.core.management.base import BaseCommand
from news_api.models import Ticker

class Command(BaseCommand):
    help = "Fetch and update detailed info for all tickers"

    def handle(self, *args, **kwargs):
        # change this to conditionally uplaod company info w/ yfinance
        tickers = Ticker.objects.all()
        total = tickers.count()
        success = 0

        for ticker in tickers:
            try:
                yf_ticker = yf.Ticker(ticker.symbol)
                info = yf_ticker.info
                ticker.name = info.get("shortName","")
                ticker.sector = info.get("sector","")
                ticker.industry = info.get("industry","")
                ticker.website = info.get("website","")
                ticker.market_cap = info.get("marketCap","")
                ticker.headquarters = info.get("city","")
                ticker.save()

                success += 1
                self.stdout.write(f"Updated {ticker.symbol} ({success}/{total})")
            except Exception as e:
                self.stdout.write(f"Failed {ticker.symbol}: {e}")

        self.stdout.write(self.style.SUCCESS(f"Done updating {success}/{total} tickers"))
