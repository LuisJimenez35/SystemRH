import random
import pymysql
from email.message import EmailMessage
import smtplib
import messagebox
from datetime import date
#-------------------Funcion Inicio---------------#
def prmenust():
    prmst = int(input("{-----------------RH SYSTEM-----------------}\n                  !WELCOME!\n                  1.Login\n                  2.Register\n                  3.Cerrar\n{-------------------------------------------}\n"))
    if prmst == 1:
        login()
    elif prmst == 2:
        print("Register")
        registeruser()
    elif prmst == 3:
        print("{--------------CLOSE RH SYSTEM--------------}")
    else:
        print("\n{------/*Digite una opcion Correcta\*-------}\n")
        prmenust()
      
#-------------------Funcion login---------------#
def login():
    print("\n{-----------------Login System-----------------}")
    username = input("[Digite el user]: \n} ")
    password = input("[Digite el pass]: \n} ")
    print("{-------------------------------------------}")
    mydb = pymysql.connect(host="localhost",user="root",passwd="Halobat17.",database="rhdb")
    cursor = mydb.cursor()
    savequery = "SELECT * FROM users WHERE Usuario=%s AND Pass=%s" # Get the records with these username and password ONLY
    cursor.execute(savequery,(username,password))
    myresult = cursor.fetchall()
    if myresult:
        messagebox.showinfo("LOGIN Corecto",'Bienvenid@'+username)
        consultardatostrabajadores()
    else: 
        messagebox.showerror("LOGIN Fallido","Usuario o Pass no encontrados")
        cursor.close()
        mydb.close()
        cerrarinput = input("   Desea cerrar recuperar el password?\n                  S = Si\n                  N = No\n{-------------------------------------------}\n")
        if cerrarinput.upper() == "S":
            olvidopass()
        elif cerrarinput.upper() == "N":
            print("          ---{Cerrando programa}---\n              <Nos vemos ",username,">")
              
#----------------Funcion para crear nueva contrase??a-----------------
def olvidopass():
    print("\n        {-----Recuperar contrase??a-----}\n")
    inputadmin = input("<Digite su usuario> : ")
    #-----------------Conexion a la Base de datos de los Administradores--------------
    db = pymysql.connect(host="localhost",user="root",passwd="Halobat17.",db="rhdb")
    cur = db.cursor()
    cur.execute("SELECT * FROM users where Usuario ='" +inputadmin+ "'")
    for row in cur.fetchall():
        valicorreo = row[1]
        valiuser = row[0]
        valiSQ = row[2]
    #--------------Creador del codigo random secreto-------------
    randlowercase1 = chr(random.randint(ord('a'), ord('z')))
    randuppercase2 = chr(random.randint(ord('A'), ord('Z')))
    randuppercase3 = chr(random.randint(ord('A'), ord('Z')))
    randuppercase4 = chr(random.randint(ord('a'), ord('z')))
    randuppercase5 = chr(random.randint(ord('A'), ord('Z')))
    randuppercase6 = str(random.randint(0,9))
    secretcode = (randlowercase1+randuppercase2+randuppercase3+randuppercase4+randuppercase5+randuppercase6)
    #------------Enviar el correo de soporte-----------------
    remit = "soportprimeprogram@gmail.com"
    desto = valicorreo
    msj = "Para crear una contrase??a nueva digite el siguiente codigo en el Sistema: "+secretcode
    email = EmailMessage()
    email["From"] = remit
    email["To"] = desto
    email["Subject"] = "Correo de Soporte"
    email.set_content(msj)
    smtp = smtplib.SMTP_SSL("smtp.gmail.com")
    smtp.login(remit, "gbaabtuzmxgxrvhn")
    smtp.sendmail(remit, desto, email.as_string())
    smtp.quit()
    print("\n        ^------Correo Enviado------^\n")
    #---------------Actulizar la nueva contrase??a----------------
    inputcode = input("{Digite el codigo enviado a su correo}: \n")
    if inputcode == secretcode:
        messagebox.showinfo("Secure Code","Codigo Correcto")
        newpass = input("\n1.Digite la nueva contrase??a: \n")
        newpass2 = input("\n2.Confirme la contrase??a: \n")
        if newpass == newpass2:
            newpass3 = newpass
            updated_users = """UPDATE users SET Email = %s,SecurityQuestion = %s,Pass = %s WHERE Usuario = %s;"""
            cur.execute(updated_users, (valicorreo, valiSQ, newpass3, valiuser))
            messagebox.showinfo ("Recuperar Password","Password cambiada con exito")
            db.commit()
            login()
    else:
        print("Error , verifique su correo")
        oprec = input("Volver a intentarlo?\nS=Si\nN=No\n")
        if oprec.upper == "S":
            olvidopass()
        else:
            login()

