from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from Crypto.PublicKey import RSA
from SCCrypto import SCCrypto

@csrf_exempt
def trial(request):
    if request.method == 'GET':

        sc = SCCrypto()

        key = RSA.generate(2048)
        keyStr = key.exportKey('PEM')

        xord = sc.splitSK_RSA(key)


        ret_val = [{'SK': keyStr, 'ClK': xord[0]}]
        return JsonResponse(ret_val, safe=False)