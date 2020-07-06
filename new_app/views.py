# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import sys
import WXBizMsgCrypt
import traceback




@csrf_exempt
def main_callback(request):
    print "callback"
    print request.method
    print request.GET
    print request.POST
    try:
        if request.method == 'GET':
            sToken = '27T5S1'
            sEncodingAESKey = 'rkIM5ajsToHKM8r2OfJh9n97isvUdHVGa68IvrFUBpH'
            sCorpID = 'wxde725bb3d3601e9d'
            wxcpt = WXBizMsgCrypt(sToken, sEncodingAESKey, sCorpID)
            sVerifyMsgSig = request.GET.get('msg_signature', '')
            sVerifyTimeStamp = request.GET.get('timestamp', '')
            sVerifyNonce = request.GET.get('nonce', '')
            sVerifyEchoStr = request.GET.get('echostr', '').split(' ')
            sVerifyEchoStr = '+'.join(sVerifyEchoStr)
            print sVerifyMsgSig, sVerifyTimeStamp, sVerifyNonce, sVerifyEchoStr
            ret, sEchoStr = wxcpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp, sVerifyNonce, sVerifyEchoStr)
            print ret
            if (ret != 0):
                print "ERR: VerifyURL ret: " + str(ret)
                sys.exit(1)
            # 验证URL成功，将sEchoStr返回给企业号
            return HttpResponse(sEchoStr)
    except:
        traceback.print_exc()


@csrf_exempt
def data(request):
    print "callback"
    print request.method
    print request.GET
    print request.POST
    try:
        if request.method == 'GET':
            sToken = '27T5S1'
            sEncodingAESKey = 'rkIM5ajsToHKM8r2OfJh9n97isvUdHVGa68IvrFUBpH'
            sCorpID = 'wxde725bb3d3601e9d'
            wxcpt = WXBizMsgCrypt(sToken, sEncodingAESKey, sCorpID)
            sVerifyMsgSig = request.GET.get('msg_signature', '')
            sVerifyTimeStamp = request.GET.get('timestamp', '')
            sVerifyNonce = request.GET.get('nonce', '')
            sVerifyEchoStr = request.GET.get('echostr', '').split(' ')
            sVerifyEchoStr = '+'.join(sVerifyEchoStr)
            print sVerifyMsgSig, sVerifyTimeStamp, sVerifyNonce, sVerifyEchoStr
            ret, sEchoStr = wxcpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp, sVerifyNonce, sVerifyEchoStr)
            print ret
            if (ret != 0):
                print "ERR: VerifyURL ret: " + str(ret)
                sys.exit(1)
            # 验证URL成功，将sEchoStr返回给企业号
            return HttpResponse(sEchoStr)
    except:
        traceback.print_exc()


@csrf_exempt
def order(request):
    print 'myorder_callback-begin'
    print request.method
    print request.GET
    print request.POST
    sToken = '27T5S1'
    sEncodingAESKey = 'rkIM5ajsToHKM8r2OfJh9n97isvUdHVGa68IvrFUBpH'
    sCorpID = 'wxde725bb3d3601e9d'
    wxcpt = WXBizMsgCrypt(sToken, sEncodingAESKey, sCorpID)
    if request.method == 'GET':
        # 完成指令回调的校验
        sVerifyMsgSig = request.GET.get('msg_signature', '')
        sVerifyTimeStamp = request.GET.get('timestamp', '')
        sVerifyNonce = request.GET.get('nonce', '')
        sVerifyEchoStr = request.GET.get('echostr', '').split(' ')
        sVerifyEchoStr = '+'.join(sVerifyEchoStr)
        ret, sEchoStr = wxcpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp, sVerifyNonce, sVerifyEchoStr)
        print ret
        if (ret != 0):
            print "ERR: VerifyURL ret: " + str(ret)
            sys.exit(1)
        # 验证URL成功，将sEchoStr返回给企业号
        return HttpResponse(sEchoStr)
