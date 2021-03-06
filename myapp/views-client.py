# coding=utf-8
from pyramid.view import view_config
import json
from pyramid.httpexceptions import HTTPFound
from pyramid.view import (view_config,forbidden_view_config)
from pyramid.security import (remember,forget,)
from datetime import datetime
from .models import ( # el nombre de la clase en modelo
    DBSession, Producto, Usuario, Pedido, Prod_Pedido)


@view_config(route_name='carrito', renderer='templates/client/chart.pt', permission='shop')
def carrito(request):
    inicio = request.route_url('carrito')
    return dict(inicio=inicio, logged_in=request.authenticated_userid)


@view_config(route_name='generate_ajax_data', renderer="json")
def my_ajax_view(request):
    nombres= request.POST['nombres'].split(",")
    unidades= request.POST['unidades'].split(",")
    client = DBSession.query(Usuario).filter_by(username=request.authenticated_userid).one()

    dt = datetime.now()
    pedido = Pedido(client.id, dt, 0, None)
    DBSession.add(pedido)
    pedido = DBSession.query(Pedido).filter_by(cliente_id=client.id, fecha_pedido=dt).one()
    cont=0
    for nombre in nombres:
        producto = DBSession.query(Producto).filter_by(nombre=nombre).one()
        prod_pedido = Prod_Pedido(pedido.id, producto.id, unidades[cont])
        DBSession.add(prod_pedido)
        cont=cont+1
    return dict(message="Pedido realizado con éxito", logged_in=request.authenticated_userid)


@view_config(route_name='cuenta', renderer='templates/client/cuenta.pt', permission='shop')
def cuenta(request):
    message=''
    username = request.authenticated_userid
    user = DBSession.query(Usuario).filter_by(username=username).one()
    if 'form.submitted' in request.params:
        user.nombre = request.params['nombre']
        user.apellido = request.params['apellido']
        user.username = request.params['username']
        if request.params['cambio']=="t":
            user.password = request.params['password']

        user.rol = request.params['rol']
        DBSession.add(user)
        message='Datos actualizados'
    elif 'form.delete' in request.params:
        return HTTPFound(request.route_url('desactivar'))

    return dict(message=message, user=user, save_form=request.route_url('cuenta'),
                logged_in=request.authenticated_userid)


@view_config(route_name='desactivar', renderer='templates/client/desc_cuenta.pt', permission='shop')
def desactivar(request):
    username = request.authenticated_userid
    user = DBSession.query(Usuario).filter_by(username=username).one()
    if user is None:
        return HTTPFound(request.route_url('home-client'))
    if 'form.confirmDelete' in request.params:
        headers = forget(request)
        user.estado = False
        DBSession.add(user)
        return HTTPFound(location=request.route_url('login'), headers=headers)
    elif 'form.cancelar' in request.params:
        return HTTPFound(request.route_url('cuenta'))

    return dict(user=user, delete_form=request.route_url('desactivar'),
                logged_in=request.authenticated_userid)


@view_config(route_name='pedidos', renderer='templates/client/pedidos.pt', permission='shop')
def pedidos(request):
    username = request.authenticated_userid
    user = DBSession.query(Usuario).filter_by(username=username).one()
    data = DBSession.query(Pedido).filter_by(cliente_id=user.id).all()
    return dict(formData=data, logged_in=request.authenticated_userid)


@view_config(route_name='detalle_pedido', renderer='templates/client/detalle_pedido.pt', permission='shop')
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


@view_config(route_name='get_data', renderer="json")
def get_data(request):
    uid = request.matchdict['uid']
    p= DBSession.query(Pedido).filter_by(id=uid).one()
    f = p.fecha_atencion if (p.fecha_atencion is None) else p.fecha_atencion.isoformat()
    pedido = {"uid": uid, "fecha_pedido": p.fecha_pedido.isoformat(),
              "fecha_atencion":f, "estado": p.estado}
    cliente = {"nombre":p.cliente.nombre, "apellido":p.cliente.apellido, "username":p.cliente.username, "estado":p.cliente.estado}
    data = DBSession.query(Prod_Pedido).filter_by(pedido_id=p.id).all()
    productos = []
    for prod in data:
        productos.append({"nombre":prod.producto.nombre, "unidades":prod.unidades, "precio":prod.producto.precio})
    return {"productos": productos, "pedido": pedido, "cliente": cliente}


@view_config(route_name='get_pedidos', renderer="json")
def get_pedidos(request):
    client = DBSession.query(Usuario).filter_by(username=request.authenticated_userid).one()
    data = DBSession.query(Pedido).filter_by(cliente_id=client.id).all()
    pedidos = []
    for p in data:
        f = p.fecha_atencion if (p.fecha_atencion is None) else p.fecha_atencion.isoformat()
        pedidos.append({"id": p.id, "fecha_pedido": p.fecha_pedido.isoformat(),
                        "fecha_atencion":f,"estado": p.estado})
    return {"pedidos": pedidos}