#--------------------Funcion Registrarse-------------------#
def registeruser():
    print("\n{-----------------Register System-----------------}")
    db = pymysql.connect(host="localhost",user="root",passwd="Halobat17.",database="rhdb")
    curs = db.cursor()
    insert_stmt = (
    "INSERT INTO users(Usuario, Email, SecurityQuestion, Pass)"
    "VALUES (%s, %s, %s, %s)"
    )
    in0 = input("1. Digite el Usuario: ")
    in1 = input("2. Digite el Email: ")
    in2 = input("3. Digite la respuesta a su SQ: ")
    in3 = input("4. Digte la Password: ")
    print("{-------------------------------------------------}/n")
    data = (in0, in1, in2, in3)    
    try:
        curs.execute(insert_stmt, data)
        db.commit()
        messagebox.showinfo("Register","Usuario Registrado")
        prmenust
    except:
        db.rollback()
        messagebox.showerror("Register","Usuario no Registrado")
        prmenust()
          
#-------------------Consulta Trabajadores---------------#
def consultardatostrabajadores():
    print("Sistema Recursos Humanos\n")
    db = pymysql.connect(host="localhost",user="root",passwd="Halobat17.",db="rhdb")
    opciontrabajador = int(input("{----------Menu RH----------}\n1.Trabajadores Disponibles\n2.Ver Datos de Trabajadores\n3.Cambiar Datos trabajadores\n4.Enviar Correo a Trabajador\n5.Agregar Trabajador\n6.Eiminar Trabajador\n7.Pago Trabajadores\n8.Reiniciar Salarios\n9.Salir\n{---------------------------}\n"))
    #-------------------Cosnultar la Lista de trabajadores general---------------#
    if opciontrabajador == 1:
        print("-----Trabajadores Disponibles-----")
        cur = db.cursor()
        cur.execute("SELECT * FROM trabajadores")
        for Dniwork, FullName, FullLastName, Birthday, Location, DateOfHire, Position, Cellphone, Email, Salary in cur.fetchall() :
            print("\nDNI:",Dniwork, "\nNombre Completo:",FullName,FullLastName, "\nPuesto:",Position,"\nEmail:",Email,"\n")
        consultardatostrabajadores()
    #-------------------Consultar datos trabajadores por separado---------------#
    elif opciontrabajador == 2:
        print("Ver Datos de Trabajadores")
        inputOt2 = input("Escriba la cedula del trabajador: ")
        cur = db.cursor()
        cur.execute("SELECT * FROM trabajadores where Dniwork ='" +inputOt2+ "'")
        for row in cur.fetchall():
            print("\nCedula: ",row[0],"\nNombre Completo: ",row[1],row[2],"\nFecha de Nacimiento: ",row[3],"\nUbicacion: ",row[4],"\nFecha de Contratacion: ",row[5],"\nPuesto: ",row[6],"\nTelefono: ",row[7],"\nEmail: ",row[8],"\nSalario: ",row[9],"\n")
            consultardatostrabajadores()
    #-------------------Cambiar Datos de Trabajadores---------------#
    elif opciontrabajador == 3:
        print("Cambiar Datos de Trabajadores")
        inputOt3 = input("Digite la Cedula del Trabajador ")
        cur = db.cursor()
        cur.execute("SELECT * FROM trabajadores where Dniwork ='" +inputOt3+ "'")
        for row in cur.fetchall():
            Op0 = row[0]
            Op1 = row[1]
            Op2 = row[2]
            Op3 = row[3]
            Op5 = row[5]
            Op9 = row[9]
        newlocation = input("Digite la nueva Ubicacion ")
        newposition = input("Digite el nuevo titulo ")
        newcelllphone = input("Digite el nuevo Telefono ")
        newEmail = input("Digite el nuevo Email ")
        updated_email =  """UPDATE trabajadores
                            SET FullName = %s,
                                FullLastName = %s,
                                Birthday = %s,
                                Location = %s,
                                DateOfHire = %s,
                                Position = %s,
                                Cellphone = %s,
                                Email = %s,
                                Salary = %s
                            WHERE DNI = %s;"""
        cur.execute(updated_email, (Op1, Op2, Op3, newlocation, Op5, newposition, newcelllphone,newEmail,Op9,Op0))
        db.commit()
        consultardatostrabajadores()
    #-------------------Enviar Correo a Trabajadores---------------#
    elif opciontrabajador == 4:
        print("Enviar Correo a Trabajador")
        inputOt4 = input("Digite la Cedula del Trabajador ")
        cur = db.cursor()
        cur.execute("SELECT * FROM trabajadores where DNI ='" +inputOt4+ "'")
        for row in cur.fetchall():
            Op8 = row[8]
        msjOT4 = input("Escriba el mensaje que va a enviar")
        remit = "soportprimeprogram@gmail.com"
        desto = Op8
        msj = msjOT4
        email = EmailMessage()
        email["From"] = remit
        email["To"] = desto
        email["Subject"] = "Correo de Recursos Humanos"
        email.set_content(msj)
        smtp = smtplib.SMTP_SSL("smtp.gmail.com")
        smtp.login(remit, "gbaabtuzmxgxrvhn")
        smtp.sendmail(remit, desto, email.as_string())
        smtp.quit()
        print("Correo Enviado con Exito")
        consultardatostrabajadores()
    #-------------------Agregar Trabajadores---------------#
    elif opciontrabajador == 5:
        print("Agregar Trabajador")
        consultardatostrabajadores()
    #-------------------Borrar Trabajadores---------------#
    elif opciontrabajador == 6:
        print("Eliminar Trabajador")
        assword = input("Digite el pass: ")
        mydb = pymysql.connect(host="localhost",user="root",passwd="Halobat17.",database="rhdb")
        cursor = mydb.cursor()
        savequery = "SELECT * FROM users WHERE Usuario=%s AND Pass=%s" # Get the records with these username and password ONLY
        cur.execute(updated_email, (Op1, Op2, Op3, newlocation, Op5, newposition, newcelllphone, newEmail,Op9,Op0))
        db.commit()
        messagebox.showinfo("Actualizacion de datos","Los datos fueron actualizados con exito")
        consultardatostrabajadores()
    #-------------------Enviar Correo a Trabajadores---------------#
    elif opciontrabajador == 4:
        print("Enviar Correo a Trabajador")
        inputOt4 = input("Digite la Cedula del Trabajador ")
        cur = db.cursor()
        cur.execute("SELECT * FROM trabajadores where Dniwork ='" +inputOt4+ "'")
        for row in cur.fetchall():
            Op8 = row[8]
        msjOT4 = input("Escriba el mensaje que va a enviar")
        remit = "soportprimeprogram@gmail.com"
        desto = Op8
        msj = msjOT4
        email = EmailMessage()
        email["From"] = remit
        email["To"] = desto
        email["Subject"] = "Correo de Recursos Humanos"
        email.set_content(msj)
        smtp = smtplib.SMTP_SSL("smtp.gmail.com")
        smtp.login(remit, "gbaabtuzmxgxrvhn")
        smtp.sendmail(remit, desto, email.as_string())
        smtp.quit()
        print("Correo Enviado con Exito")
        consultardatostrabajadores()
    #-------------------Agregar Trabajadores---------------#
    elif opciontrabajador == 5:
        print("Agregar Trabajador")
        curs = db.cursor()
        insert_stmt = (
        "INSERT INTO trabajadores(Dniwork, FullName, FullLastName, Birthday, Location, DateOfHire, Position, Cellphone, Email, Salary)"
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        in0 = int(input("Digite la Cedula: "))
        in1 = input("Digite el Nombre Completo: ")
        in2 = input("Digite los Apellidos Completos: ")
        in3 = input("Digte la Fecha de Nacimento con el Formato 0/0/0: ")
        in4 = input("Digite la Ubicacion: ")
        in5 = input("Digite la Fecha de contratacion con el Formato 0/0/0: ")
        in6 = input("Digite el Titulo: ")
        in7 = input("Digite el Telefono")
        in8 = input("Digite el Correo")
        data = (in0, in1, in2, in3, in4, in5, in6, in7, in8, 0)
        try:
            curs.execute(insert_stmt, data)
            db.commit()
            consultardatostrabajadores()
        except:
            db.rollback()          
    #-------------------Borrar Trabajadores---------------#
    elif opciontrabajador == 6:
        print("Eliminar Trabajador")
        cursor = db.cursor()
        sql_Delete_query = """Delete from trabajadores where Dniwork = %s"""
        # row to delete
        DNIinput = input("Digite la cedula del trabajador: ")
        cursor.execute(sql_Delete_query, (DNIinput,))
        db.commit()
        print("Record Deleted successfully ")
        if db:
            messagebox.showinfo("Accept",'Se elimino a '+DNIinput)
            consultardatostrabajadores()
        else:
            messagebox.showinfo("Deny",'No se encontro a '+DNIinput)
            consultardatostrabajadores()
    #-------------------Pago Quincenal---------------#
    elif opciontrabajador == 7:
        print("Pago Quincenal: ")
        today = date.today()
        payday = today.strftime("%b-%d-%Y")
        Bach = 280000
        Lic = 360000
        Mast = 450000
        Doc = 510000
        inputOt3 = input("Digite la Cedula del Trabajador ")
        cur = db.cursor()
        cur.execute("SELECT * FROM trabajadores where Dniwork ='" +inputOt3+ "'")
        for row in cur.fetchall():
            Op0 = row[0]
            Op1 = row[1]
            Op2 = row[2]
            Op3 = row[3]
            Op4 = row[4]
            Op5 = row[5]
            Op6 = row[6]
            Op7 = row[7]
            Op8 = row[8]
            Op9 = row[9]
        if Op6 == "Bach":
            Falinput = int(input("Digite las faltas: "))
            calc = 18600 * Falinput
            Resf = Bach - calc
            updated_pay = """UPDATE trabajadores 
                      SET FullName = %s,
                         FullLastName = %s,
                         Birthday = %s,
                         Location = %s,
                         DateOfHire = %s,
                         Position = %s,
                         Cellphone = %s,
                         Email = %s,
                         Salary = %s
                      WHERE Dniwork = %s;"""
            cur.execute(updated_pay, (Op1, Op2, Op3, Op4, Op5, Op6, Op7, Op8, Resf,Op0))
            db.commit()
            refs = str(Resf)
            fallas = str(Falinput)
            messagebox.showinfo("Pago Autorizado", "Puede ver el pago en los datos de los trabajadores")
            remit = "soportprimeprogram@gmail.com"
            desto = Op8
            msj = "Hola de parte de RHSystem al trabajador "+Op1+ Op2+" se le notifica que el "+payday+" se le ha pagado su salario quincenal correspodiente a: "+refs+" colones , esto debido a "+fallas+" faltas cometidas en estos 15 dias , si tiene alguna queja por favor enviar un mensaje a contarhsys@gmail.com"
            email = EmailMessage()
            email["From"] = remit
            email["To"] = desto
            email["Subject"] = "Notificacion de pago Quincenal"
            email.set_content(msj)
            smtp = smtplib.SMTP_SSL("smtp.gmail.com")
            smtp.login(remit, "gbaabtuzmxgxrvhn")
            smtp.sendmail(remit, desto, email.as_string())
            messagebox.showinfo("Pago Notificacacion","Notoficaion enviada con exito")
            smtp.quit()
            consultardatostrabajadores()
        elif Op6 == "Lic":
            Falinput = int(input("Digite las faltas: "))
            calc = 24000 * Falinput
            Resf = Lic - calc
            updated_pay = """UPDATE trabajadores 
                      SET FullName = %s,
                         FullLastName = %s,
                         Birthday = %s,
                         Location = %s,
                         DateOfHire = %s,
                         Position = %s,
                         Cellphone = %s,
                         Email = %s,
                         Salary = %s
                      WHERE Dniwork = %s;"""
            cur.execute(updated_pay, (Op1, Op2, Op3, Op4, Op5, Op6, Op7, Op8, Resf,Op0))
            db.commit()
            refs = str(Resf)
            fallas = str(Falinput)
            messagebox.showinfo("Pago Autorizado", "Puede ver el pago en los datos de los trabajadores")
            remit = "soportprimeprogram@gmail.com"
            desto = Op8
            msj = "Hola de parte de RHSystem al trabajador "+Op1+ Op2+" se le notifica que el "+payday+" se le ha pagado su salario quincenal correspodiente a: "+refs+" colones , esto debido a "+fallas+" faltas cometidas en estos 15 dias , si tiene alguna queja por favor enviar un mensaje a contarhsys@gmail.com"
            email = EmailMessage()
            email["From"] = remit
            email["To"] = desto
            email["Subject"] = "Notificacion de pago Quincenal"
            email.set_content(msj)
            smtp = smtplib.SMTP_SSL("smtp.gmail.com")
            smtp.login(remit, "gbaabtuzmxgxrvhn")
            smtp.sendmail(remit, desto, email.as_string())
            messagebox.showinfo("Pago Notificacacion","Notoficaion enviada con exito")
            smtp.quit()
            consultardatostrabajadores()
        elif Op6 == "Mast":
            Falinput = int(input("Digite las faltas: "))
            calc = 30000 * Falinput
            Resf = Mast - calc
            updated_pay = """UPDATE trabajadores 
                      SET FullName = %s,
                         FullLastName = %s,
                         Birthday = %s,
                         Location = %s,
                         DateOfHire = %s,
                         Position = %s,
                         Cellphone = %s,
                         Email = %s,
                         Salary = %s
                      WHERE Dniwork = %s;"""
            cur.execute(updated_pay, (Op1, Op2, Op3, Op4, Op5, Op6, Op7, Op8, Resf,Op0))
            db.commit()
            refs = str(Resf)
            fallas = str(Falinput)
            messagebox.showinfo("Pago Autorizado", "Puede ver el pago en los datos de los trabajadores")
            remit = "soportprimeprogram@gmail.com"
            desto = Op8
            msj = "Hola de parte de RHSystem al trabajador "+Op1+ Op2+" se le notifica que el "+payday+" se le ha pagado su salario quincenal correspodiente a: "+refs+" colones , esto debido a "+fallas+" faltas cometidas en estos 15 dias , si tiene alguna queja por favor enviar un mensaje a contarhsys@gmail.com"
            email = EmailMessage()
            email["From"] = remit
            email["To"] = desto
            email["Subject"] = "Notificacion de pago Quincenal"
            email.set_content(msj)
            smtp = smtplib.SMTP_SSL("smtp.gmail.com")
            smtp.login(remit, "gbaabtuzmxgxrvhn")
            smtp.sendmail(remit, desto, email.as_string())
            messagebox.showinfo("Pago Notificacacion","Notoficaion enviada con exito")
            smtp.quit()
            consultardatostrabajadores()
        elif Op6 == "Doc":
            Falinput = int(input("Digite las faltas: "))
            calc = 34000 * Falinput
            Resf = Doc - calc
            updated_pay = """UPDATE trabajadores 
                      SET FullName = %s,
                         FullLastName = %s,
                         Birthday = %s,
                         Location = %s,
                         DateOfHire = %s,
                         Position = %s,
                         Cellphone = %s,
                         Email = %s,
                         Salary = %s
                      WHERE Dniwork = %s;"""
            cur.execute(updated_pay, (Op1, Op2, Op3, Op4, Op5, Op6, Op7, Op8, Resf,Op0))
            db.commit()
            refs = str(Resf)
            fallas = str(Falinput)
            messagebox.showinfo("Pago Autorizado", "Puede ver el pago en los datos de los trabajadores")
            remit = "soportprimeprogram@gmail.com"
            desto = Op8
            msj = "Hola de parte de RHSystem al trabajador "+Op1+ Op2+" se le notifica que el "+payday+" se le ha pagado su salario quincenal correspodiente a: "+refs+" colones , esto debido a "+fallas+" faltas cometidas en estos 15 dias , si tiene alguna queja por favor enviar un mensaje a contarhsys@gmail.com"
            email = EmailMessage()
            email["From"] = remit
            email["To"] = desto
            email["Subject"] = "Notificacion de pago Quincenal"
            email.set_content(msj)
            smtp = smtplib.SMTP_SSL("smtp.gmail.com")
            smtp.login(remit, "gbaabtuzmxgxrvhn")
            smtp.sendmail(remit, desto, email.as_string())
            messagebox.showinfo("Pago Notificacacion","Notoficaion enviada con exito")
            smtp.quit()
            consultardatostrabajadores()
    elif opciontrabajador == 8:
        print("{------Reiniciar Salario de trabajadores------}")
        
    elif opciontrabajador == 9:
        print("Devolviendose: ")
        prmenust()
    else:
        print("Opcion Incorrecta\nIntente denuevo")
        opciontrabajador()
                
#-------------------Llamar Funcion Principal---------------#
prmenust()
