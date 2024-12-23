import network
import time
import urequests
import dht
import _thread
import socket
from machine import Pin,Timer

# Wi-Fi 設定
SSID = 'Alan'
PASSWORD = '54alan520'
# 連接 Wi-Fi
def connect_wifi():
    times=0
    wlan = network.WLAN(network.STA_IF)  # 取得 WLAN 物件
    wlan.active(True)  # 啟用 WLAN
    if not wlan.isconnected():  # 如果沒有連接
        print('network connecting')
        wlan.connect(SSID, PASSWORD)  # 連接到 Wi-Fi
        while not wlan.isconnected():  # 等待連接完成
            time.sleep(1)
            if times>5:
                print("連接失敗")
                break
    if times>5:
        print("請重新啟動")
    else:
        print('Wi-Fi connected', wlan.ifconfig())  # 顯示 IP 地址

def start_server():
    """啟動Web伺服器"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)

    #加上要控制的GPIO LED
    led_g=Pin(23, Pin.OUT)
    led_y=Pin(22, Pin.OUT)
    led_r=Pin(21, Pin.OUT)
    
    while True:
        try:
            conn, addr = s.accept()
            request = conn.recv(1024).decode()
            if request.find('/led?light=')>0:
                text_start = request.find('light=')
                text_end = request.find(' ',text_start)
                text = request[text_start:text_end].replace('\n','')
                text = text.replace('light=','')
                wlan = network.WLAN(network.STA_IF)
                # wlan.active(True)
                staticIP = wlan.ifconfig()[0]
                if not wlan.isconnected():
                    print(wlan.ifconfig())

                print(text)
                #補上呼叫WebAPI
                if text=="1":
                    led_g.value(1)
                    led_y.value(0)
                    led_r.value(0)
                    response = change_light_api("1",staticIP)
                elif text == "2":
                    led_g.value(0)
                    led_y.value(1)
                    led_r.value(0)
                    response = change_light_api("2",staticIP)
                else:
                    led_g.value(0)
                    led_y.value(0)
                    led_r.value(1)
                    response = change_light_api("3",staticIP)
                
            # 給出回應標頭並設置 CORS 支援
                response_headers = 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n'
                response_headers += 'Access-Control-Allow-Origin: *\r\n'  # 支援跨域請求
                response_headers += '\r\n'

                conn.send(response_headers.encode())
                #conn.send(response.encode())  # 傳送回應內容
                conn.close()

        except Exception as e:
            print('錯誤:', e)
            conn.close()

def change_light_api(l_num,staticip):
    url = 'http://192.168.1.102:5097/Light/LogLightChange'  # 替換為你的 Web API URL
    headers = {'Content-Type': 'application/json'}
    data = {
            'LightNum':int(l_num),
            'SensorIP':staticip
            }  # 根據需求構造你的請求資料
    
    try:
        # 發送 POST 請求
        response = urequests.post(url, json=data, headers=headers)
        print('status code:', response.status_code)  # 顯示 HTTP 回應狀態碼
        response.close()  # 關閉回應
        return response
    except Exception as e:
        print('Error:', e)

# 主程式
def main():
    connect_wifi()  # 先連接 Wi-Fi
    #call_web_api()  # 呼叫 Web API
    start_server()

# 執行主程式
main()