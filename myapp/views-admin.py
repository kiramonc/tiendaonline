# coding=utf-8
import os
import uuid
import shutil
from pyramid.response import Response
from pyramid.renderers import render
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.view import (view_config,forbidden_view_config)
from pyramid.security import (remember,forget,)
from datetime import datetime
from .models import ( # el nombre de la clase en modelo
    DBSession, Producto, Usuario, Pedido, Prod_Pedido)


@view_config(route_name='add', renderer='templates/admin/add.pt', permission='edit')
def add_product(request):
    if 'form.submitted' in request.params:
        nombre = request.params['nombre']
        descripcion = request.params['descripcion']
        inventario = request.params['inventario']
        precio = request.params['precio']
        input_file = request.POST['file'].file
        extension = os.path.splitext(request.POST['file'].filename)[1]
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
    return dict(producto=producto, save_form=request.route_url('add'),
                logged_in=request.authenticated_userid)


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

        if request.POST['file'] != "":
            input_file = request.POST['file'].file
            extension = os.path.splitext(request.POST['file'].filename)[1]
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

    return dict(save_form=request.route_url('edit', uid=uid),
                logged_in=request.authenticated_userid, uid=uid)


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
    return dict(user=user, save_form=request.route_url('add_user'), logged_in=request.authenticated_userid)


@view_config(route_name='list_user', renderer='templates/admin/list_user.pt', permission='edit')
def list_user(request):
    return {"logged_in": request.authenticated_userid}


@view_config(route_name='edit_user', renderer='templates/admin/edit_user.pt', permission='edit')
def edit_user(request):
    uid = request.matchdict['uid']
    user = DBSession.query(Usuario).filter_by(id=uid).one()
    if user is not None:
        if 'form.submitted' in request.params:
            user.nombre = request.params['nombre']
            user.apellido = request.params['apellido']
            user.username = request.params['username']
            if request.params['cambio']=="t":
                user.password = request.params['password']
            user.rol = request.params['rol']
            DBSession.add(user)
            return HTTPFound(request.route_url('list_user'))
        elif 'form.delete' in request.params:
            return HTTPFound(request.route_url('delete_user', uid=uid))
        save_form = request.route_url('edit_user', uid=uid)
        return dict(save_form=save_form, logged_in=request.authenticated_userid, uid=uid)
    else:
        return HTTPFound(request.route_url('list_user'))


@view_config(route_name='delete_user', renderer='templates/admin/delete_user.pt', permission='edit')
def delete_user(request):
    uid = request.matchdict['uid']
    user = DBSession.query(Usuario).filter_by(id=uid).one()
    if user is None:
        return HTTPFound(request.route_url('list_user'))
    elif user.username == request.authenticated_userid:
        return HTTPFound(request.route_url('list_user'))
    if 'form.confirmDelete' in request.params:
        DBSession.delete(user)
        return HTTPFound(request.route_url('list_user'))
    elif 'form.cancelar' in request.params:
        return HTTPFound(request.route_url('list_user'))

    return dict(user=user, delete_form=request.route_url('delete_user', uid=uid),
                logged_in=request.authenticated_userid)


@view_config(route_name='detalle_pedido_admin', renderer='templates/admin/detalle_pedido.pt', permission='edit')
def detalle_pedido_admin(request):
    uid = request.matchdict['uid']
    pedido = DBSession.query(Pedido).filter_by(id=uid).one()
    data = DBSession.query(Prod_Pedido).filter_by(pedido_id=pedido.id).all()
    if 'form.response' in request.params:
        for prod in data:
            p = DBSession.query(Producto).filter_by(id=prod.producto.id).one()
            p.inventario = p.inventario - prod.unidades
            DBSession.add(p)
        pedido.estado = "Atendido"
        DBSession.add(pedido)
        return HTTPFound(request.route_url('admin_pedidos'))
    return dict(response_pedido=request.route_url('detalle_pedido_admin', uid=uid),
        formData=data, pedido=pedido, logged_in=request.authenticated_userid, uid=uid)


@view_config(route_name='admin_pedidos', renderer='templates/admin/pedidos.pt', permission='edit')
def admin_pedidos(request):
    data = DBSession.query(Pedido).all()
    return dict(formData=data, logged_in=request.authenticated_userid)


@view_config(route_name='data_products', renderer="json")
def data_products(request):
    data = DBSession.query(Producto).all()
    productos = []
    for prod in data:
        productos.append({"nombre": prod.nombre, "descripcion": prod.descripcion,
        "inventario": prod.inventario, "precio": prod.precio, "img": prod.img})
    return {"productos": productos}


@view_config(route_name='data_product', renderer="json")
def data_product(request):
    uid = request.matchdict['uid']
    prod = DBSession.query(Producto).filter_by(nombre=uid).one()
    producto = {"id":prod.id, "nombre": prod.nombre, "descripcion": prod.descripcion,
        "inventario": prod.inventario, "precio": prod.precio, "img": prod.img}
    return {"producto": producto}


@view_config(route_name='data_users', renderer="json")
def data_users(request):
    data = DBSession.query(Usuario).all()
    usuarios = []
    for user in data:
        usuarios.append({"id":user.id, "nombre":user.nombre, "apellido":user.apellido, "username":user.username,
            "password":user.password, "rol": user.rol})
    return {"usuarios": usuarios}


@view_config(route_name='data_user', renderer="json")
def data_user(request):
    uid = request.matchdict['uid']
    user = DBSession.query(Usuario).filter_by(id=uid).one()
    usuario = {"id":user.id, "nombre":user.nombre, "apellido":user.apellido, "username":user.username,
            "password":user.password, "rol": user.rol}
    return {"usuario": usuario}