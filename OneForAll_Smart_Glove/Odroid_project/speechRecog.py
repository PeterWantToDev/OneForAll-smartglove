import speech_recognition as sr
import pyaudio
import odroid_wiringpi as wpi
import time

# Configure the UART port with defined pins
#ser = serial.Serial("/dev/ttyS1", baudrate=115200, timeout=1)
serial = wpi.serialOpen('/dev/ttyS1', 115200);
def process_voice_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)
        return command
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that.")
        return ""
    except sr.RequestError:
        print("Sorry, there was an issue connecting to the service.")
        return ""

while True:
    #wpi.serialPuts(serial,'1')
    voice_command = process_voice_command()
    if voice_command:
        print(voice_command)
        if voice_command == "open browser":
            value_to_send = '1'
        elif voice_command == "safe mode":
            value_to_send = '2'
        elif voice_command == "turbo mode":
            value_to_send = '3'
        elif voice_command == "task manager":
            value_to_send = '4'
        elif voice_command == "switch app":
            value_to_send = '5'
        elif voice_command == "scroll":
            value_to_send = '6'
        elif voice_command == "open notepad":
            value_to_send = '7'
        elif voice_command == "capture":
            value_to_send = '8'
        elif voice_command == "go to facebook":
            value_to_send = '9'
        elif voice_command == "volume up":
            value_to_send = '10'
        elif voice_command == "volume down":
            value_to_send = '11'
        elif voice_command == "volume mute":
            value_to_send = '12'
        elif voice_command == "lock screen":
            value_to_send = '13'
        elif voice_command == "control panel":
            value_to_send = '14'
        elif voice_command == "terminal start":
            value_to_send = '15'
        elif voice_command == "powershell start":
            value_to_send = '16'
        elif voice_command == "device manager":
            value_to_send = '17'
        elif voice_command == "open calculator":
            value_to_send = '18'
        elif voice_command == "close app":
            value_to_send = '19'
        elif voice_command == "new tab":
            value_to_send = '20'
        elif voice_command == "type my name":
            value_to_send = '21'
        elif voice_command == "change language":
            value_to_send = '22'
        elif voice_command == "sleep computer":
            value_to_send = '23'
        elif voice_command == "restart computer":
            value_to_send = '24'
        elif voice_command == "shut down":
            value_to_send = '25'                                

        else:
            value_to_send = '0'  # Default value for unrecognized commands

        try:
            # Send the value over UART
            #ser.write(str(value_to_send).encode
            wpi.serialPuts(serial, value_to_send)
            print("Value sent:", value_to_send)

            # Add a delay (if needed)
            time.sleep(0.5)  # Sleep for 1 second

        except:
            pass
wpi.serialClose(serial)