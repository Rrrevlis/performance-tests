from pydantic import BaseModel, HttpUrl

class DocumentSchema(BaseModel):
    """
    Описание структуры документа.
    """
    url: HttpUrl
    document: str


class GetTariffDocumentResponseSchema(BaseModel):
    """
    Описание структуры ответа на запрос получения тарифа по счету.
    """
    tariff: DocumentSchema


class GetContractDocumentResponseSchema(BaseModel):
    """
    Описание структуры ответа на запрос получения контракта по счету.
    """
    contract: DocumentSchema
