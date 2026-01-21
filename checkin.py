from http.client import ACCEPTED
import os
import requests
import json
from datetime import datetime

def glados_checkin(cookie):
    url = "https://glados.cloud/api/user/checkin"
    headers = {
        "cookie": cookie,
        "content-type": "application/json;charset=UTF-8",
        "accept": "application/json, text/plain, */*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "referer": "https://glados.cloud/console/checkin",
        "origin": "https://glados.cloud"  
    }
    data = {"token": "glados.cloud"}
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        # 打印状态和响应（便于调试）
        #print(f"[DEBUG] Status Code: {response.status_code}")
        #print(f"[DEBUG] Response Body: {response.text}")
        
        # 检查 HTTP 状态
        if response.status_code != 200:
            return False, f"HTTP {response.status_code}", None
        
        result = response.json()
        
        # ✅ 正确判断：检查 code 字段
        if result.get("code") == 0:
            message = result.get("message", "Success")
            # 从 data[0].balance 获取剩余天数（新版结构）
            days_left = "Unknown"
            if "data" in result and isinstance(result["data"], list) and len(result["data"]) > 0:
                balance = result["data"][0].get("balance")
                if balance is not None:
                    days_left = str(balance)
            return True, message, days_left
        else:
            # API 返回业务错误（如已签到、cookie 失效）
            error_msg = result.get("message", "Unknown API error")
            return False, f"API Error: {error_msg}", None
            
    except json.JSONDecodeError:
        return False, "Invalid response: Not JSON format (possibly blocked or redirected)", None
    except Exception as e:
        return False, f"Request failed: {str(e)}", None

def send_wechat_notification(send_key, title, content):
    url = f"https://sctapi.ftqq.com/{send_key}.send"
    data = {
        "title": title,
        "desp": content
    }
    
    try:
        response = requests.post(url, data=data)
        return response.json().get('code') == 0
    except Exception as e:
        print(f"Failed to send notification: {e}")
        return False

def main():
    cookie = os.getenv('GLADOS_COOKIE')
    #cookie = "koa:sess=eyJ1c2VySWQiOjIzMDc4NiwiX2V4cGlyZSI6MTc5NDc5OTEwODk2OSwiX21heEFnZSI6MjU5MjAwMDAwMDB9; koa:sess.sig=T9mN-dp_AxKBiXP_SJsm2Y7zNAE"
    send_key = os.getenv('SERVERCHAN_SENDKEY')
    
    if not cookie:
        print("❌ GLADOS_COOKIE is not set")
        return
    
    checkin_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    success, message, days_left = glados_checkin(cookie)
    
    if success:
        title = f"🎉 Glados 签到成功 - {checkin_time}"
        content = f"""
### 签到结果
- 消息: {message}
- 剩余天数: {days_left}
- 时间: {checkin_time}
        """
    else:
        title = f"❌ Glados 签到失败 - {checkin_time}"
        content = f"""
### 签到失败
- 错误信息: {message}
- 时间: {checkin_time}

> 💡 建议检查 GLADOS_COOKIE 是否有效（有效期通常为 30 天）
        """
    
    if send_key:
        notification_sent = send_wechat_notification(send_key, title, content)
        print(f"Notification sent: {notification_sent}")
    
    print(title)
    print(content)

if __name__ == "__main__":
    main()
