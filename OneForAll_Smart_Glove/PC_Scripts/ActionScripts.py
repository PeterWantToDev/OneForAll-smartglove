import serial
import os
import webbrowser
import pyautogui
import time

ser = serial.Serial('COM3', 115200)  

def open_task_manager():
    os.system("taskmgr")
    time.sleep(3)  # Wait for Task Manager to open
    pyautogui.hotkey('Ctrl', 'Tab')  

def switch_app():
    pyautogui.hotkey('ALT', 'Tab')

    
while True:
    if ser.in_waiting > 0:
        message = ser.readline().decode('utf-8').strip()
        if message == "25":
            print("Received shutdown command. Shutting down...")
            os.system("shutdown /s /t 1")
        elif message == 'sleep':
            print('The device going DEEP SLEEP')
        elif message == "1":
            print("Received open browser command. Opening browser...")
            webbrowser.open('https://www.google.com')  
        elif message == "2":
            print("Received safe mode command. Changing to safe battery mode...")
            os.system("powercfg /setactive 64a64f24-65b9-4b56-befd-5ec1eaced9b3")
        elif message == "3":
            print("Received turbo mode command. Changing to turbo battery mode...")
            os.system("powercfg /setactive 6fecc5ae-f350-48a5-b669-b472cb895ccf")
        elif message == "4":
            print("Received task manager command. Opening Task Manager - Performance tab...")
            open_task_manager()
        elif message == "5" :
            print("Received switch app command. Switching app...")
            switch_app()
        elif message == "6" :
            print("Received scroll command.")
            pyautogui.scroll(-10)
        elif message == "7":
            print("Received open notepad command . Performing custom action...")
            os.system("start notepad.exe")
        elif message == "8":
            print("Received screenshot command . Performing custom action...")
            screenshot = pyautogui.screenshot()
            screenshot.save("screenshot.png")
        elif message == "9":
            print("Received Open Facebook command . Performing custom action...")
            webbrowser.open('https://www.facebook.com')
        elif message == "10":
            print("Received volumeup command . Performing custom action...")
            pyautogui.press('volumeup')
        elif message == "11":
            print("Received volumdown command . Performing custom action...")
            pyautogui.press('volumedown')
        elif message == "12":
            print("Received mute command . Performing custom action...")
            pyautogui.press('volumemute')
        elif message == "13":
            print("Received lock screen command . Performing custom action...")
            pyautogui.hotkey('winleft', 'l')
        elif message == "14":
            print("Received open control panel command . Performing custom action...")
            os.system("control")
        elif message == "15":
            print("Received open cmd command . Performing custom action...")
            os.system("start cmd")
        elif message == "16":
            print("Received open powershell command . Performing custom action...")
            os.system("start powershell")
        elif message == "17":
            print("Received device manager command . Performing custom action...")
            os.system("devmgmt.msc")
        elif message == "18":
            print("Received open calculator command . Performing custom action...")
            os.system("start calc")
        elif message == '19':
            print("Received close current window command. Performing custom action...")
            pyautogui.hotkey('alt', 'f4')
        elif message == "20":
            print("Received open new browser tab command. Performing custom action...")
            pyautogui.hotkey('ctrl', 't')
        elif message == '21':
            print("Received  typing my name command. Performing custom action...")
            pyautogui.write("6410110305, Poramee Madadam")
        elif message == '22':
            print('Received  change language command. Performing custom action...')
            pyautogui.hotkey('alt', 'shift')
        elif message == '23':
            print('Received  sleep pc command. Performing custom action...')
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        elif message == '24':
            print('Received  restart pc command. Performing custom action...')
            os.system("shutdown /r /t 1")
