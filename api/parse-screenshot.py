import requests
import json

def handler(request):
    try:
        body = json.loads(request.body)
        image_base64 = body.get("image_base64")

        if not image_base64:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing image_base64"})
            }

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

        res = requests.post("https://api.deepseek.com/v1/chat/completions", json=payload, headers=headers)
        result = res.json()["choices"][0]["message"]["content"]

        return {
            "statusCode": 200,
            "body": json.dumps({"parsed": result})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
