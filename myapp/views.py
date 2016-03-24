# coding=utf-8
import os
import uuid
import shutil
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from sqlalchemy.exc import DBAPIError

from pyramid.view import (
    view_config,
    forbidden_view_config,
    )
from pyramid.security import (
    remember,
    forget,
    )
from datetime import datetime
from .models import (
    DBSession,
    Producto,  # el nombre de la clase en modelo
    Usuario,
    Pedido,
    Prod_Pedido
    )


@view_config(route_name='home', renderer='templates/home.pt', permission='show')
@view_config(route_name='home-client', renderer='templates/client/home.pt', permission='show')
@view_config(route_name='home-admin', renderer='templates/admin/home.pt', permission='edit')
def home(request):
    username = request.authenticated_userid
    if username is None:
        inicio = request.route_url('home')
        print "No logueado"
        return dict(inicio=inicio, logged_in=request.authenticated_userid)
    else:
        user = DBSession.query(Usuario).filter_by(username=username).one()
        if user.rol == 'admins':
            inicio = request.route_url('home-admin')
            print "Admin logueado"
            return dict(inicio=inicio, logged_in=request.authenticated_userid)
        else:
            inicio = request.route_url('home-client')
            print "CLiente logueado"
            return dict(inicio=inicio, logged_in=request.authenticated_userid)


@view_config(route_name='pag-error', renderer='templates/error.pt', permission='show')
@view_config(route_name='error-client', renderer='templates/client/error.pt', permission='show')
@view_config(route_name='error-admin', renderer='templates/admin/error.pt', permission='edit')
def error(request):
    username = request.authenticated_userid
    if username is None:
        inicio = request.route_url('pag-error')
        return dict(inicio=inicio, logged_in=request.authenticated_userid)
    else:
        user = DBSession.query(Usuario).filter_by(username=username).one()
        if user.rol == 'admins':
            inicio = request.route_url('error-admin')
            return dict(inicio=inicio, logged_in=request.authenticated_userid)
        else:
            inicio = request.route_url('error-client')
            return dict(inicio=inicio, logged_in=request.authenticated_userid)


@view_config(route_name='add', renderer='templates/admin/add.pt', permission='edit')
def add_product(request):
    if 'form.submitted' in request.params:
        nombre = request.params['nombre']
        descripcion = request.params['descripcion']
        inventario = request.params['inventario']
        precio = request.params['precio']


        filename = request.POST['file'].filename
        print "Imagen: "+ filename
        input_file = request.POST['file'].file
        extension = os.path.splitext(filename)[1]
        file_path = os.path.join('myapp/static/img/productos/', '%s' % uuid.uuid4()+extension)
        temp_file_path = file_path + '~'
        input_file.seek(0)
        with open(temp_file_path, 'wb') as output_file:
            shutil.copyfileobj(input_file, output_file)
        os.rename(temp_file_path, file_path)

        img = os.path.basename(file_path)
        producto = Producto(nombre, descripcion, inventario, precio, img)
        DBSession.add(producto)
        return HTTPFound(request.route_url('list'))

    producto = Producto(nombre="", descripcion="", inventario=0, precio=0.0, img="")
    save_form = request.route_url('add')
    return dict(producto=producto, save_form=save_form,
                logged_in=request.authenticated_userid)


@view_config(route_name='productos', renderer='templates/client/productos.pt', permission='show')
@view_config(route_name='list_prod', renderer='templates/productos.pt', permission='show')
@view_config(route_name='list', renderer='templates/admin/list.pt', permission='edit')
def list_product(request):
    data = DBSession.query(Producto).all()
    return dict(formData=data, logged_in=request.authenticated_userid)


@view_config(route_name='ver', renderer='templates/client/show.pt', permission='show')
@view_config(route_name='ver_prod', renderer='templates/show.pt', permission='show')
@view_config(route_name='show', renderer='templates/admin/show.pt', permission='edit')
def show_product(request):
    uid = request.matchdict['uid']
    producto = DBSession.query(Producto).filter_by(nombre=uid).one()
    if producto is None:
        return HTTPFound(request.route_url('list'))
    return dict(producto=producto, logged_in=request.authenticated_userid)


@view_config(route_name='edit', renderer='templates/admin/edit.pt', permission='edit')
def edit_product(request):
    uid = request.matchdict['uid']
    producto = DBSession.query(Producto).filter_by(nombre=uid).one()
    if producto is None:
        return HTTPFound(request.route_url('list'))
    if 'form.submitted' in request.params:
        producto.nombre = request.params['nombre']
        producto.descripcion = request.params['descripcion']
        producto.inventario = request.params['inventario']
        producto.precio = request.params['precio']


        filename = request.POST['file'].filename
        print request.POST['file']
        print filename

        input_file = request.POST['file'].file
        extension = os.path.splitext(filename)[1]
        file_path = os.path.join('myapp/static/img/productos/', '%s' % uuid.uuid4()+extension)
        temp_file_path = file_path + '~'
        input_file.seek(0)
        with open(temp_file_path, 'wb') as output_file:
            shutil.copyfileobj(input_file, output_file)
        os.rename(temp_file_path, file_path)

        producto.img = os.path.basename(file_path)



        DBSession.add(producto)
        return HTTPFound(request.route_url('list'))
    elif 'form.delete' in request.params:
        return HTTPFound(request.route_url('delete', uid=uid))

    return dict(producto=producto, save_form=request.route_url('edit', uid=uid),
                logged_in=request.authenticated_userid)


