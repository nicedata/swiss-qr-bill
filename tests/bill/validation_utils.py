from swiss_qr_bill.generator.address import Address

from swiss_qr_bill.generator.bill import Bill
from swiss_qr_bill.validator.helpers import MessageType, ValidationConstants, ValidationResult
from swiss_qr_bill.validator.validator import Validator


def assert_no_messages(result: ValidationResult):
    """Asserts that the validation succeeded with no messages"""
    assert result.has_errors is False
    assert result.has_warnings is False
    assert result.has_messages is False
    assert len(result._messages) == 0


def assert_single_error_message(result: ValidationResult, field: ValidationConstants, message_key: ValidationConstants):
    """Asserts that the validation produced a single validation error message"""
    assert result.has_errors is True
    assert result.has_warnings is False
    assert result.has_messages is True
    assert len(result._messages) == 1

    msg = result._messages[0]
    assert msg.type == MessageType.ERROR
    assert msg.field == field
    assert msg.key == message_key


def assert_single_warning_message(result: ValidationResult, field: ValidationConstants, message_key: ValidationConstants):
    """Asserts that the validation succeeded with a single warning"""
    assert result.has_errors is False
    assert result.has_warnings is True
    assert result.has_messages is True
    assert len(result._messages) == 1

    msg = result._messages[0]
    assert msg.type == MessageType.WARNING
    assert msg.field == field
    assert msg.key == message_key


def createValidPerson(self) -> Address:
    """Creates an address with valid person data"""
    address = Address()
    address.name = "Zuppinger AG"
    address.street = "Industriestrasse"
    address.house_no = "34a"
    address.postal_code = "9548"
    address.town = "Matzingen"
    address.country_code = "CH"
    return address


def validated_bill(vresult: ValidationResult) -> Bill:
    return vresult.cleaned_bill


def validate(bill: Bill) -> ValidationResult:
    """Validate the bill"""
    return Validator.validate(bill)
