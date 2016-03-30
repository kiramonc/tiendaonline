from .models import (
    DBSession,
    Usuario
    )


def groupfinder(userid, request):
    usuario = DBSession.query(Usuario).filter_by(username=userid).one()
    if usuario is None:
        grupo = {'invitado': ['invitado']}
        return grupo.get('invitado', [])
    grupo = {usuario.username: [usuario.rol]}
    return grupo.get(userid, [])