import pytest
from sample_data import sample_bill_4, sample_bill_6, sample_bill_with_qr_iban, sample_bill_with_simple_iban
from validation_utils import assert_no_messages, assert_single_error_message, assert_single_warning_message, validate, validated_bill

from swiss_qr_bill.generator.alternative_scheme import AlternativeScheme
from swiss_qr_bill.validator.helpers import MessageType, ValidationConstants


def test_valid_QR_reference():
    REFERENCE = "00 00000 21100 00000 00000 0102"
    EXPECTED_CREDITOR_REFERENCE = "000000021100000000000001024"
    bill = sample_bill_with_qr_iban()
    bill.create_and_set_QR_reference(REFERENCE)
    val_result = validate(bill)
    val_bill = validated_bill(val_result)
    assert val_bill.reference == EXPECTED_CREDITOR_REFERENCE
    assert_no_messages(val_result)


def test_invalid_QR_reference():
    REFERENCE = "00 00000 21100 00000 00000 XXX"
    bill = sample_bill_with_qr_iban()
    with pytest.raises(TypeError):
        bill.create_and_set_QR_reference(REFERENCE)


def test_valid_creditor_reference():
    REFERENCE = "ABA TEST"
    EXPECTED_CREDITOR_REFERENCE = "RF87ABATEST"
    bill = sample_bill_with_qr_iban()
    bill.create_and_set_creditor_reference(REFERENCE)
    val_result = validate(bill)
    val_bill = validated_bill(val_result)
    assert val_bill.reference == EXPECTED_CREDITOR_REFERENCE


def test_empty_creditor_reference():
    bill = sample_bill_with_qr_iban()
    bill.create_and_set_creditor_reference("")
    val_result = validate(bill)
    val_bill = validated_bill(val_result)
    assert val_bill.reference is None


def test_valid_CHF_currency():
    CURRENCY = "CHF"
    bill = sample_bill_with_qr_iban()
    bill.currency = CURRENCY
    val_result = validate(bill)
    val_bill = validated_bill(val_result)
    assert_no_messages(val_result)
    assert val_bill.currency == CURRENCY


def test_valid_EUR_currency():
    CURRENCY = "EUR"
    bill = sample_bill_with_qr_iban()
    bill.currency = CURRENCY
    val_result = validate(bill)
    val_bill = validated_bill(val_result)
    assert_no_messages(val_result)
    assert val_bill.currency == CURRENCY


def test_invalid_USD_currency():
    CURRENCY = "USD"
    bill = sample_bill_with_qr_iban()
    bill.currency = CURRENCY
    val_result = validate(bill)
    assert_single_error_message(val_result, ValidationConstants.FIELD_CURRENCY, ValidationConstants.KEY_CURRENCY_NOT_CHF_OR_EUR)


def test_missing_currency():
    CURRENCY = None
    bill = sample_bill_with_qr_iban()
    bill.currency = CURRENCY
    val_result = validate(bill)
    assert_single_error_message(val_result, ValidationConstants.FIELD_CURRENCY, ValidationConstants.KEY_FIELD_VALUE_MISSING)


def test_empty_currency():
    CURRENCY = ""
    bill = sample_bill_with_qr_iban()
    bill.currency = CURRENCY
    val_result = validate(bill)
    assert_single_error_message(val_result, ValidationConstants.FIELD_CURRENCY, ValidationConstants.KEY_FIELD_VALUE_MISSING)


def test_no_amount():
    bill = sample_bill_with_qr_iban()
    bill.amount = None
    val_result = validate(bill)
    val_bill = validated_bill(val_result)
    assert_no_messages(val_result)
    assert val_bill.amount is None


def test_amount_valid():
    AMOUNT = 100.15
    bill = sample_bill_with_qr_iban()
    bill.amount = AMOUNT
    val_result = validate(bill)
    val_bill = validated_bill(val_result)
    assert_no_messages(val_result)
    assert val_bill.amount == AMOUNT


def test_amount_undeflow():
    AMOUNT = 0.01
    bill = sample_bill_with_qr_iban()
    bill.amount = AMOUNT
    val_result = validate(bill)
    assert_single_error_message(val_result, ValidationConstants.FIELD_AMOUNT, ValidationConstants.KEY_AMOUNT_OUTSIDE_VALID_RANGE)


def test_amount_overflow():
    AMOUNT = 1000000000.0
    bill = sample_bill_with_qr_iban()
    bill.amount = AMOUNT
    val_result = validate(bill)
    assert_single_error_message(val_result, ValidationConstants.FIELD_AMOUNT, ValidationConstants.KEY_AMOUNT_OUTSIDE_VALID_RANGE)


def test_valid_CH_account():
    ACCOUNT = "CH4431999123000889012"
    bill = sample_bill_with_qr_iban()
    bill.account = ACCOUNT
    val_result = validate(bill)
    val_bill = validated_bill(val_result)
    assert_no_messages(val_result)
    assert val_bill.account == ACCOUNT


def test_valid_LI_account():
    ACCOUNT = "LI5608800000020940808"
    bill = sample_bill_with_simple_iban()
    bill.account = ACCOUNT
    val_result = validate(bill)
    val_bill = validated_bill(val_result)
    assert_no_messages(val_result)
    assert val_bill.account == ACCOUNT


