import os
from datetime import datetime, timedelta
from mycroft import MycroftSkill, intent_file_handler

def getBattery():
    stream=os.popen("echo 'get battery' | nc -q 0 127.0.0.1 8423 | sed -e 's/battery: //' -e 's/\..*//'")
    output = stream.read()
    return(output.strip())
"""
This is for newer PiSugar hardware; please check documentation for older hardare as I have none available for testing
"""
def getCharger():
    stream = os.popen("echo 'get battery_power_plugged' | nc -q 0 127.0.0.1 8423| sed -e's/battery_power_plugged: //' | tr '[:lower:]' '[:upper:]'")
    output = stream.read()
    return(output.strip())

class PisugarBatteryBackup(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.b5 = True
        self.b10 = True
        self.b15 = True
        self.b20 = True
        self.b25 = True
        self.b50 = True
        self.b75 = True
        self.autonomous = True
        self.pluggedIn = False

    def initialize(self):
        # Battery charge checker 
        self.schedule_repeating_event(self.__check_battery, datetime.now(),
                                      60, name='batteryBackup')

    def resetFlags(self):
        """Retting flag handler

        Reset all flags when the charger is plugged in
        """
        self.b5 = True
        self.b10 = True
        self.b15 = True
        self.b20 = True
        self.b25 = True
        self.b50 = True
        self.b75 = True
        self.pluggedIn = True

    @intent_file_handler('battery.pisugar.intent')
    def handle_battery_pisugar(self, message):
        self.speak_dialog('battery.pisugar',{'percent': getBattery()})

    @intent_file_handler('charger.pisugar.intent')
    def handle_charger_pisugar(self, message):
        if getCharger() == 'TRUE':
            charge = ' charging'
        else:
            charge = ' not charging'
        self.speak_dialog('charger.pisugar',{'charging': charge})

    def __check_battery(self, message):
        """Repeating event handler.

        Checking if charger plugged in; if not, check battery status.
        """

        if getCharger() == 'TRUE':
            if self.pluggedIn == False:
#                self.speak('Thanks, I needed that!')
                self.speak_dialog('charging.pisugar')
            self.resetFlags()
        else:
            self.pluggedIn = False
            batteryPercent = int(getBattery())

            if batteryPercent <= 5 and self.b5 == True:
                self.b5 = False
                self.speak(f'I will shutdown if you do no recharge soon. Battery Charge is {batteryPercent}%')
            elif batteryPercent <= 10 and self.b10 == True:
                self.b10 = False
                self.speak(f'Please recharge soon. Battery Charge is {batteryPercent}%')
            elif batteryPercent <= 15 and self.b15 == True:
                self.b15 = False
                self.speak(f'Please recharge soon. Battery Charge is {batteryPercent}%')
            elif batteryPercent <= 20 and self.b20 == True:
                self.b20 = False
                self.speak(f'Please recharge soon. Battery Charge is {batteryPercent}%')
            elif batteryPercent <= 25 and self.b25 == True:
                self.b25 = False
                self.speak(f'Please recharge soon. Battery Charge is {batteryPercent}%')
            elif batteryPercent <= 50 and self.b50 == True:
                self.b50 = False
                self.speak(f'Battery Charge is {batteryPercent}%')
            elif batteryPercent <= 75 and self.b75 == True:
                self.b75 = False
                self.speak(f'Battery Charge is {batteryPercent}%')

def create_skill():
    return PisugarBatteryBackup()

