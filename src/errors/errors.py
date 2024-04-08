class ApiError(Exception):
    code = 422
    description = "Default message"


class EmailBadRequestError(ApiError):
    code = 400
    description = "Los campos email o app_uuid no están presentes en la solicitud o email tiene un mal formato"


class EmailAlreadyExistsError(ApiError):
    code = 412
    description = "El email ya está registrado"


class EmailNotFoundError(ApiError):
    code = 404
    # Usuario no encontrado
    description = "Email no encontrado"

class ResetBlackListDBError(ApiError):
    code = 500
    #'Error al eliminar registros de blacklist.
    description = "Error al eliminar registros de blacklist"


    