@view_config(route_name='delete', renderer='templates/admin/delete.pt', permission='edit')
def delete_product(request):
    uid = request.matchdict['uid']
    producto = DBSession.query(Producto).filter_by(nombre=uid).one()
    if producto is None:
        return HTTPFound(request.route_url('list'))
    if 'form.confirmDelete' in request.params:
        DBSession.delete(producto)
        return HTTPFound(request.route_url('list'))
    elif 'form.cancelar' in request.params:
        return HTTPFound(request.route_url('list'))

    return dict(producto=producto, delete_form=request.route_url('delete', uid=uid),
                logged_in=request.authenticated_userid)


@view_config(route_name='register', renderer='templates/register.pt', permission='show')
def register(request):
    if 'form.submitted' in request.params:
        nombre = request.params['nombre']
        apellido = request.params['apellido']
        username = request.params['username']
        password = request.params['password']
        user = Usuario(nombre, apellido, username, password,'clients')
        DBSession.add(user)
        return HTTPFound(request.route_url('login'))

    user = Usuario(nombre="", apellido="", username="", password="", rol='invitado')
    save_form = request.route_url('register')
    return dict(user=user, save_form=save_form,
                logged_in=request.authenticated_userid)


@view_config(route_name='add_user', renderer='templates/admin/add_user.pt', permission='edit')
def add_user(request):
    if 'form.submitted' in request.params:
        nombre = request.params['nombre']
        apellido = request.params['apellido']
        username = request.params['username']
        password = request.params['password']
        user = Usuario(nombre, apellido, username, password,'admins')
        DBSession.add(user)
        return HTTPFound(request.route_url('list_user'))

    user = Usuario(nombre="", apellido="", username="", password="", rol='invitado')
    save_form = request.route_url('add_user')
    return dict(user=user, save_form=save_form,
                logged_in=request.authenticated_userid)


@view_config(route_name='list_user', renderer='templates/admin/list_user.pt', permission='edit')
def list_user(request):
    data = DBSession.query(Usuario).all()
    return dict(formData=data, logged_in=request.authenticated_userid)


@view_config(route_name='edit_user', renderer='templates/admin/edit_user.pt', permission='edit')
def edit_user(request):
    uid = request.matchdict['uid']
    user = DBSession.query(Usuario).filter_by(id=uid).one()
    if user is None:
        return HTTPFound(request.route_url('list_user'))
    if 'form.submitted' in request.params:
        user.nombre = request.params['nombre']
        user.apellido = request.params['apellido']
        user.username = request.params['username']
        user.password = request.params['password']
        user.rol = request.params['rol']
        DBSession.add(user)
        return HTTPFound(request.route_url('list_user'))
    elif 'form.delete' in request.params:
        return HTTPFound(request.route_url('delete_user', uid=uid))

    return dict(user=user, save_form=request.route_url('edit_user', uid=uid),
                logged_in=request.authenticated_userid)


@view_config(route_name='delete_user', renderer='templates/admin/delete_user.pt', permission='edit')
def delete_user(request):
    uid = request.matchdict['uid']
    user = DBSession.query(Usuario).filter_by(id=uid).one()
    if user is None:
        return HTTPFound(request.route_url('list_user'))
    if 'form.confirmDelete' in request.params:
        DBSession.delete(user)
        return HTTPFound(request.route_url('list_user'))
    elif 'form.cancelar' in request.params:
        return HTTPFound(request.route_url('list_user'))

    return dict(user=user, delete_form=request.route_url('delete_user', uid=uid),
                logged_in=request.authenticated_userid)


@view_config(route_name='cuenta', renderer='templates/client/cuenta.pt', permission='show')
def cuenta(request):
    username = request.authenticated_userid
    user = DBSession.query(Usuario).filter_by(username=username).one()
    if user is None:
        return HTTPFound(request.route_url('list_user'))
    if 'form.submitted' in request.params:
        user.nombre = request.params['nombre']
        user.apellido = request.params['apellido']
        user.username = request.params['username']
        user.password = request.params['password']
        user.rol = request.params['rol']
        DBSession.add(user)
        return HTTPFound(request.route_url('cuenta'))
    elif 'form.delete' in request.params:
        return HTTPFound(request.route_url('desactivar'))

    return dict(user=user, save_form=request.route_url('cuenta'),
                logged_in=request.authenticated_userid)


@view_config(route_name='desactivar', renderer='templates/client/desc_cuenta.pt', permission='show')
def desactivar(request):
    username = request.authenticated_userid
    user = DBSession.query(Usuario).filter_by(username=username).one()
    if user is None:
        return HTTPFound(request.route_url('home-client'))
    if 'form.confirmDelete' in request.params:
        headers = forget(request)
        DBSession.delete(user)
        return HTTPFound(location=request.route_url('home'), headers=headers)
    elif 'form.cancelar' in request.params:
        return HTTPFound(request.route_url('cuenta'))

    return dict(user=user, delete_form=request.route_url('desactivar'),
                logged_in=request.authenticated_userid)


