import base64
import sys
import os
sys.path.append('pycades')
import pycades
from error_log.views import create_item_error_log


"""
 266  /opt/cprocsp/bin/amd64/certmgr -inst -store uMy -pfx -silent -keep_exportable -pin 123456 -file /home/ubuntu/natcatparse/natcat_pfx.pfx
  324  /opt/cprocsp/bin/amd64/certmgr -inst -file "home/ubuntu/natcatparse/natcat.cer" -cont uMy -silent
  601  /opt/cprocsp/bin/<архитектура процессора>/certmgr -install -pfx -file /home/ubuntu/natcatparse/natcat.pfx -pin 123456 -silent
  602  /opt/cprocsp/bin/amd64/certmgr -install -pfx -file /home/ubuntu/natcatparse/natcat.pfx -pin 123456 -silent


"""
ACTIVE_CERT_FILE = 'active_cert.txt'


def get_active_cert_number():
    """
    Читает номер активного сертификата из файла
    Возвращает номер сертификата или None если файл не найден или пустой
    """
    try:
        if os.path.exists(ACTIVE_CERT_FILE):
            with open(ACTIVE_CERT_FILE, 'r') as f:
                cert_number = f.read().strip()
                if cert_number and cert_number.isdigit():
                    return int(cert_number)
    except (IOError, ValueError):
        pass
    return None

def about_cert():
    try:
        about_dict = {}
        store = pycades.Store()
        store.Open(
            pycades.CAPICOM_CURRENT_USER_STORE,
            pycades.CAPICOM_MY_STORE,
            pycades.CAPICOM_STORE_OPEN_MAXIMUM_ALLOWED)

        print("CAPICOM_MY_STORE: ", pycades.CAPICOM_MY_STORE)
        print("CAPICOM_MY_CONT: ", pycades.CADESCOM_CONTAINER_STORE)
        about_dict['store'] = pycades.CAPICOM_MY_STORE

        certs = store.Certificates
        print("COUNT: ", certs.Count)
        about_dict['count'] = str(certs.Count)

        # Получаем номер активного сертификата
        active_cert_number = get_active_cert_number()
        about_dict['active_cert_number'] = active_cert_number

        item_list = []
        temp_dict = {}
        for i in range(1,certs.Count+1):
            cert = certs.Item(i)
            temp_dict['item_number'] = str(i)
            temp_dict['subject'] = str(cert.SubjectName)
            temp_dict['issuer'] = str(cert.IssuerName)
            temp_dict['serial'] = str(cert.SerialNumber)
            temp_dict['thumbprint'] = str(cert.Thumbprint)
            temp_dict['valid_from'] = str(cert.ValidFromDate)
            temp_dict['valid_to'] = str(cert.ValidToDate)
            temp_dict['private_key'] = str(cert.HasPrivateKey())
            temp_dict['is_active'] = (active_cert_number == i)
            item_list.append(temp_dict)
            temp_dict = {}
        about_dict['data'] = item_list
    except Exception:
        about_dict = {}
    return about_dict



def load_cert(zapis):
    status_signature = True
    error_message = None
    store = pycades.Store()
    store.Open(
        pycades.CAPICOM_CURRENT_USER_STORE,
        pycades.CAPICOM_MY_STORE,
        pycades.CAPICOM_STORE_OPEN_MAXIMUM_ALLOWED)

    print("CAPICOM_MY_STORE: ", pycades.CAPICOM_MY_STORE)
    print("CAPICOM_MY_CONT: ", pycades.CADESCOM_CONTAINER_STORE)

    certs = store.Certificates
    print("COUNT: ", certs.Count)
    if certs.Count == 0:
        status_signature = False
        error_message = "Нет установленных сертификатов."
        return status_signature, None, error_message

    # Получаем номер активного сертификата из файла
    cert_number = get_active_cert_number()

    if cert_number is None or cert_number > certs.Count or cert_number < 1:
        print(f"Активный сертификат не найден или недействителен, используем сертификат #1")
        cert_number = 1

    print(f"Используем сертификат #{cert_number}")





    try:
        signer = pycades.Signer()
        signer.Certificate = certs.Item(cert_number)
        signer.CheckCertificate = True
        signedData = pycades.SignedData()
        signedData.Content = zapis
        signature = signedData.SignCades(signer, pycades.CADESCOM_CADES_BES)
        _signedData = pycades.SignedData()
        _signedData.VerifyCades(signature, pycades.CADESCOM_CADES_BES)
        print("Verified successfully")
        return status_signature, signature, error_message
    except Exception:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        frame = exc_traceback.tb_frame
        lineno = exc_traceback.tb_lineno
        create_item_error_log(
            frame.f_code.co_filename, exc_type, exc_value, lineno
        )
        status_signature = False
        error_message = "Не удалось подписать файл."
        return status_signature, None, error_message



    # print("--Signature--")
    # print(signature)
    # print("----")





def true_cert(zapis):
    store = pycades.Store()
    store.Open(
        pycades.CAPICOM_CURRENT_USER_STORE,
        pycades.CAPICOM_MY_STORE,
        pycades.CAPICOM_STORE_OPEN_MAXIMUM_ALLOWED
    )
    print("CAPICOM_MY_STORE: ", pycades.CAPICOM_MY_STORE)
    certs = store.Certificates
    print("COUNT: ", certs.Count)
    print(pycades.ModuleVersion())

    # Получаем номер активного сертификата из файла
    cert_number = get_active_cert_number()

    # Если номер не найден или не существует, используем первый сертификат (1)
    if cert_number is None or cert_number > certs.Count or cert_number < 1:
        print(f"Активный сертификат не найден или недействителен, используем сертификат #1")
        cert_number = 1

    print(f"Используем сертификат #{cert_number}")
    signer = pycades.Signer()
    signer.Certificate = certs.Item(cert_number)
    # signer.CheckCertificate = True
    signer.Options = pycades.CAPICOM_CERTIFICATE_INCLUDE_END_ENTITY_ONLY
    signed_data = pycades.SignedData()
    signed_data.ContentEncoding = pycades.CADESCOM_BASE64_TO_BINARY
    signed_data.Content = zapis
    signature = signed_data.SignCades(signer, pycades.CADESCOM_CADES_BES, True)
    final_signature = ''.join(signature.splitlines())
    print("--Signature--")
    print(final_signature)
    print("----")

    _signedData = pycades.SignedData()
    _signedData.ContentEncoding = pycades.CADESCOM_BASE64_TO_BINARY
    _signedData.Content = zapis
    _signedData.VerifyCades(signature, pycades.CADESCOM_CADES_BES, True)
    print("Verified successfully")

    return signature

