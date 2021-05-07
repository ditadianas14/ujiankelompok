import mysql.connector
import random, datetime, time

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="DitaDianaSari14",
  database="ac"
)
mycursor = mydb.cursor()

def Menu():
    print("SIMULATOR MESIN")
    print("1. Data Monitoring HVAC")
    print("2. Refresh Data Monitoring HVAC")
    print("---------------------")
    print("3. Exit Program")
    print()
    choice = int(input("Enter here: "))

    if(choice==1):
        for i in range(10):
            now = datetime.datetime.now()
            date_time = now.strftime("%d/%m/%Y %H:%M:%S")
            time.sleep(1.5)
            in_con = random.randint(55,65)
            out_con = in_con - 10
            in_evp = random.randint(55,65)
            out_evp = in_evp + 15
            comp = random.randint (50,90)
            room = random.randint (27,35)
            
            mycursor = mydb.cursor()
            mycursor.execute("INSERT INTO monitoring_ac (datetime, in_conden, out_conden, in_evapor, out_evapor, compressor, ambient) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                             (date_time, in_con, out_con, in_evp, out_evp, comp, room))
            mydb.commit()
            print(mycursor.rowcount, "Membaca Kondisi HVAC")     

    if(choice==3):
        exit()

Menu()