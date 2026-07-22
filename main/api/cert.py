import base64
import sys
sys.path.append('pycades')
import pycades
from error_log.views import create_item_error_log


"""
 266  /opt/cprocsp/bin/amd64/certmgr -inst -store uMy -pfx -silent -keep_exportable -pin 123456 -file /home/ubuntu/natcatparse/natcat_pfx.pfx
  324  /opt/cprocsp/bin/amd64/certmgr -inst -file "home/ubuntu/natcatparse/natcat.cer" -cont uMy -silent
  601  /opt/cprocsp/bin/<архитектура процессора>/certmgr -install -pfx -file /home/ubuntu/natcatparse/natcat.pfx -pin 123456 -silent
  602  /opt/cprocsp/bin/amd64/certmgr -install -pfx -file /home/ubuntu/natcatparse/natcat.pfx -pin 123456 -silent


"""

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



    # print(cert.SerialNumber)

    try:
        signer = pycades.Signer()
        signer.Certificate = certs.Item(3)
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
    signer = pycades.Signer()
    signer.Certificate = certs.Item(3)
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

