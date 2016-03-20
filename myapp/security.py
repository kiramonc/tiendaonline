from .models import (
    DBSession,
    Usuario
    )


def groupfinder(userid, request):
    usuario = DBSession.query(Usuario).filter_by(username=userid).one()
    if usuario is None:
        return None
    grupo = {usuario.username: [usuario.rol]}
    return grupo.get(userid, [])