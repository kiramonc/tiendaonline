# coding=utf-8
from sqlalchemy import (
    Column,
    Integer,
    Text,
    Sequence,
    String,
    Float,
    DateTime,
    ForeignKey,
    Boolean,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)
from zope.sqlalchemy import ZopeTransactionExtension
from pyramid.security import (
    Allow,
    Everyone,
    )
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Producto(Base):
    __tablename__ = 'producto'
    id = Column(Integer, Sequence('producto_seq'), primary_key=True)
    nombre = Column(String(255), unique=True)
    descripcion = Column(String(255))
    inventario = Column(Integer)
    precio = Column(Float)
    img = Column(String(255))
    estado = Column(Boolean)

    def __init__(self, nombre, descripcion, inventario, precio, img, estado):
        self.nombre = nombre
        self.descripcion = descripcion
        self.inventario = inventario
        self.precio = precio
        self.img = img
        self.estado = estado


class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, Sequence('usuario_seq'), primary_key=True)
    username = Column(String(255), unique=True)
    password = Column(String(255))
    nombre = Column(String(255))
    apellido = Column(String(255))
    rol = Column(String(255))
    pedidos = relationship("Pedido")
    estado = Column(Boolean)

    def __init__(self, nombre, apellido, username, password, rol, estado):
        self.username = username
        self.password = password
        self.nombre = nombre
        self.apellido = apellido
        self.rol = rol
        self.estado = estado


class Pedido(Base):
    __tablename__ = 'pedido'
    id = Column(Integer, Sequence('pedido_seq'), primary_key=True)
    cliente_id = Column(Integer, ForeignKey('usuario.id'))
    fecha_pedido = Column(DateTime)
    fecha_atencion = Column(DateTime)
    estado = Column(Integer)
    productos = relationship("Prod_Pedido")
    cliente = relationship("Usuario")

    def __init__(self, cliente_id, fecha_pedido, estado, fecha_atencion):
        self.cliente_id = cliente_id
        self.fecha_pedido = fecha_pedido
        self.estado = estado
        self.fecha_atencion = fecha_atencion


class Prod_Pedido(Base):
    __tablename__ = 'prod_pedido'
    pedido_id = Column(Integer, ForeignKey('pedido.id'), primary_key=True)
    prod_id = Column(Integer, ForeignKey('producto.id'), primary_key=True)
    unidades = Column(Integer)
    producto = relationship("Producto")

    def __init__(self, pedido_id, prod_id, unidades):
        self.pedido_id = pedido_id
        self.prod_id = prod_id
        self.unidades = unidades
# Index('my_index', Producto.nombre, unique=True, mysql_length=255)


class RootFactory(object):
    __acl__ = [ (Allow, Everyone, 'all'),
                (Allow, 'admins', 'edit'),
                (Allow, 'clients', 'shop'),
                (Allow, 'invitado', 'show')]

    def __init__(self, request):
        pass