@view_config(route_name='pedidos', renderer='templates/client/pedidos.pt', permission='show')
def pedidos(request):
    username = request.authenticated_userid
    user = DBSession.query(Usuario).filter_by(username=username).one()
    data = DBSession.query(Pedido).filter_by(cliente_id=user.id).all()
    return dict(formData=data, logged_in=request.authenticated_userid)


@view_config(route_name='detalle_pedido', renderer='templates/client/detalle_pedido.pt', permission='show')
def detalle_pedido(request):
    username = request.authenticated_userid
    if username is not None:
        user = DBSession.query(Usuario).filter_by(username=request.authenticated_userid).one()
        uid = request.matchdict['uid']
        pedido = DBSession.query(Pedido).filter_by(id=uid).one()
        if pedido.cliente_id == user.id:
            data = DBSession.query(Prod_Pedido).filter_by(pedido_id=pedido.id).all()
            return dict(formData=data, pedido=pedido, logged_in=request.authenticated_userid, uid=uid)
        else:
            return HTTPFound(request.route_url('error-client'))
    else:
        return HTTPFound(request.route_url('pag-error'))


@view_config(route_name='detalle_pedido_admin', renderer='templates/admin/detalle_pedido.pt', permission='edit')
def detalle_pedido_admin(request):
    uid = request.matchdict['uid']
    pedido = DBSession.query(Pedido).filter_by(id=uid).one()
    data = DBSession.query(Prod_Pedido).filter_by(pedido_id=pedido.id).all()
    return dict(formData=data, pedido=pedido, logged_in=request.authenticated_userid, uid=uid)


@view_config(route_name='carrito', renderer='templates/client/chart.pt', permission='show')
def carrito(request):
    inicio = request.route_url('carrito')
    return dict(inicio=inicio, logged_in=request.authenticated_userid)


@view_config(route_name='get_data', renderer="json")
def get_data(request):
    uid = request.matchdict['uid']
    pedido = DBSession.query(Pedido).filter_by(id=uid).one()
    cliente = {"nombre":pedido.cliente.nombre, "apellido":pedido.cliente.apellido, "username":pedido.cliente.username}
    print "CLIENTE"
    print cliente
    data = DBSession.query(Prod_Pedido).filter_by(pedido_id=pedido.id).all()
    productos = []
    fecha = pedido.fecha.strftime("%d-%m-%Y %H:%M")
    for prod in data:
        productos.append({"nombre":prod.producto.nombre, "unidades":prod.unidades, "precio":prod.producto.precio})
    return {"productos": productos, "fecha": fecha, "uid": uid, "cliente": cliente}


@view_config(route_name='generate_ajax_data', renderer="json")
def my_ajax_view(request):
    print "Hello response"
    nombres= request.POST['nombres'].split(",")
    unidades= request.POST['unidades'].split(",")
    # print nombres[0] + ": " + unidades[0]
    client = DBSession.query(Usuario).filter_by(username=request.authenticated_userid).one()
    print "Usuario: " + client.username

    dt = datetime.now()
    pedido = Pedido(client.id, dt, "En espera")
    print "Fecha y hora: " + pedido.fecha.strftime("%d-%m-%Y %H:%M")
    DBSession.add(pedido)
    pedido = DBSession.query(Pedido).filter_by(cliente_id=client.id, fecha=dt).one()
    cont=0
    for nombre in nombres:
        producto = DBSession.query(Producto).filter_by(nombre=nombre).one()
        prod_pedido = Prod_Pedido(pedido.id, producto.id, unidades[cont])
        DBSession.add(prod_pedido)
        cont=cont+1
    return dict(message="Pedido realizado con éxito", logged_in=request.authenticated_userid)


@view_config(route_name='admin_pedidos', renderer='templates/admin/pedidos.pt', permission='edit')
def admin_pedidos(request):
    data = DBSession.query(Pedido).all()
    return dict(formData=data, logged_in=request.authenticated_userid)


@view_config(route_name='login', renderer='templates/login.pt')
@forbidden_view_config(renderer='templates/login.pt')
def login(request):
    login_url = request.route_url('login')
    referrer = request.url

    came_from = request.params.get('came_from', referrer)
    message = ''
    login = ''
    password = ''
    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        usuario= DBSession.query(Usuario).filter_by(username=login).one()
        if usuario is not None:
            if usuario.password == password:
                headers = remember(request, login)
                if referrer == login_url:
                    user = DBSession.query(Usuario).filter_by(username=login).one()
                    if user.rol == 'admins':
                        return HTTPFound(request.route_url('home-admin'), headers=headers)
                    else:
                        return HTTPFound(request.route_url('home-client'), headers=headers)

                return HTTPFound(location=came_from, headers=headers)
        message = 'Failed login'
    return dict(message=message, url=request.route_url('login'), came_from=came_from,
        login = login, password = password)


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location=request.route_url('home'), headers=headers)

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_MyApp_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
