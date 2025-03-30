from swiss_qr_bill.generator.alternative_scheme import AlternativeScheme


def test_default_constructor():
    scheme = AlternativeScheme()
    assert scheme.name is None
    assert scheme.instruction is None


def test_constructor():
    NAME = "Paymit"
    INSTRUCTION = "PM,12341234,1241234"
    schema = AlternativeScheme(NAME, INSTRUCTION)
    assert schema.name == NAME
    assert schema.instruction == INSTRUCTION


def test_equals():
    NAME = "Paymit"
    INSTRUCTION = "PM,12341234,1241234"
    schema_1 = AlternativeScheme(NAME, INSTRUCTION)
    schema_2 = AlternativeScheme(NAME, INSTRUCTION)
    assert schema_1 == schema_2
    schema_2.name = "TWINT"
    assert schema_1 != schema_2
