#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import sys
import atexit
import csv
import time
from datetime import datetime

import serial
from serial.tools.list_ports import comports
from serial.tools import hexlify_codec


def ask_for_port():
    sys.stderr.write("\n--- Available ports:\n")
    ports = []
    for n, (port, desc, hwid) in enumerate(sorted(comports()), 1):
        sys.stderr.write("--- {:2}: {:20} {!r}\n".format(n, port, desc))
        ports.append(port)
    while True:
        port = input("--- Enter port index or full name: ")
        try:
            index = int(port) - 1
            if not 0 <= index < len(ports):
                sys.stderr.write("--- Invalid index!\n")
                continue
        except ValueError:
            #     pass
            port = ports[len(ports)-1]
        else:
            port = ports[index]
        return port


def ask_baud():
    baud = 115200
    baud = input("--- Enter baudrate: ")

    try:
        sys.stdout.write("---  baudrate: ")
        sys.stdout.write(str(int(baud)))
        # print(int(baud))
    except ValueError:
        sys.stdout.write("115200")
        baud = 115200

    return baud


def printAscii(Ser):
    strLine = ''
    while True:
        bytes_data = Ser.read()
        string_data = str(bytes_data.decode("utf-8"))
        sys.stdout.write(string_data)
        strLine += string_data
        if string_data == '\n':
            strLine = str(strLine + ' UNIX_Time:' + str(datetime.now()))
            # sys.stdout.write(strLine)  # 改行コードまでの文字列
            strLine = strLine.replace(':', ',').replace(
                ' ', ',').replace('\t', ',').replace('\r', '').replace('\n', '')
            dataList = strLine.split(',')
            # print(dataList) #リスト化されたやつ
            addCSV(dataList)
            strLine = ''


def addCSV(list):
    with open('data.csv', 'a', newline='') as data:
        csv.writer(data, lineterminator='\n').writerow(list)
        data.close()


def printData():
    global Ser
    Ser = serial.Serial(serialPort, serialBaud, timeout=None)
    printAscii(Ser)


def exit():
    print('----------------------------------------------')
    print('✨finish!!✨')
    Ser.close()


if __name__ == "__main__":
    atexit.register(exit)

    serialPort = ask_for_port()
    serialBaud = ask_baud()
    printData()
