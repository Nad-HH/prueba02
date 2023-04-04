from flask import Flask, render_template,request,redirect, url_for,flash,session 
from datetime import datetime 
from flask import send_from_directory
import os  
import database as db

# con esto accedemos a la carpeta "proyecto_gestion"
template_dir= os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
# unimos las carpetas src y templates a la carpeta del proyecto
template_dir=os.path.join(template_dir,'src','templates')

#inicializamos flask 
app = Flask(__name__,template_folder=template_dir)

#sesiones
app.secret_key="develoteca"

# ======rutas de la aplicacion===== 
# === Pagina de Inicio ===
@app.route('/')
def home():
    cursor=db.database.cursor()
    cursor.execute("SELECT * FROM informacionweb")
    myresult = cursor.fetchall()
    # convertimos los datos a diccionario
    insertObject=[]
    columNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columNames, record)))
    cursor.close()
    print(insertObject)
    return render_template('index.html', data=insertObject)

@app.route('/')
def home_base():
    cursor=db.database.cursor()
    cursor.execute("SELECT * FROM informacionweb")
    myresult = cursor.fetchall()
    # convertimos los datos a diccionario
    insertObject=[]
    columNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columNames, record)))
    cursor.close()
    print(insertObject)
    return render_template('base.html', data=insertObject)

# === IMAGENES ===
@app.route('/img/<imagen>')
def imagenes(imagen):
    print(imagen)
    return send_from_directory(os.path.join('templates/img'),imagen) 






@app.route('/evento.html')
def evento():
    cursor=db.database.cursor()
    cursor.execute("SELECT * FROM evento_academico")
    eventos = cursor.fetchall()
    db.database.commit()
    return render_template('evento.html',eventos_acad=eventos)


@app.route('/programa_general.html')
def programa_general():

    return render_template('programa_general.html')

# =================== ADMINISTRADOR ===================

@app.route('/admin/')
def administrador():
    if not 'login' in session:
        return redirect("/admin/login")
    return render_template('admin/index.html')

@app.route('/admin/login')
def login_admin():

    return render_template('admin/login.html')

@app.route('/admin/login', methods=['POST'])
def login_admin_post():
    _usuario=request.form['txtusuarioAdmin']
    _password=request.form['txtpasswordAdmin']
    print(_usuario)
    print(_password)
    #aumentar para la base de datos 2:43:01
    if _usuario=="admin" and _password=="123":
        session["login"]=True
        session["usuario"]="Administrador" 
        return redirect('/admin')   
    return render_template('/admin/login.html',mensaje="Acceso denegado")

# ________ configuracion  de informacion web __________

@app.route('/admin/informacion_web')
def login_admin_inf_web():
    if not 'login' in session:
        return redirect("/admin/login")
    
    cursor=db.database.cursor()
    cursor.execute("SELECT * FROM informacionweb")
    informacion_web = cursor.fetchall()
    db.database.commit()
    #print(informacion_web)
    
    return render_template('admin/informacion_web.html',infor_web=informacion_web)

# editar imagen e informacion web:

