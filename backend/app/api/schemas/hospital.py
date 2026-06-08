from pydantic import BaseModel


class CreateHospitalRequest(BaseModel):
    """
    Request schema for creating a hospital.
    """

    name: str
    code: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    contact_number: str | None = None
    email: str | None = None


class CreateHospitalUnitRequest(BaseModel):
    """
    Request schema for creating a hospital unit.
    """

    name: str
    code: str | None = None


class HospitalUnitResponse(BaseModel):
    """
    Public hospital unit response.
    """

    id: int
    hospital_id: int
    name: str
    code: str | None = None
    is_active: bool

    class Config:
        from_attributes = True


class HospitalListItemResponse(BaseModel):
    """
    Public hospital list item response.
    """

    id: int
    name: str

    class Config:
        from_attributes = True


class HospitalDetailResponse(BaseModel):
    """
    Public hospital detail response.
    """

    id: int
    name: str
    code: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    contact_number: str | None = None
    email: str | None = None

    class Config:
        from_attributes = True


class HospitalUnitsResponse(BaseModel):
    """
    Public hospital units response.
    """

    units: list[HospitalUnitResponse]