from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from Crypto.PublicKey import RSA
from SCCrypto import SCCrypto
from api.models import Encryption


@csrf_exempt
def trial(request):
    if request.method == 'POST':
        dct = json.loads(request.body)
        hid = dct['id']

        ret = Encryption.objects.filter(id=hid)

        if len(ret) == 0:
            sc = SCCrypto()
            key = RSA.generate(2048)

            pKeyStr = key.publickey().exportKey('PEM')
            xord = sc.splitSK_RSA(key)

            n = Encryption(id=hid, public_key=pKeyStr, private_key_part=xord[0], recovery=hid, password="antananarive")
            n.save()

            ret_val = [{'P1K': xord[0]}]
            return JsonResponse(ret_val, safe=False)
        else:
            P1K = ret[0].private_key_part
            ret_val = [{'P1K': P1K}]
            return JsonResponse(ret_val, safe=False)