import base64
import hashlib, json
import random
from urllib.parse import urlencode
import redis
from django.conf import settings
from django.db import transaction
from django.http import JsonResponse
from django.views.generic.base import View
from authorization.views import make_token
from common.logging_check import logging_check
from users.models import Users, Address, WeiboUsers
from users.tasks import send_active_email

r = redis.Redis(host='127.0.0.1', port=6379, db=0, password='123456')


class UsersView(View):
    def get(self, request):
        return JsonResponse({'code': 200, 'data': 'hello'})

    def post(self, request):
        data = request.body
        # 验证提交
        if not data:
            return JsonResponse({'code': 400, 'error': 'Please give me data'})
        json_obj = json.loads(data.decode())
        username = json_obj.get('uname')
        password = json_obj.get('password')
        email = json_obj.get('email')
        phone = json_obj.get('phone')
        # 验证表单内容
        if not username and not password and not email and not phone:
            return JsonResponse({'code': 400, 'error': {"message": 'Please give me data'}})
        old_user = Users.objects.filter(username=username)
        if old_user:
            return JsonResponse({'code': 400, 'error': {"message": 'The username is existed'}})
        m = hashlib.md5()
        m.update(password.encode())
        b64_password = m.hexdigest()
        try:
            Users.objects.create(username=username, password=b64_password, phone=phone, email=email)
        except Exception as e:
            return JsonResponse({'code': 200, 'error': {"message": '注册失败'}})
        int_random = random.randint(1000, 9999)
        code_str = username + "_" + str(int_random)
        code_str_bs = base64.urlsafe_b64encode(code_str.encode()).decode()
        r.set("email_active_%s" % (username), code_str)
        active_url = 'http://127.0.0.1:7000/dadashop/templates/active.html?code=%s' % (code_str_bs)
        send_active_email.delay(email, active_url)
        return JsonResponse({'code': 200, "username": username, 'data': {'token': make_token(username)}})

    def put(self, request):
        return JsonResponse({'code': 200, 'data': 'hello'})

    def delete(self, request):
        return JsonResponse({'code': 200, 'data': 'hello'})


class AddressView(View):
    @logging_check
    def get(self, request, username, id):
        all_user = Address.objects.filter(uid=request.myuser)
        if not all_user:
            return JsonResponse({'code': 200, 'data': {
                "addresslist": [],
            }})
        res = []
        for add in all_user:
            res.append({
                'id': 123456,  # 地址id
                'address': add.address,
                'receiver': add.receiver,
                'is_default': add.isDefault,
                'tag': add.tag,
                'receiver_mobile': add.receiver_mobile,
                'postcode': add.postacode,
            })
        return JsonResponse({'code': 200, 'data': {
            "addresslist": res,
        }})

    @logging_check
    def post(self, request, username, id):
        user = request.myuser
        if username != user.username:
            return JsonResponse({'code': 500, 'error': "The request is illegal"})
        body = json.loads(request.body.decode())
        receiver = body.get('receiver')
        address = body.get('address')
        receiver_phone = body.get('receiver_phone')
        postcode = body.get('postcode')
        tag = body.get('tag')
        old_user = Address.objects.filter(uid_id=user)
        if not old_user:
            isdefault = True
        else:
            isdefault = False
        Address.objects.create(
            receiver=receiver,
            address=address,
            postacode=postcode,
            receiver_mobile=receiver_phone,
            tag=tag,
            uid=user,
            isDefault=isdefault
        )
        res = []
        all_user = Address.objects.filter(uid=user)
        for add in all_user:
            res.append({
                'id': 123456,  # 地址id
                'address': add.address,
                'receiver': add.receiver,
                'is_default': add.isDefault,
                'tag': add.tag,
                'receiver_mobile': add.receiver_mobile,
                'postcode': add.postacode,
            })
        return JsonResponse({'code': 200, 'data': {
            "addresslist": res,
        }})

    def put(self, request):
        pass

    def delete(self, request):
        pass


