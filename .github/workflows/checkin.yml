import os
import requests
import json
from datetime import datetime

def glados_checkin(cookie):
    url = "https://glados.rocks/api/user/checkin"
    headers = {
        "cookie": cookie,
        "content-type": "application/json",
    }
    data = {"token": "glados.one"}
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        result = response.json()
        
        if 'message' in result and 'list' in result:
            message = result['message']
            days_left = result['list'][0]['balance']
            return True, message, days_left
        else:
            return False, "Invalid response format", None
            
    except Exception as e:
        return False, str(e), None

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
    # 从环境变量获取配置
    cookie = os.getenv('GLADOS_COOKIE')
    send_key = os.getenv('SERVERCHAN_SENDKEY')
    
    if not cookie:
        print("GLADOS_COOKIE is not set")
        return
    
    # 执行签到
    checkin_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    success, message, days_left = glados_checkin(cookie)
    
    # 准备通知内容
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
        """
    
    # 发送微信通知
    if send_key:
        notification_sent = send_wechat_notification(send_key, title, content)
        print(f"Notification sent: {notification_sent}")
    
    # 输出结果到日志
    print(title)
    print(content)

if __name__ == "__main__":
    main()
