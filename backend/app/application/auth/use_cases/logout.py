class LogoutUseCase:
    """
    Logout current user.

    Stateless JWT version: no server-side token revocation yet.
    """

    def execute(self) -> None:
        return None