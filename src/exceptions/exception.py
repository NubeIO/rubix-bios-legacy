class BadDataException(Exception):
    def __init__(self, *args):
        super(BadDataException, self).__init__(*args)


class UnauthorizedException(Exception):
    def __init__(self, *args):
        super(UnauthorizedException, self).__init__(*args)


class ForbiddenException(Exception):
    def __init__(self, *args):
        super(ForbiddenException, self).__init__(*args)


class NotFoundException(Exception):
    def __init__(self, *args):
        super(NotFoundException, self).__init__(*args)


class PreConditionException(Exception):
    def __init__(self, *args):
        super(PreConditionException, self).__init__(*args)


class InternalServerErrorException(Exception):
    def __init__(self, *args):
        super(InternalServerErrorException, self).__init__(*args)


class NotImplementedException(Exception):
    def __init__(self, *args):
        super(NotImplementedException, self).__init__(*args)


class GatewayTimeoutException(Exception):
    def __init__(self, *args):
        super(GatewayTimeoutException, self).__init__(*args)