def test_valid_account_with_spaces():
    ACCOUNT = " CH44 3199 9123 0008 89012 "
    bill = sample_bill_with_qr_iban()
    bill.account = ACCOUNT
    val_result = validate(bill)
    val_bill = validated_bill(val_result)
    assert_no_messages(val_result)
    assert val_bill.account == ACCOUNT.strip().replace(" ", "")


def test_valid_unstructured_message():
    MESSAGE = "Bill no 39133"
    bill = sample_bill_with_qr_iban()
    bill.unstructured_message = MESSAGE
    val_result = validate(bill)
    val_bill = validated_bill(val_result)
    assert_no_messages(val_result)
    assert val_bill.unstructured_message == MESSAGE


def test_empty_instructured_message():
    bill = sample_bill_with_qr_iban()
    bill.unstructured_message = "      "
    val_result = validate(bill)
    val_bill = validated_bill(val_result)
    assert_no_messages(val_result)
    assert val_bill.unstructured_message is None


def test_unstructured_message_with_leading_and_trailing_whitespace():
    MESSAGE = "  Bill no 39133 "
    bill = sample_bill_with_qr_iban()
    bill.unstructured_message = MESSAGE
    val_result = validate(bill)
    val_bill = validated_bill(val_result)
    assert_no_messages(val_result)
    assert val_bill.unstructured_message == MESSAGE.strip()


def test_clipped_unstructured_message():
    bill = sample_bill_4()
    bill.unstructured_message = "123456789-123456789-123456789-123456789-123456789-123456789-123456789-123456789-123456789-123456789-123456789-123456789-123456789-123456789-AAAAAA"
    assert len(bill.unstructured_message) == 146
    val_result = validate(bill)
    val_bill = validated_bill(val_result)
    assert_single_warning_message(val_result, ValidationConstants.FIELD_UNSTRUCTURED_MESSAGE, ValidationConstants.KEY_FIELD_VALUE_CLIPPED)
    assert len(val_bill.unstructured_message) == 140


def test_too_long_bill_information():
    bill = sample_bill_with_qr_iban()
    bill.unstructured_message = None
    bill.bill_information = "//AA4567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789x"
    val_result = validate(bill)
    assert_single_error_message(val_result, ValidationConstants.FIELD_BILL_INFORMATION, ValidationConstants.KEY_FIELD_VALUE_TOO_LONG)


def test_invalid_bill_information_1():
    bill = sample_bill_with_qr_iban()
    bill.bill_information = "ABCD"
    val_result = validate(bill)
    assert_single_error_message(val_result, ValidationConstants.FIELD_BILL_INFORMATION, ValidationConstants.KEY_BILL_INFO_INVALID)


def test_invalid_bill_information_2():
    bill = sample_bill_with_qr_iban()
    bill.bill_information = "//A"
    val_result = validate(bill)
    assert_single_error_message(val_result, ValidationConstants.FIELD_BILL_INFORMATION, ValidationConstants.KEY_BILL_INFO_INVALID)


def test_too_long_unstr_message_bill_info():
    bill = sample_bill_6()
    assert len(bill.unstructured_message) + len(bill.bill_information) == 140
    bill.unstructured_message = bill.unstructured_message + "A"
    val_result = validate(bill)
    assert val_result.has_errors is True
    assert val_result.has_warnings is False
    assert val_result.has_messages is True
    assert len(val_result._messages) == 2

    msg = val_result._messages[0]
    assert msg.type == MessageType.ERROR
    assert msg.field == ValidationConstants.FIELD_UNSTRUCTURED_MESSAGE
    assert msg.key == ValidationConstants.KEY_ADDITIONAL_INFO_TOO_LONG

    msg = val_result._messages[1]
    assert msg.type == MessageType.ERROR
    assert msg.field == ValidationConstants.FIELD_BILL_INFORMATION
    assert msg.key == ValidationConstants.KEY_ADDITIONAL_INFO_TOO_LONG


def test_too_many_alt_schemes():
    bill = sample_bill_with_qr_iban()
    bill.alternative_schemes.append(AlternativeScheme("Ultraviolet", "UV;UltraPay005;12345"))
    bill.alternative_schemes.append(AlternativeScheme("Xing Yong", "XY;XYService;54321"))
    bill.alternative_schemes.append(AlternativeScheme("Too Much", "TM/asdfa/asdfa/"))
    val_result = validate(bill)
    assert_single_error_message(val_result, ValidationConstants.FIELD_ALTERNATIVE_SCHEMES, ValidationConstants.KEY_ALT_SCHEME_MAX_EXCEEDED)


def test_too_long_alt_scheme_instructions():
    bill = sample_bill_with_qr_iban()
    bill.alternative_schemes.clear()
    bill.alternative_schemes.append(AlternativeScheme("Ultraviolet", "UV;UltraPay005;12345;xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"))
    bill.alternative_schemes.append(AlternativeScheme("Xing Yong", "XY;XYService;54321"))
    val_result = validate(bill)
    assert_single_error_message(val_result, ValidationConstants.FIELD_ALTERNATIVE_SCHEMES, ValidationConstants.KEY_FIELD_VALUE_TOO_LONG)


#
