#!/usr/bin/env python3
# *-* coding: utf-8 *-*
from oscrypto import asymmetric
from endesive import pdf
from OpenSSL.crypto import load_pkcs12
from cryptography.hazmat.primitives.serialization import pkcs12
import datetime, os
from dotenv import load_dotenv
load_dotenv()
PASSWD = os.getenv("PASSWD")

def main():
    date = datetime.datetime.utcnow() - datetime.timedelta(hours=12)
    date = date.strftime("D:%Y%m%d%H%M%S+00'00'")
    dct = {
        "aligned": 0,
        "sigflags": 3,
        "sigflagsft": 132,
        "sigpage": 0,
        "sigbutton": True,
        "sigfield": "Signature1",
        "auto_sigfield": True,
        "sigandcertify": True,
        "signaturebox": (470, 840, 570, 640),
        "signature": "Dokument podpisany cyfrowo ąćęłńóśżź",
#        "signature_img": "signature_test.png",
        "contact": "mak@trisoft.com.pl",
        "location": "Szczecin",
        "signingdate": date,
        "reason": "Dokument podpisany cyfrowo aą cć eę lł nń oó sś zż zź",
        "password": "1234",
    }
    with open("certificate.p12", "rb") as f:
        private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(f.read(), PASSWD.encode('ascii'))

        datau = open('pdf.pdf', 'rb').read()
        datas = pdf.cms.sign(datau, dct, private_key, certificate, additional_certificates)
        with open('pdf-signed-cms.pdf', 'wb') as fp:
            fp.write(datau)
            fp.write(datas)

main()
