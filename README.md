# My Daily Fund Bot

## 功能

使用 AWS Lambda 搭配 EventBridge (CloudWatch Event) 定時發送每日資料至 Telegram

1. [MoneyDJ](/lambda_function.py)

    基金資料, 每日更新時間約為 9:30 ~ 10:00 之間

    EventBridge Schedule expression: `cron(0 2 ? * TUE-SAT *)`

1. [Yahoo Finance](/yahoo_finance.py)

    美股資料, 每日收盤時間為 04:00 (UTC+8), 夏令 05:00 (UTC+8)

    EventBridge Schedule expression: `cron(30 21 ? * MON-FRI *)`

## 參考資料

### 部署

要把 package 都包進 zip, 再上傳到 AWS Lambda

### layer

另外一個做法是把 package 包成 zip, 放到 layer 內, 如果是 python, 要在 zip 內新增一個 python 資料夾

參考以下連結的 Include library dependencies in a layer

[Creating and sharing Lambda layers - AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html)

```text
pillow.zip
│ python/PIL
└ python/Pillow-5.3.0.dist-info
```

### AWS Lambda 範例

[教學課程：在 Python 3.8 中建立 Lambda 函數 - AWS Lambda](https://docs.aws.amazon.com/zh_tw/lambda/latest/dg/python-package-create.html)

[Building a Telegram Bot with AWS API Gateway and AWS Lambda - DEV Community](https://dev.to/nqcm/-building-a-telegram-bot-with-aws-api-gateway-and-aws-lambda-27fg)

### 設定 webhook

url 為 API Gateway 的 URL

`https://api.telegram.org/bot{token}/setWebhook?url=https://{restapi_id}.execute-api.{region}.amazonaws.com/{stage_name}/`

會回傳

```json
{"ok":true,"result":true,"description":"Webhook was set"}
```

[setwebhook - Telegram Bot API](https://core.telegram.org/bots/api#setwebhook)

[在 Amazon API Gateway 中叫用 REST API - Amazon API Gateway](https://docs.aws.amazon.com/zh_tw/apigateway/latest/developerguide/how-to-call-api.html)

### 查看 webhook 資訊

`https://api.telegram.org/bot{token}/getWebhookInfo`

[getwebhookinfo - Telegram Bot API](https://core.telegram.org/bots/api#getwebhookinfo)

### 設定 command

可以用 @botfather, /setcommands

[How to show options in telegram bot? - Stack Overflow](https://stackoverflow.com/questions/34457568/how-to-show-options-in-telegram-bot)

[setmycommands - Telegram Bot API](https://core.telegram.org/bots/api#setmycommands)

### python-telegram-bot

[Extensions – Your first Bot · python-telegram-bot/python-telegram-bot Wiki](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-Your-first-Bot)

[Webhooks · python-telegram-bot/python-telegram-bot Wiki](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks)

### Beautiful Soup

[css-selectors - Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#css-selectors)