def user_active(request):
    if request.method != "GET":
        return JsonResponse({'code': 400, 'error': 'Please user get !!'})
    code = request.GET.get('code')
    code_str = base64.urlsafe_b64decode(code.encode()).decode()
    username, rcode = code_str.split('_')
    old_data = r.get("email_active_%s" % (username)).decode()
    if code_str != old_data:
        return JsonResponse({'code': 500, 'error': 'Code is error'})
    user = Users.objects.filter(username=username)[0]
    user.isActive = True
    user.save()
    r.delete("email_active_%s" % (username))
    return JsonResponse({'code': 200, 'data': '激活成功'})


class OAuthWeiboUrlView(View):
    def get(self, request):
        return JsonResponse({'code': 200, 'oauth_url': get_weibo_login_url()})


def get_weibo_login_url():
    params = {
        "response_type": 'code',
        'client_id': settings.WEIBO_CLIEND_ID,
        'redirect_uri': settings.WEIBO_REDIRECT_URL,
        'scope': '',
    }
    weibo_url = "https://api.weibo.com/oauth2/authorize?"
    url = weibo_url + urlencode(params)
    return url


class OAuthWeiboView(View):
    def get(self, request):
        # 获取code
        code = request.GET.get('code')
        # 想微博发请求
        try:
            user_info = get_access_token(code)
        except Exception as e:
            return JsonResponse({'code': 202, 'error': {'message': "WeiBo server is busy--"}})
        print(user_info)
        wbuid = user_info.get('uid')
        access_token = user_info.get('access_token')
        try:
            weibo_user = WeiboUsers.objects.get(wbuid=wbuid)
        except Exception as e:
            # 创建数据 暂时不绑定uid  等待用户注册
            WeiboUsers.objects.create(wbuid=wbuid, access_token=access_token)
            return JsonResponse({'code': 201, 'uid': wbuid})
        else:
            # 无报错  该用户之前用微博登录过
            uid = weibo_user.uid
            if uid:
                token = make_token(uid.username)
                #  之前绑定过 则认为当前为正常登录 照常签发token
                return JsonResponse({'code': 200, 'data': {'token': token}, "username": uid.username})
            else:
                #  之前微博登录过 没有绑定 去注册 则认为当前去绑定微博和商城用户id
                return JsonResponse({'code': 201, 'uid': wbuid})

    def post(self, request):
        data = request.body
        # 验证提交
        if not data:
            return JsonResponse({'code': 400, 'error': 'Please give me data'})
        json_obj = json.loads(data.decode())
        username = json_obj.get('username')
        password = json_obj.get('password')
        email = json_obj.get('email')
        phone = json_obj.get('phone')
        wbid = json_obj.get('uid')
        # 验证表单内容
        if not username and not password and not email and not phone:
            return JsonResponse({'code': 400, 'error': {"message": 'Please give me data'}})
        old_user = Users.objects.filter(username=username)
        if old_user:
            return JsonResponse({'code': 400, 'error': {"message": 'The username is existed'}})
        m = hashlib.md5()
        m.update(password.encode())
        b64_password = m.hexdigest()
        with transaction.atomic():
            Users.objects.create(username=username, password=b64_password, phone=phone, email=email)
            wbuser = WeiboUsers.objects.get(wbuid=wbid)
            wbuser.uid_id = Users.objects.get(username=username).id
            wbuser.save()
        # 邮箱激活
        int_random = random.randint(1000, 9999)
        code_str = username + "_" + str(int_random)
        code_str_bs = base64.urlsafe_b64encode(code_str.encode()).decode()
        r.set("email_active_%s" % (username), code_str)
        active_url = 'http://127.0.0.1:7000/dadashop/templates/active.html?code=%s' % (code_str_bs)
        send_active_email.delay(email, active_url)
        return JsonResponse({'code': 200, "username": username, 'data': {'token': make_token(username)}})


def get_access_token(code):
    import requests
    token_url = 'https://api.weibo.com/oauth2/access_token'
    post_data = {
        'client_id': settings.WEIBO_CLIEND_ID,
        'client_secret': settings.WEIBO_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'redirect_uri': settings.WEIBO_REDIRECT_URL,
        'code': code
    }
    try:
        res = requests.post(token_url, data=post_data)
    except Exception as e:
        raise
    if res.status_code == 200:
        return json.loads(res.text)
    raise
