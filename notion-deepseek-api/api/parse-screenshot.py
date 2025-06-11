import requests

def handler(request):
    try:
        data = request.json()
        image_base64 = data.get("image_base64")

        # 调用 Deepseek API
        headers = {
            "Authorization": "Bearer sk-9055d64ab7764e3eb33333a331e4beef",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "deepseek-coder-v1.5",
            "messages": [
                {"role": "user", "content": "请识别截图中的支付信息...输出 JSON"},
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
