class NegativeBalanceError(Exception):
    """Вызывается, когда начальный баланс отрицательный"""
    pass


class WalletNotFound(Exception):
    """Вызывается, когда кошелек или несколько кошельков не найдены"""
    pass


class DatabaseError(Exception):
    """Вызывается, когда операция не прошла в БД"""
    pass


class OperationBalanceError(Exception):
    """Вызывается, когда операция не соответсвуюет правилам"""
    pass
