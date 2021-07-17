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
        get_net_value(bot)
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

    if text.startswith("/url"):
        get_url(bot)

    if text.startswith("/now"):
        get_net_value(bot)

    if text.startswith("/high"):
        get_highest_value(bot)

    if text.startswith("/low"):
        get_lowest_value(bot)


def get_fund_data():
    """取得 MoneyDJ 基金資料"""
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    overview_table = soup.select_one("#article > form > table.t01 > tr:nth-child(2)")
    # 淨值日期
    net_value_date = overview_table.select_one("td:nth-child(1)").get_text()
    # 最新淨值
    net_value = overview_table.select_one("td:nth-child(2)").get_text()
    # 每日變化
    net_value_change = overview_table.select_one("td:nth-child(3)").get_text()
    # 最高淨值(年)
    net_value_highest = overview_table.select_one("td:nth-child(4)").get_text()
    # 最低淨值(年)
    net_value_lowest = overview_table.select_one("td:nth-child(5)").get_text()

    return {
        "net_value_date": net_value_date,
        "net_value": net_value,
        "net_value_change": net_value_change,
        "net_value_highest": net_value_highest,
        "net_value_lowest": net_value_lowest,
    }


def get_url(bot):
    """回傳抓取的 URL"""
    bot.sendMessage(chat_id=MY_CHAT_ID, text=URL)


def get_net_value(bot):
    """回傳現在淨值"""
    fund_data = get_fund_data()
    net_value_date = fund_data.get("net_value_date")
    net_value = fund_data.get("net_value")
    net_value_change = fund_data.get("net_value_change")
    text = f"淨值日期:{net_value_date}, 最新淨值:{net_value}, 每日變化:{net_value_change}"
    bot.sendMessage(chat_id=MY_CHAT_ID, text=text)


def get_highest_value(bot):
    """回傳最高淨值(年)"""
    fund_data = get_fund_data()
    net_value_highest = fund_data.get("net_value_highest")
    text = f"最高淨值(年):{net_value_highest}"
    bot.sendMessage(chat_id=MY_CHAT_ID, text=text)


def get_lowest_value(bot):
    """回傳最低淨值(年)"""
    fund_data = get_fund_data()
    net_value_lowest = fund_data.get("net_value_lowest")
    text = f"最低淨值(年):{net_value_lowest}"
    bot.sendMessage(chat_id=MY_CHAT_ID, text=text)
