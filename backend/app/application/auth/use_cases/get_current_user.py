class GetCurrentUserUseCase:
    """
    Return current authenticated user context.
    """

    def execute(self, current_user):
        return current_user