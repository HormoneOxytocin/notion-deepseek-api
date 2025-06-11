import base64
import requests

def handler(request):
    try:
        body = request.json()
        image_base64 = body.get("image_base64")

        headers = {
            "Authorization": "Bearer sk-9055d64ab7764e3eb33333a331e4beef",
            "Content-Type": "application/json"
        }

        prompt = "请识别截图中的支付信息，包括：金额、时间、方式、交易对象、备注，输出 JSON 格式。"

        payload = {
            "model": "deepseek-coder-v1.5",
            "messages": [
                {"role": "user", "content": prompt},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            "temperature": 0.2
        }

        response = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=payload)
        result = response.json()["choices"][0]["message"]["content"]

        return {
            "statusCode": 200,
            "body": {
                "parsed": result
            }
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": {
                "error": str(e)
            }
        }
