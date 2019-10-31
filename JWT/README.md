## 前提概要

### **base64**

**功能**: 二进制可视化.

原理:

1. 将字符串拆成每三个字符一组
2. 计算每一个字符对应的ASCII码二进制
3. 将8位的二进制码，按照每6位一组重新分组(不足6位的在后面补0)
4. 计算对应的十进制编码
5. 按照base64表，查看对应的字符(不足4位的在后面补=)

方法:

- b64encode()/b64decode()
- urlsafe_b64encode()/urlsafe_b64decode() #  功能同上  *进行url的字符串编码*    +'替换成 '-',将'/'替换成'_'  



### SHA-256

功能: 安全**散列**算法的一种（hash）

```python
s = hashlib.sha256()
s.update(b'xxxx')
s.digest()
```

- update() 在之前运算基础上累加计算

  

### **hmac**

功能**: 使用**散列**算法同时结合一个加密**密钥**

```python
h = hmac.new(key, str, digestmod='SHA256 ')
h.digest() 
```



#### RSA256 非对称加密
```
..
```

## JWT 组成

1.  ```python
   #header
   {'alg':'HS256','typ':'JWT'}
   ```

2. ```python
   #payload
   {
       'exp': xxx, # Expiration Time 此token的过期时间的时间戳
       'iss': xxx，# (Issuer) Claim 指明此token的签发者
       'aud': xxx, #(Audience) Claim 指明此token的
       'iat': xxx, # (Issued At) Claim 指明此创建时间的时间戳
       'aud': xxx, # (Audience) Claim 指明此token签发面向群体
       ...
       'uid': 1
   }
   ```

3. signature 签名 **HS256(自定义的key , base64后的header + '.' +base64后的payload)**

4. jwt结果    **base64(header) + '.' + base64(payload) + '.' + base64(sign)**



## JWT效验

1. 解析header, 确认alg
2. 重复JWT组成步骤3  比对signature 判断是否被篡改
3. 获取payload自定义内容



## 测试地址: 

​	**https://jwt.io/**