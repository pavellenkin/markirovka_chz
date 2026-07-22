import mysql.connector
import pymysql
from getpass import getpass
from mysql.connector import errorcode
from mysql.connector import connect, Error



"""
user='MOBILE_CB_User',
password='J0xoer|VmE@zte8E',
"""



def connection_lord():
    try:
        with connect(
                host="192.168.1.3",
                user="MOBILE_CB_User",
                port=3000,
                password="J0xoer|VmE@zte8E",
        ) as connection:
            print(connection)
    except Error as e:
        print(e)