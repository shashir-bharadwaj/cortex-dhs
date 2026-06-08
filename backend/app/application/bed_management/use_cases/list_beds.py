from typing import List

from app.domain.entities.bed import BedMaster
from app.domain.repositories.bed_repository import BedRepository


class ListBedsUseCase:
    """
    Use case for listing beds.
    """

    def __init__(self, bed_repository: BedRepository):
        self.bed_repository = bed_repository

    def execute(self) -> List[BedMaster]:
        return self.bed_repository.list()