from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import bcrypt
from Crypto.PublicKey import RSA
from SCCrypto import SCCrypto
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

            ret_val = [{'P1K': "No such entity."}]
            return JsonResponse(ret_val, safe=False)

        else:
            hpsw = ret[0].password.encode('utf-8')

            allowed = hpsw == bcrypt.hashpw(psw, hpsw)
            if allowed:
                P1K = ret[0].private_key_part
                ret_val = [{'P1K': P1K}]
                return JsonResponse(ret_val, safe=False)
            else:
                ret_val = [{'P1K': "No permission."}]
                return JsonResponse(ret_val, safe=False)

@csrf_exempt
def exist(request):
    if request.method == 'POST':
        dct = json.loads(request.body)
        hid = dct['id']

        ret = Encryption.objects.filter(id=hid)

        if len(ret) == 0:

            ret_val = [{'retVal': "No"}]
            return JsonResponse(ret_val, safe=False)

        else:
            ret_val = [{'retVal': "Yes"}]
            return JsonResponse(ret_val, safe=False)

@csrf_exempt
def newE(request):
    if request.method == 'POST':
        dct = json.loads(request.body)

        hid = dct['id']
        psw = dct['psw']
        reqM = dct['reqM']

        ret = Encryption.objects.filter(id=hid)

        if len(ret) == 0:
            sc = SCCrypto()
            key = RSA.generate(2048)

            pKeyStr = key.publickey().exportKey('PEM')
            xord = sc.splitSK_RSA(key)

            n = Encryption(id=hid, public_key=pKeyStr, private_key_part=xord[0], recovery=reqM, password=psw)
            n.save()

            ret_val = [{'P1K': xord[1]}]
            return JsonResponse(ret_val, safe=False)

        else:
            ret_val = [{'P1K': ""}]
            return JsonResponse(ret_val, safe=False)