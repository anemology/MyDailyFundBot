import json

import requests
from bs4 import BeautifulSoup
from telegram import Bot, Update

URL = "https://www.moneydj.com/funddj/ya/yp010001.djhtm?a=FTZ11"
TOKEN = "<telegram_token>"
MY_CHAT_ID = "<your_chat_id>"


def lambda_handler(event, context):
    bot = Bot(TOKEN)

    # EventBridge (CloudWatch Events)
    # 定期執行的排程
    if event.get("source") == "aws.events":
        fund_data = FundData(URL)
        send_message(bot, fund_data.get_net_value())
        return

    # 判斷是 post 以及有 body 才往下走, 代表是從 telegram 發來的 webhook
    try:
        if event["requestContext"]["http"]["method"] != "POST" or not event.get("body"):
            return {"statusCode": 200, "body": json.dumps("Add layers!")}
    except KeyError:
        pass

    update = Update.de_json(json.loads(event.get("body")), bot)
    chat_id = update.message.chat.id
    text = update.message.text

    response_text = text
    if text == "/start":
        response_text = "Started!"
        bot.sendMessage(chat_id=chat_id, text=response_text)
        return

    if text.startswith("/url"):
        send_message(bot, URL)
        return
    
    fund_data = FundData(URL)
    if text.startswith("/now"):
        send_message(bot, fund_data.get_net_value())
        return

    if text.startswith("/high"):
        send_message(bot, fund_data.get_highest_value())
        return

    if text.startswith("/low"):
        send_message(bot, fund_data.get_lowest_value())
        return


class FundData():
    def __init__(self, url):
        """取得 MoneyDJ 基金資料"""
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        overview_table = soup.select_one("#article > form > table.t01 > tr:nth-child(2)")
        # 淨值日期
        self.net_value_date = overview_table.select_one("td:nth-child(1)").get_text()
        # 最新淨值
        self.net_value = overview_table.select_one("td:nth-child(2)").get_text()
        # 每日變化
        self.net_value_change = overview_table.select_one("td:nth-child(3)").get_text()
        # 最高淨值(年)
        self.net_value_highest = overview_table.select_one("td:nth-child(4)").get_text()
        # 最低淨值(年)
        self.net_value_lowest = overview_table.select_one("td:nth-child(5)").get_text()

    def get_net_value(self):
        """現在淨值"""
        return f"淨值日期:{self.net_value_date}, 最新淨值:{self.net_value}, 每日變化:{self.net_value_change}"

    def get_highest_value(self):
        """最高淨值(年)"""
        return f"最高淨值(年):{self.net_value_highest}"

    def get_lowest_value(self):
        """最低淨值(年)"""
        return f"最低淨值(年):{self.net_value_lowest}"


def send_message(bot, text):
    """回傳訊息"""
    bot.sendMessage(chat_id=MY_CHAT_ID, text=text)
