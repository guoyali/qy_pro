# coding:utf-8

# 1.企业首次安装完三方应用的回调及逻辑处理
# 2.从企业微信工作台打开三方应用的跳转逻辑及相关绑定业务逻辑处理
# 3.星链和星轨为何共用了一个跳转页，实现原理是什么
# 4.通讯里信息的获取--成员信息的获取及展示
# 5.jssdk 相关开发--企业微信对于部分信息不直接返回，需要结合 jssdk 来使用，后续可能还会有调整


# 1、需要拿到的参数
# 获取服务商的token   -provider_access_token （用于服务商级别的接口调用，比如登录授权、推广二维码等。）
# https://qyapi.weixin.qq.com/cgi-bin/service/get_provider_token
# {
#     "corpid":"xxxxx",
#     "provider_secret":"xxx"
#  }
# 第三方应用的token    -suite_access_token （用于获取第三方应用的预授权码，获取授权企业信息等。）
# https://qyapi.weixin.qq.com/cgi-bin/service/get_suite_token
# {
#     "suite_id":"wwddddccc7775555aaa" ,
#     "suite_secret": "ldAE_H9anCRN21GKXVfdAAAAAAAAAAAAAAAAAA",
#     "suite_ticket": "Cfp0_givEagXcYJIztF6sfbdmIZCmpaR8ZBsvJEFFNBrWmnD5-CGYJ3_NhYexMyw"
# }
# 授权企业的token        -access_token     （用于操作授权企业相关接口，如通讯录管理，消息推送等。）
# https://qyapi.weixin.qq.com/cgi-bin/service/get_corp_token?suite_access_token=SUITE_ACCESS_TOKEN
# {
#      "auth_corpid": "auth_corpid_value",   # 授权方corpid
#      "permanent_code": "code_value"        # 永久授权码，通过get_permanent_code获取
#  }
# 2、获取预授权码     -pre_auth_code     （预授权码用于企业授权时的第三方服务商安全验证。）
# https://qyapi.weixin.qq.com/cgi-bin/service/get_pre_auth_code?suite_access_token=SUITE_ACCESS_TOKEN
# 3、获取永久授权码     -permanent_code    （该API用于使用临时授权码换取授权方的永久授权码，并换取授权信息、企业access_token。）
# https://qyapi.weixin.qq.com/cgi-bin/service/get_permanent_code?suite_access_token=SUITE_ACCESS_TOKEN
# {
#     "auth_code": "auth_code_value"    # 临时授权码
# }
# 获取企业授权信息    -agentid   授权方应用id    -corpid   授权方企业微信id
#  https://qyapi.weixin.qq.com/cgi-bin/service/get_auth_info?suite_access_token=SUITE_ACCESS_TOKEN
# {
#      "auth_corpid": "auth_corpid_value",   # 授权方corpid
#      "permanent_code": "code_value"        # 永久授权码
#  }
# 4、获取管理员权限
# 5、回调接口    数据回调url      指令回调url    token     EncodingAESKey
# 通过 Token、EncodingAESKey、CorpID（服务商CorpID）计算出Signature与URL的GET参数中的Signature作对比，如果一样就验证通过
# 数据回调是直接调用，查看是否接口可以调通。指令回调是给后端的接口传送推一些数据，比如suit_token等。
# 整体逻辑：
# a、从request中拿到签名（signature）、时间戳(timestamp)、随机字符串(nonce) 和验证回调的URL的有效性传入的字符串(echostr)
# b、需要对echostr进行解密操作，然后再将解密后的值返回给企业微信，这样就证明这个URL可以对密文进行解密。是可以调通的。
#    注意：这个时间在实例化WXBizMsgCrypt用的是corpId。 WXBizMsgCrypt是企业微信提供的工具类。
# c、指令回调需要传递一些数据到后端接口，这时候需要将这些数据（request.post）sMsg，然后再将这个sMsg进行解密，转化成xml文件，然后根据xml文件中的类型，进行操作。注意：这个在实例化的时候用的是suiteID。
#    得到sMsg，然后方法得到的sMsg解密，然后再解析xml，根据xml中的 InfoType得到不同类型的回调数据
# 授权成功通知    InfoType：create_auth   存入数据库
# 变更授权通知    InfoType：change_auth   修改授权范围
# 取消授权通知    InfoType：cancel_auth   从数据库删除
# 6、获取二维码  ——扫码登陆第三方网站
# https://open.work.weixin.qq.com/wwopen/sso/qrConnect?appid=CORPID&agentid=AGENTID&redirect_uri=REDIRECT_URI&state=STATE
# usertype -支持登录的类型。admin代表管理员登录（使用微信扫码）,member代表成员登录（使用企业微信扫码），默认为admin
# 7、获取登录用户信息   --user_info
# https://qyapi.weixin.qq.com/cgi-bin/service/get_login_info?access_token=PROVIDER_ACCESS_TOKEN
# {
#     "auth_code":"xxxxx"   # 授权企业微信管理员登录产生的code
#  }
# 获取用户姓名（2020.6.30起）  user_info['userid']
# https://qyapi.weixin.qq.com/cgi-bin/user/get?access_token=ACCESS_TOKEN&userid=USERID
# 8、发送消息
# https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=ACCESS_TOKEN
# {
#    "touser" : "UserID1|UserID2|UserID3",   # 指定接收消息的成员，成员ID列表
#    "toparty" : "PartyID1|PartyID2",        # 指定接收消息的部门，部门ID列表
#    "totag" : "TagID1 | TagID2",            # 指定接收消息的标签，标签ID列表
#    "msgtype" : "text",
#    "agentid" : 1,                          # 企业应用的id
#    "text" : {
#        "content" : "你的快递已到，请携带工卡前往邮件中心领取。\n出发前可查看<a href=\"http://work.weixin.qq.com\">邮件中心视频实况</a>，聪明避开排队。"
#    },
#    "safe":0,
#    "enable_id_trans": 0,
#    "enable_duplicate_check": 0,
#    "duplicate_check_interval": 1800
# }
# 9、工作台跳转 --网页授权跳转第三方
# 文档：https://open.work.weixin.qq.com/api/doc/10975#%E7%BD%91%E9%A1%B5%E6%8E%88%E6%9D%83%E7%99%BB%E5%BD%95%E7%AC%AC%E4%B8%89%E6%96%B9
# https://open.weixin.qq.com/connect/oauth2/authorize?appid=APPID&redirect_uri=REDIRECT_URI&response_type=code&scope=SCOPE&state=STATE#wechat_redirect
# snsapi_base：静默授权，可获取成员的的基础信息  UserId与DeviceId
# redirect_uri?code=CODE&state=STATE  获取code   企业可根据code参数获得员工的userid。code长度最大为512字节。
# 获取成员信息
# https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo?access_token=ACCESS_TOKEN&code=CODE
# {
#    "errcode": 0,
#    "errmsg": "ok",
#    "UserId":"USERID",       # 绑定到手机号一致的星链账户
#    "DeviceId":"DEVICEID",
#    "user_ticket": "USER_TICKET"，
#    "expires_in":7200
# }
# 10、获取通讯录成员信息   （只能拉取token对应的应用的权限范围内的部门列表里的成员信息）
# department_id 获取的部门id， 部门id。获取指定部门及其下的子部门。 如果不填，默认获取全量组织架构
# https://qyapi.weixin.qq.com/cgi-bin/department/list?access_token=ACCESS_TOKEN&id=ID
# https://qyapi.weixin.qq.com/cgi-bin/user/list?access_token=ACCESS_TOKEN&department_id=DEPARTMENT_ID
# 11、jssdk 相关开发


