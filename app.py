from flask import Flask, render_template, request, redirect ,url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'python_crud'

mysql = MySQL(app)


app.secret_key = 'mysecretkey'

@app.route('/')
def Mostrar_index():
    mostrar = mysql.connection.cursor()
    mostrar.execute('SELECT * FROM contactos')
    data = mostrar.fetchall()
    mysql.connection.commit()
    return render_template('index.html', contactos = data)

@app.route('/agregar_user', methods=['POST'])
def Agregar_Contacto():
    if request.method == 'POST':
        nombres = request.form['nombres']
        telefono = request.form['telefono']
        email = request.form['email']
        agree = mysql.connection.cursor()
        agree.execute('INSERT INTO contactos (nombres, telefono, email) VALUES (%s, %s, %s)',
        (nombres, telefono, email))
        mysql.connection.commit()
        flash('Contacto insertado correcctamente')
        return redirect(url_for('Mostrar_index'))


@app.route('/editar_user/<string:id>')
def Editar_user(id):
    edit = mysql.connection.cursor()
    edit.execute('SELECT * FROM contactos WHERE id = %s', (id))
    data = edit.fetchall()
    print(data)
    mysql.connection.commit()
    return render_template('edit.html', contacto = data[0])

@app.route('/update_user/<id>',  methods=['POST'])
def Update_User(id):
    if request.method == 'POST':
        nombres = request.form['nombres']
        telefono = request.form['telefono']
        email = request.form['email']
        update = mysql.connection.cursor()
        update.execute("""
            UPDATE contactos SET nombres = %s, telefono = %s, email = %s WHERE id = %s
        """, (nombres, telefono, email, id))
        mysql.connection.commit()
        flash('Usuario actualizado')
        return redirect(url_for('Mostrar_index'))



@app.route('/eliminar_user/<string:id>')
def Eliminar_User(id):
    delete = mysql.connection.cursor()
    delete.execute('DELETE FROM `contactos` WHERE `contactos`.`id` = {0}'.format(id))
    mysql.connection.commit()
    flash('Usuario elimando con exito')
    return redirect(url_for('Mostrar_index'))

if __name__ == '__main__':
    app.run(port = 3000, debug = True)
