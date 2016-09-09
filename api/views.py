from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import bcrypt
from Crypto.PublicKey import RSA
from SCCrytpo.SCCryptoUtil import SCCrypto
from api.models import Encryption


@csrf_exempt
def getPK(request):
    if request.method == 'POST':
        dct = json.loads(request.body)
        hid = dct['id']
        psw = dct['psw']
        psw = psw.encode('utf-8')


        ret = Encryption.objects.filter(id=hid)

        if len(ret) == 0:

            ret_val = [{'Ans': "No such entity"}]
            return JsonResponse(ret_val, safe=False)

        else:
            hpsw = ret[0].password.encode('utf-8')

            allowed = hpsw == bcrypt.hashpw(psw, hpsw)
            if allowed:
                PK = ret[0].public_key
                ret_val = [{'PK': PK, 'Ans': "OK"}]
                return JsonResponse(ret_val, safe=False)
            else:
                ret_val = [{'Ans': "No permission"}]
                return JsonResponse(ret_val, safe=False)

@csrf_exempt
def exist(request):
    if request.method == 'POST':
        dct = json.loads(request.body)
        hid = dct['id']

        ret = Encryption.objects.filter(id=hid)

        if len(ret) == 0:

            ret_val = [{'Ans': "No"}]
            return JsonResponse(ret_val, safe=False)

        else:
            ret_val = [{'Ans': "Yes"}]
            return JsonResponse(ret_val, safe=False)

@csrf_exempt
def newE(request):
    if request.method == 'POST':
        dct = json.loads(request.body)

        hid = dct['id']
        psw = dct['psw']
        recM = dct['recM']

        ret = Encryption.objects.filter(id=hid)

        if len(ret) == 0:
            sc = SCCrypto()
            key = RSA.generate(2048)

            pKeyStr = key.publickey().exportKey('PEM')
            xord = sc.splitSK_RSA(key)

            n = Encryption(id=hid, public_key=pKeyStr, private_key_part=xord[0], recovery=recM, password=psw)
            n.save()

            ret_val = [{'Ans': "OK", 'PrKPart': xord[1], 'PK': pKeyStr}]
            return JsonResponse(ret_val, safe=False)

        else:
            ret_val = [{'Ans': "Duplicate"}]
            return JsonResponse(ret_val, safe=False)