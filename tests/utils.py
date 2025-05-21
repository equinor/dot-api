import pytest
import json
from typing import TypeVar, Type
from pydantic import BaseModel
from httpx import Response

T = TypeVar('T', bound=BaseModel)

def parse_response_to_dtos(response: Response, dto_class: Type[T]) -> list[T]:
    content=json.loads(response.content.decode('utf-8'))
    return [dto_class.model_validate(obj) for obj in content]

def parse_response_to_dto(response: Response, dto_class: Type[T]) -> T:
    content=json.loads(response.content.decode('utf-8'))
    return dto_class.model_validate(content)

def parse_response_to_dto_test(response: Response, dto_class: Type[T]) -> T:
    try:
        return parse_response_to_dto(response, dto_class)
    except:
        pytest.fail("Response parsing encountered an exception")

def parse_response_to_dtos_test(response: Response, dto_class: Type[T]) -> list[T]:
    try:
        return parse_response_to_dtos(response, dto_class)
    except:
        pytest.fail("Response parsing encountered an exception")