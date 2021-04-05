import json

import requests
from bs4 import BeautifulSoup

URL = "https://www.moneydj.com/funddj/ya/yp010001.djhtm?a=FTZ11"


def lambda_handler(event, context):
    # TODO implement
    return {"statusCode": 200, "body": json.dumps("Hello from Lambda!")}


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


def get_url():
    """回傳抓取的 URL"""
    # TODO send_message
    pass