@app.route('/admin/informacion_web/editar_img/<string:id>',methods=['POST'])
def informacion_web_editar_imagen(id):
    tiempo=datetime.now()
    horaActual=tiempo.strftime('%Y%H%M%S')
    _imagenx = request.files['img_logo']
    _imagen_portadax = request.files['img_portada1']
    _imagen_portada2x = request.files['img_portada2']
    _imagen_portada3x = request.files['img_portada3']
    if _imagenx.filename!="":
        _imagen = request.files['img_logo']
        # Resto del código para procesar la imagen
        if _imagen.filename!="":
            nuevoNombre=horaActual+" "+_imagen.filename
            _imagen.save("templates/img/"+nuevoNombre)
        else:
            nuevoNombre=None
        
        cursor=db.database.cursor()
        cursor.execute("SELECT logotipo, portada1,portada2,portada3 FROM informacionweb WHERE id_info=%s",(id,))
        evento = cursor.fetchone()
        db.database.commit()
        
        if nuevoNombre is not None and os.path.exists("templates/img/"+str(evento[0])):
            os.unlink("templates/img/"+str(evento[0]))
            
        
    else:
        cursor=db.database.cursor()
        cursor.execute("SELECT logotipo, portada1,portada2,portada3 FROM informacionweb WHERE id_info=%s",(id,))
        evento = cursor.fetchone()
        db.database.commit()
        
        nuevoNombre=str(evento[0])
        
    if _imagen_portadax.filename!="":
        _imagen_portada = request.files['img_portada1']
        
        # Resto del código para procesar la imagen
        if _imagen_portada.filename!="":
            nuevoNombre_portada=horaActual+" "+_imagen_portada.filename
            _imagen_portada.save("templates/img/"+nuevoNombre_portada)
        else:
            nuevoNombre_portada=None
        cursor=db.database.cursor()
        cursor.execute("SELECT logotipo, portada1,portada2,portada3 FROM informacionweb WHERE id_info=%s",(id,))
        evento = cursor.fetchone()
        db.database.commit()
        if nuevoNombre_portada is not None and os.path.exists("templates/img/"+str(evento[1])):
            os.unlink("templates/img/"+str(evento[1]))
        
        
    else:
        cursor=db.database.cursor()
        cursor.execute("SELECT logotipo, portada1,portada2,portada3 FROM informacionweb WHERE id_info=%s",(id,))
        evento = cursor.fetchone()
        db.database.commit()
        nuevoNombre_portada=str(evento[1])
    
    #portada 2:
    
    if _imagen_portada2x.filename!="":
        _imagen_portada2 = request.files['img_portada2']
        
        # Resto del código para procesar la imagen
        if _imagen_portada2.filename!="":
            nuevoNombre_portada2=horaActual+" "+_imagen_portada2.filename
            _imagen_portada2.save("templates/img/"+nuevoNombre_portada2)
        else:
            nuevoNombre_portada2=None
        cursor=db.database.cursor()
        cursor.execute("SELECT logotipo, portada1,portada2,portada3 FROM informacionweb WHERE id_info=%s",(id,))
        evento = cursor.fetchone()
        db.database.commit()
        if nuevoNombre_portada2 is not None and os.path.exists("templates/img/"+str(evento[2])):
            os.unlink("templates/img/"+str(evento[2]))

    else:
        cursor=db.database.cursor()
        cursor.execute("SELECT logotipo, portada1,portada2,portada3 FROM informacionweb WHERE id_info=%s",(id,))
        evento = cursor.fetchone()
        db.database.commit()
        nuevoNombre_portada2=str(evento[2])
    
     #portada 3:
    
    if _imagen_portada3x.filename!="":
        _imagen_portada3 = request.files['img_portada3']
        
        # Resto del código para procesar la imagen
        if _imagen_portada3.filename!="":
            nuevoNombre_portada3=horaActual+" "+_imagen_portada3.filename
            _imagen_portada3.save("templates/img/"+nuevoNombre_portada3)
        else:
            nuevoNombre_portada3=None
        cursor=db.database.cursor()
        cursor.execute("SELECT logotipo, portada1,portada2,portada3 FROM informacionweb WHERE id_info=%s",(id,))
        evento = cursor.fetchone()
        db.database.commit()
        if nuevoNombre_portada3 is not None and os.path.exists("templates/img/"+str(evento[3])):
            os.unlink("templates/img/"+str(evento[3]))

    else:
        cursor=db.database.cursor()
        cursor.execute("SELECT logotipo, portada1,portada2,portada3 FROM informacionweb WHERE id_info=%s",(id,))
        evento = cursor.fetchone()
        db.database.commit()
        nuevoNombre_portada3=str(evento[3])
      
    
    cursor2 = db.database.cursor()
    sql="UPDATE `informacionweb` SET logotipo=%s, portada1=%s,portada2=%s,portada3=%s WHERE id_info=%s"
    datos=(nuevoNombre,nuevoNombre_portada,nuevoNombre_portada2,nuevoNombre_portada3, id)
    cursor2.execute(sql,datos)
    db.database.commit()
  
    return redirect("/admin/informacion_web")

# editar texto:
    
@app.route('/admin/informacion_web/editar/<string:id>',methods=['POST'])
def informacion_web_editar(id):
    _nom=request.form['txtnombre']
    _desc=request.form['txtdesc']
    _mision=request.form['txtmision']
    _vision=request.form['txtvision']
    _obj=request.form['txtobj']
    _direc=request.form['txtdirec']
    _contacto=request.form['txtcontacto']
    _correo=request.form['txtcorreo']
    
    
    if _nom and _desc and _mision and _vision and _obj and _direc and _contacto and _correo :
        cursor = db.database.cursor()
        sql="UPDATE `informacionweb` SET`direccion`=%s,`descripcion`=%s,`mision`=%s,`vision`=%s,`objetivo`=%s,`nombre`=%s,`celular`=%s,`correo_el`=%s WHERE id_info=%s"
        datos=( _direc ,_desc, _mision , _vision , _obj , _nom,_contacto , _correo,id)
        cursor.execute(sql,datos)
        db.database.commit()
    
    return redirect("/admin/informacion_web")
    
# ________ configuracion  de eventos __________

@app.route('/admin/gestion_eventos')
def login_admin_eventos():
    if not 'login' in session:
        return redirect("/admin/login")
    cursor=db.database.cursor()
    cursor.execute("SELECT * FROM evento_academico")
    evento_acad = cursor.fetchall()
    db.database.commit()
    return render_template('admin/gestion_eventos.html',eventos=evento_acad)


