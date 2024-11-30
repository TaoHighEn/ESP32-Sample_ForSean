import network
import time
import urequests
import dht
from machine import Pin,Timer

# Wi-Fi 設定
SSID = 'androidALN'
PASSWORD = '00000000'

# DHT11 感測器設定
dht_pin = Pin(15)  # 連接到 GPIO 15
sensor = dht.DHT11(dht_pin)  # 使用 DHT22 感測器

# 連接 Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)  # 取得 WLAN 物件
    wlan.active(True)  # 啟用 WLAN
    if not wlan.isconnected():  # 如果沒有連接
        print('network connecting')
        wlan.connect(SSID, PASSWORD)  # 連接到 Wi-Fi
        while not wlan.isconnected():  # 等待連接完成
            time.sleep(1)
    print('Wi-Fi connected', wlan.ifconfig())  # 顯示 IP 地址

# 呼叫 Web API 範例
def call_web_api(temp,humi):
    url = 'http://192.168.40.65:5231/api/Test'  # 替換為你的 Web API URL
    headers = {'Content-Type': 'application/json'}
    data = {'TEMP': temp, 'HUMI': humi}  # 根據需求構造你的請求資料
    
    try:
        # 發送 POST 請求
        response = urequests.post(url, json=data, headers=headers)
        print('status code:', response.status_code)  # 顯示 HTTP 回應狀態碼
        print('Response Content:', response.text)  # 顯示回應內容
        response.close()  # 關閉回應
    except Exception as e:
        print('Error:', e)

def measureTemp(self):
    try:
        sensor.measure() # 測量
        temp = sensor.temperature() # 取得溫度
        humi = sensor.humidity() # 取得濕度
        temp_humi = "%2d℃/%2d%%" % (temp, humi) # 格式代文字
        print(temp_humi)
        call_web_api(temp,humi)
        print('123')
    except Exception as e:
        print('Error',e)

# 主程式
def main():
    connect_wifi()  # 先連接 Wi-Fi
    timer1=Timer(1)
    timer1.init(period=3000, mode=Timer.PERIODIC, callback=measureTemp) # 每隔3秒執行 measureTemp
    #call_web_api()  # 呼叫 Web API

# 執行主程式
main()