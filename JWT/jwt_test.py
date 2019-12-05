import json, base64, time, copy, hmac


class MyJWT(object):

    @staticmethod
    def encode(key='', payload=None, exp=200):
        # header
        dict_header = {'typ': 'JWT', 'alg': 'SHA256'}
        str_header = json.dumps(dict_header, separators=(',', ':'), sort_keys=True)
        b64_header = MyJWT.base64_encode(str_header)
        # payload
        dict_payload = copy.deepcopy(payload)
        dict_payload['exp'] = str(time.time() + exp)
        str_payload = json.dumps(dict_payload, separators=(',', ':'), sort_keys=True)
        b64_payload = MyJWT.base64_encode(str_payload)
        # sign
        if isinstance(key, str):
            b_key = key.encode()
        str_signature = b64_header + '.' + b64_payload
        h_signature = hmac.new(b_key, str_signature.encode(), digestmod=dict_header['alg'])
        base_signature = h_signature.hexdigest()
        return b64_header + '.' + b64_payload + '.' + base_signature


    @staticmethod
    def base64_encode(str_1):
        return  base64.urlsafe_b64encode(str_1.encode()).decode().replace('=', '')

    @staticmethod
    def decode(key='123', token=''):
        str_header, str_payload, str_signature = token.split('.')
        dict_header = json.loads(MyJWT.base64_decode(str_header))
        header_payload = str_header + '.' + str_payload
        h_signature = hmac.new(key.encode(), header_payload.encode(), digestmod=dict_header['alg'])
        base_signature = h_signature.hexdigest()
        if base_signature != str_signature:
            return '内容被篡改'
        dict_payload = json.loads(MyJWT.base64_decode(str_payload))
        if int(float(dict_payload['exp'])) < int(time.time()):
            return 'token超时'
        del dict_payload['exp']
        return dict_payload

    @staticmethod
    def base64_decode(str_1):
        str_1 += '=' * (4 - len(str_1) % 4)
        return base64.urlsafe_b64decode(str_1.encode()).decode()

    # ------------------------

    @staticmethod
    def b64decode(b_s):
        # 补全签发时 替换掉的 等号
        b_s += '=' * (4 - len(b_s) % 4)
        return base64.urlsafe_b64decode(b_s)

    @staticmethod
    def decode(str_jwt, str_key):
        # 校验token
        # 1， 检查签名 【前两项bs 再做一次hmac签名，与第三部分进行比较，若两者相等，校验成功;失败 raise】
        # 2，检查时间戳是否过期 [过期则raise]
        # 3，return payload明文 即payload字典对象
        str_header, str_payload, str_sign = str_jwt.split('.')
        if isinstance(str_key, str):
            b_key = str_key.encode()
        hm = hmac.new(b_key, str_header.encode() + b'.' + str_payload.encode(), digestmod='SHA256')
        bs_new_sign = Jwt.b64encode(hm.digest()).decode()
        if bs_new_sign != str_sign:
            raise ('被篡改')
        # 检查payload中的时间
        json_payload = Jwt.b64decode(str_payload)
        # json字符串 ->  python对象
        payload = json.loads(json_payload)
        exp = payload['exp']
        if time.time() > exp:
            raise ('过期')
        return payload


if __name__ == '__main__':
    str_key = '123qwe'
    str_token = MyJWT.encode(payload={'username': 'wwn', 'age': 16}, key=str_key, exp=100)
    print(str_token)
    # res_payload = Jwt.decode(str_jwt=str_token, str_key=str_key)
    # print(res_payload)
