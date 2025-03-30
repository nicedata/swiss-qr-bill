from swiss_qr_bill import Address
from swiss_qr_bill.generator.enums import AddressType


def _create_structured_address() -> Address:
    address = Address()
    address.name = "Cornelia Singer"
    address.street = "Alte Landstrasse"
    address.house_no = "73"
    address.postal_code = "3410"
    address.town = "Hunzenschwil"
    address.country_code = "CH"
    return address


def _create_combined_element_address() -> Address:
    address = Address()
    address.name = "Cornelia Singer"
    address.address_line1 = "Alte Landstrasse 75"
    address.address_line2 = "8702 Zollikon"
    address.country_code = "CH"
    return address


def test_undetermined():
    address = Address()
    assert address.type is AddressType.UNDETERMINED


def test_set_name():
    VALUE = "Martin Mohnhaupt"
    address = Address()
    address.name = VALUE
    assert address.name == VALUE


def test_set_address_line1():
    VALUE = "Route de La Plaine 90"
    address = Address()
    address.address_line1 = VALUE
    assert address.address_line1 == VALUE
    assert address.type is AddressType.COMBINED_ELEMENTS


def test_set_address_line2():
    VALUE = "1283 La Plaine"
    address = Address()
    address.address_line2 = VALUE
    assert address.address_line2 == VALUE
    assert address.type is AddressType.COMBINED_ELEMENTS


def test_set_street():
    VALUE = "1283 La Plaine"
    address = Address()
    address.street = VALUE
    assert address.street == VALUE
    assert address.type == AddressType.STRUCTURED


def test_set_house_no():
    STR_VALUE = "40B"
    INT_VALUE = 40
    address = Address()
    # Feed with an int
    address.house_no = INT_VALUE
    assert address.house_no == str(INT_VALUE)
    assert address.type == AddressType.STRUCTURED

    # Feed with a string
    address.house_no = STR_VALUE
    assert address.house_no == STR_VALUE
    assert address.type == AddressType.STRUCTURED


def test_set_postal_code():
    STR_VALUE = "1283"
    INT_VALUE = 1283
    address = Address()
    # Feed with an int
    address.postal_code = INT_VALUE
    assert address.postal_code == STR_VALUE
    assert address.type == AddressType.STRUCTURED

    # Feed with a string
    address.postal_code = STR_VALUE
    assert address.postal_code == STR_VALUE
    assert address.type == AddressType.STRUCTURED


def test_set_town():
    VALUE = "La Plaine"
    address = Address()
    address.town = VALUE
    assert address.town == VALUE
    assert address.type == AddressType.STRUCTURED


def test_country_code():
    #! Test empty countries
    VALUE = "FL"
    address = Address()
    address.country_code = VALUE
    assert address.country_code == VALUE


def test_conflict_1():
    VALUE = "Rue du Village"
    address = Address()
    address.street = VALUE
    address.address_line1 = VALUE
    assert address.type == AddressType.CONFLICTING


def test_conflict_2():
    VALUE = "33"
    address = Address()
    address.postal_code = VALUE
    address.address_line1 = VALUE
    assert address.type == AddressType.CONFLICTING


def test_conflict_3():
    VALUE = 1283
    address = Address()
    address.house_no = VALUE
    address.address_line2 = VALUE
    assert address.type == AddressType.CONFLICTING


def test_conflict_4():
    VALUE = "Genève"
    address = Address()
    address.town = VALUE
    address.address_line2 = VALUE
    assert address.type == AddressType.CONFLICTING


def test_equal_objects_structured():
    address1 = _create_structured_address()
    address2 = _create_structured_address()
    assert address1 == address2


def test_equal_objects_combined():
    address1 = _create_combined_element_address()
    address2 = _create_combined_element_address()
    assert address1 == address2


def test_clear_structured():
    address1 = _create_structured_address()
    address1.clear()
    assert address1.type == AddressType.UNDETERMINED
    assert address1.address_line1 is None
    assert address1.address_line2 is None
    assert address1.street is None
    assert address1.house_no is None
    assert address1.postal_code is None
    assert address1.town is None
    assert address1.country_code is None


def test_clear_combined():
    address1 = _create_combined_element_address()
    address1.clear()
    assert address1.type == AddressType.UNDETERMINED
    assert address1.address_line1 is None
    assert address1.address_line2 is None
    assert address1.street is None
    assert address1.house_no is None
    assert address1.postal_code is None
    assert address1.town is None
    assert address1.country_code is None


def test_equals_trivial():
    address = _create_combined_element_address()
    assert address == address
    assert address is not None
    assert address != "XXX"


def test_equals():
    address1 = _create_combined_element_address()
    address2 = _create_combined_element_address()
    assert address1 == address2
    address2.country_code = "FR"
    assert address1 != address2