@app.route('/admin/gestion_eventos/guardar',methods=['POST'])
def login_admin_evento_guardar():
    _titulo=request.form['txttituloevento']
    _tipo=request.form['txttipoevento']
    _capmax=request.form['txtcapmaxevento']
    _precio=request.form['txtprecioevento']
    _descripcion=request.form['txtdescevento']
    _area=request.form['txtareaevento']
    _fecha=request.form['txtfechaevento']
    _imagen=request.files['txtimagenevento']
    
    tiempo=datetime.now()
    horaActual=tiempo.strftime('%Y%H%M%S')
    
    if _imagen.filename!="":
        nuevoNombre=horaActual+" "+_imagen.filename
        _imagen.save("templates/img/"+nuevoNombre)
        
    sql="INSERT INTO `evento_academico`(`id_evento`, `tipo`, `portada_even`, `capacidadmax`, `precio`, `titulo`, `descripcion`, `area`, `fecha`, `id_control`, `id_administrador`) VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s,NULL,NULL);"
    datos=(_tipo,nuevoNombre,_capmax,_precio,_titulo,_descripcion,_area,_fecha)
    
    cursor=db.database.cursor()
    cursor.execute(sql,datos)
    db.database.commit()
    
    return redirect('/admin/gestion_eventos')

@app.route('/admin/gestion_eventos/borrar',methods=['POST'])
def login_admin_evento_borrar():
    _id=request.form['txtID']
    
    cursor=db.database.cursor()
    cursor.execute("SELECT portada_even FROM evento_academico WHERE id_evento=%s",(_id,))
    evento = cursor.fetchall()
    db.database.commit()
   #print(evento)
    if os.path.exists("templates/img/"+str(evento[0][0])):
       os.unlink("templates/img/"+str(evento[0][0]))
    
    cursor=db.database.cursor()
    #cursor.execute("DELETE FROM `evento_academico` WHERE id_evento=%s",(_id,))
    cursor.execute("INSERT INTO evento_eliminado ( id_evento,tipo,portada_even,capacidadmax,precio,titulo,descripcion,area,fecha,id_control,id_administrador) SELECT id_evento,tipo,portada_even,capacidadmax,precio,titulo,descripcion,area,fecha,id_control,id_administrador FROM evento_academico WHERE id_evento = %s", (_id,))
    cursor.execute("DELETE FROM `evento_academico` WHERE id_evento=%s",(_id,))
    db.database.commit() 
    
    return redirect('/admin/gestion_eventos')

# editar imagen 

@app.route('/admin/gestion_eventos/editar_imagen/<string:id>',methods=['POST'])
def login_admin_evento_editar_imagen(id):
    
       
    _imagen=request.files['img_evento']
    tiempo=datetime.now()
    horaActual=tiempo.strftime('%Y%H%M%S')
    
    if _imagen.filename!="":
        nuevoNombre=horaActual+" "+_imagen.filename
        _imagen.save("templates/img/"+nuevoNombre)
    else:
        return redirect('/admin/gestion_eventos')
    
    cursor=db.database.cursor()
    cursor.execute("SELECT portada_even FROM evento_academico WHERE id_evento=%s",(id,))
    evento = cursor.fetchall()
    db.database.commit()
    
    if os.path.exists("templates/img/"+str(evento[0][0])):
       os.unlink("templates/img/"+str(evento[0][0]))
       
    cursor = db.database.cursor()
    sql="UPDATE `evento_academico` SET portada_even=%s WHERE id_evento=%s"
    datos=(nuevoNombre,id)
    cursor.execute(sql,datos)
    db.database.commit()
    return redirect('/admin/gestion_eventos')
    
@app.route('/admin/gestion_eventos/editar/<string:id>',methods=['POST'])
def login_admin_evento_editar(id):
    _titulo=request.form['txttituloevento']
    _tipo=request.form['txttipoevento']
    _capmax=request.form['txtcapmaxevento']
    _precio=request.form['txtprecioevento']
    _descripcion=request.form['txtdescevento']
    _area=request.form['txtareaevento']
    _fecha=request.form['txtfechaevento']
    
    
    if _titulo and _tipo and _capmax and _precio and _descripcion and _area and _fecha :
        cursor = db.database.cursor()
        sql="UPDATE `evento_academico` SET tipo=%s, capacidadmax=%s, precio=%s, titulo=%s, descripcion=%s, area=%s, fecha=%s WHERE id_evento=%s"
        datos=(_tipo, _capmax,_precio,_titulo,_descripcion,_area,_fecha,id)
        cursor.execute(sql,datos)
        db.database.commit()
        
    return redirect('/admin/gestion_eventos')




# ________ configuracion  de participantes __________

@app.route('/admin/gestion_participantes')
def login_admin_participantes():
    if not 'login' in session:
        return redirect("/admin/login")
    
    cursor=db.database.cursor()
    cursor.execute("SELECT * FROM usuario")
    myresult = cursor.fetchall()
    # convertimos los datos a diccionario
    insertObject=[]
    columNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columNames, record)))
    cursor.close()
    
    return render_template('admin/gestion_participantes.html',data=insertObject)


# ________ configuracion  de control __________

@app.route('/admin/gestion_control')
def login_admin_control():
    if not 'login' in session:
        return redirect("/admin/login")
    return render_template('admin/gestion_control.html')


# ________ configuracion  de expositor __________

@app.route('/admin/gestion_expositor')
def login_admin_expositor():
    if not 'login' in session:
        return redirect("/admin/login")
    return render_template('admin/gestion_expositor.html')


# cerramos administrador: 

@app.route('/admin/cerrar')
def admin_login_cerrar():
    session.clear()
    return redirect('/admin/login')

if __name__ == '__main__':
    app.run(debug=True,port=4000)
