from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db


class DBProvider:
    """
    Provider class for low-level database dependencies.

    Responsibility:
    ---------------
    Expose a shared SQLAlchemy session dependency that can be reused
    by repository providers and, indirectly, by feature-specific providers.
    """

    @staticmethod
    def get_db_session(db: Session = Depends(get_db)) -> Session:
        """
        Return the active SQLAlchemy session.

        Why keep this in a provider:
        ----------------------------
        This gives us one shared DB entry point for all repository
        construction, instead of importing `get_db` everywhere.
        """
        return db