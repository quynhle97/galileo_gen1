import sys
import time
import signal
import mraa
from ctypes import c_bool
from multiprocessing import Process, Queue, Value, Pipe

import MFRC522
import LCD_I2C
from Datafile import Datafile

# 1: Gop thanh 1 Queue, phan loai bang properties type (RFID, SENSOR)
# 2: Class de quan ly database
# 3: Pipe de web lay du lieu

# Get UID from reading Cards
# def sendingWebServer(main_conn):
#     main_conn.send("hello")
#     main_conn.close()


def readingRFID(queueUID, cont):
    # Hook the SIGINT
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    MIFAREReader = MFRC522.MFRC522()
    while cont.value:
        # Scan for card
        start = time.time()
        (status,
         TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # If a card is found
        if status == MIFAREReader.MI_OK:
            print("Card was detected")
            mid = time.time()

            # Get the UID of the card
            (status, uid) = MIFAREReader.MFRC522_Anticoll()

            # If we have the UID, continue
            if status == MIFAREReader.MI_OK:
                # Print UID
                print("Read card UID successful")
                print("time: ", start, mid, time.time())
                useruid = [uid[0], uid[1], uid[2], uid[3]]
                queueUID.put({
                    "type": "RFID_CARD", "payload": useruid
                })


def readingSensorValue(queueSensor, cont, pin):
    # Hook the SIGINT
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    light = mraa.Aio(pin)
    while cont.value:
        # Read interger value
        sensorIntegerLight = light.read()
        queueSensor.put(
            {"type": "LIGHT_SENSOR", "payload": sensorIntegerLight})
        time.sleep(1)


if __name__ == "__main__":
    LIGHT_SENSOR_PIN = 1
    MAX_LIGHT = 70
    continue_reading = Value(c_bool, True)

    filename = 'dataRFID.json'
    fileObj = Datafile(filename, "")

    filename_sensor = 'dataSensor.json'
    fileObjSensor = Datafile(filename_sensor, "")

    lcd = LCD_I2C.lcd()

    queueGetValue = Queue()
    processRfid = Process(
        target=readingRFID, args=(
            queueGetValue,
            continue_reading,
        ))
    processSensor = Process(
        target=readingSensorValue,
        args=(
            queueGetValue,
            continue_reading,
            LIGHT_SENSOR_PIN,
        ))

    try:
        processRfid.start()
        processSensor.start()

        lcd.lcd_display_string("-Welcome DESLAB-", 1)

        print("Start running")
        print("Print continue_reading ", continue_reading.value)

        while True:
            if not queueGetValue.empty():
                item = queueGetValue.get()

                if item['type'] == "RFID_CARD":
                    uid = item['payload']
                    fileObj.setContentFromFile()
                    # Check usr_uid be existed in file
                    username = fileObj.getUsername(uid)
                    if username != "NA":
                        print(username)

                        userstate = fileObj.getState(uid)
                        if userstate == "True":
                            lcd.lcd_display_string(
                                "                       ", 1)
                            lcd.lcd_display_string("Tam biet ", 1)
                            fileObj.updateUserState(uid, "False")
                        else:
                            lcd.lcd_display_string(
                                "                       ", 1)
                            lcd.lcd_display_string("Xin chao ", 1)
                            fileObj.updateUserState(uid, "True")
                        name_split = username.split()
                        len_name = len(name_split)
                        lcd.lcd_display_string_pos(
                            name_split[len_name-1], 1, 9)
                    else:
                        print("main_ while loop_ uid")
                        print(uid)
                        buf = str(uid[0]) + " " + str(uid[1]) + \
                            " " + str(uid[2]) + " " + str(uid[3])
                        lcd.lcd_display_string("                       ", 1)
                        lcd.lcd_display_string(buf, 1)
                    fileObj.saveContentToFile()
                    print(fileObj.getContent())
                elif item['type'] == "LIGHT_SENSOR":
                    valueSensor = item['payload']
                    fileObjSensor.setContentFromFile()
                    oldIntensity = fileObjSensor.getLightIntensity()
                    currentIntensity = fileObj.checkLightIntensity(valueSensor)

                    if currentIntensity != oldIntensity:
                        fileObjSensor.updateLightIntensity(currentIntensity)
                        fileObjSensor.updateLightValue(valueSensor)
                        fileObjSensor.saveContentToFile()

                    print(fileObjSensor.getContent())
                    lcd.lcd_display_string("Light Value: 00", 2)
                    lcd.lcd_display_string_pos("   ", 2, 13)
                    lcd.lcd_display_string_pos(str(valueSensor), 2, 13)

    except KeyboardInterrupt:
        with continue_reading.get_lock():
            continue_reading.value = False
        processRfid.join()
        processSensor.join()
        sys.exit(0)
