from nlp.domain.errors import HandlingError


class ApplicationError(HandlingError):
    pass


class InvalidPasswordError(ApplicationError):
    pass


class UndefinedUserError(ApplicationError):
    pass


class AuthError(ApplicationError):
    pass


class UndefinedTaskError(ApplicationError):
    pass


class UserAlreadyExists(ApplicationError):
    pass


class UndefinedProjectError(ApplicationError):
    pass


class UserDoesNotRelatedToProject(ApplicationError):
    pass
