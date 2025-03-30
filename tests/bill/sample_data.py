from swiss_qr_bill.generator.address import Address
from swiss_qr_bill.generator.alternative_scheme import AlternativeScheme
from swiss_qr_bill.generator.bill import Bill
from swiss_qr_bill.generator.enums import Language, SeparatorType


def sample_bill_with_qr_iban():
    bill = Bill()
    bill.format.language = Language.EN
    bill.account = "CH44 3199 9123 0008  89012"
    creditor = Address()
    creditor.name = "Robert Schneider AG"
    creditor.street = "Rue du Lac"
    creditor.house_no = "1268/2/22"
    creditor.postal_code = "2501"
    creditor.town = "Biel"
    creditor.country_code = "CH"
    bill.creditor = creditor
    bill.amount = 123949.75
    bill.currency = "CHF"
    debtor = Address()
    debtor.name = "Pia-Maria Rutschmann-Schnyder"
    debtor.street = "Grosse Marktgasse"
    debtor.house_no = "28"
    debtor.postal_code = "9400"
    debtor.town = "Rorschach"
    debtor.country_code = "CH"
    bill.debtor = debtor
    bill.reference = "210000 000 00313 9471430009017"
    bill.unstructured_message = "Instruction of 15.09.2019"
    bill.bill_information = "//S1/01/20170309/11/10201409/20/14000000/22/36958/30/CH106017086/40/1020/41/3010"
    bill.alternative_schemes.append(AlternativeScheme("Ultraviolet", "UV;UltraPay005;12345"))
    bill.alternative_schemes.append(AlternativeScheme("Xing Yong", "XY;XYService;54321"))
    return bill


def sample_bill_with_simple_iban():
    bill = Bill()
    bill.format.language = Language.FR
    bill.account = "CH74 0070 0110 0061 1600 2"
    creditor = Address()
    creditor.name = "Robert Schneider AG"
    creditor.street = "Rue du Lac"
    creditor.house_no = "1268/2/22"
    creditor.postal_code = "2501"
    creditor.town = "Biel"
    creditor.country_code = "CH"
    bill.creditor = creditor
    bill.amount = 123949.75
    bill.currency = "CHF"
    debtor = Address()
    debtor.name = "Pia-Maria Rutschmann-Schnyder"
    debtor.street = "Grosse Marktgasse"
    debtor.house_no = "28"
    debtor.postal_code = "9400"
    debtor.town = "Rorschach"
    debtor.country_code = "CH"
    bill.debtor = debtor
    bill.reference = "RF18539007547034"
    return bill


def sample_bill_4():
    bill = Bill()
    bill.format.language = Language.IT
    bill.format.separator_type = SeparatorType.SOLID_LINE
    bill.account = "CH3709000000304442225"
    creditor = Address()
    creditor.name = "ABC AG"
    creditor.postal_code = "3000"
    creditor.town = "Bern"
    creditor.country_code = "CH"
    bill.creditor = creditor
    bill.currency = "CHF"
    bill.unstructured_message = ""
    return bill


def sample_bill_6():
    bill = Bill()
    bill.format.language = Language.EN
    bill.account = "CH44 3199 9123 0008  89012"
    creditor = Address()
    creditor.name = "Herrn und Frau Ambikaipagan & Deepshikha Thirugnanasampanthamoorthy"
    creditor.address_line1 = "c/o Pereira De Carvalho, Conrad-Ferdinand-Meyer-Strasse 317 Wohnung 7B"
    creditor.address_line2 = "9527 Niederhelfenschwil bei Schönholzerswilen im Kanton St. Gallen"
    creditor.country_code = "CH"
    bill.creditor = creditor
    bill.currency = "EUR"
    bill.reference = "210000 000 00313 9471430009017"
    bill.unstructured_message = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed"
    bill.bill_information = "//S1/01/20170309/11/10201409/20/14000000/22/36958/30/CH106017086/40/1020/41/3010"
    return bill
