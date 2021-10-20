from mycroft import MycroftSkill, intent_file_handler


class PisugarBatteryBackup(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('backup.battery.pisugar.intent')
    def handle_backup_battery_pisugar(self, message):
        self.speak_dialog('backup.battery.pisugar')


def create_skill():
    return PisugarBatteryBackup()

