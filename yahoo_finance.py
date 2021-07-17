"""
Yahoo Finance 股票資料

Yahoo api 的參數,
1. interval, 每筆資料的區間, 預設 1m (分)
2. range, 需要多久的資料, 預設 1d (天)

因這邊只需要 meta 內的現價與前一天收盤價, 不用詳細資料,
所以設定 interval 與 range 為 1d 可以減少資料量
"""


from datetime import datetime

import pytz as tz
import requests
from telegram import Bot

URL = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?region=US&lang=en-US&interval=1d&range=1d"
TOKEN = "{telegram_token}"
MY_CHAT_ID = "{your_chat_id}"


def lambda_handler(event, context):
    bot = Bot(TOKEN)

    # EventBridge (CloudWatch Events)
    # 定期執行的排程
    if event.get("source") == "aws.events":
        yahoo_finance = YahooFinance("AMZN")
        send_message(bot, yahoo_finance.get_current_price())
        return


class YahooFinance():
    def __init__(self, symbol, url=URL):
        """取得 Yahoo Finance 資料"""
        url = url.format(symbol=symbol)

        # Yahoo 會阻擋 requests 預設的 user agent
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        response = requests.get(url, headers=headers)
        
        data = response.json()["chart"]["result"][0]

        meta_data = data["meta"]
        self.market_price = meta_data["regularMarketPrice"]
        self.previous_cloe = meta_data["chartPreviousClose"]
        self.date = datetime.now(tz=tz.timezone("America/New_York")).date().isoformat()
        self.symbol = symbol

    def get_current_price(self):
        """回傳現在價格及漲跌幅度 e.g. 146.39, -2.09 (-1.41%)"""
        
        changed = self.market_price - self.previous_cloe
        changed_percent = (changed / self.previous_cloe) * 100
        
        return f"{self.symbol} {self.date} {self.market_price}, {changed:.2f} ({changed_percent:.2f}%)"


def send_message(bot, text):
    """回傳訊息"""
    bot.sendMessage(chat_id=MY_CHAT_ID, text=text)


if __name__ == "__main__":
    y = YahooFinance("AMZN")
    print(y.get_current_price())
