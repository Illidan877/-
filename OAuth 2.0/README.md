## OAuth2.0

### 定义

- OAuth 的核心就是向第三方应用颁发令牌
- OAuth 引入了一个授权层，用来分离两种不同的角色：客户端和资源所有者。......资源所有者同意以后，资源服务器可以向客户端颁发令牌。客户端通过令牌，去请求数据。

### 四种获得令牌的流程

- 授权码（authorization-code）(常用)
- 隐藏式（implicit）
- 密码式（password）
- 客户端凭证（client credentials）



### 开发者平台注册

 备案  以微博为例

1. 微链接 -->移动应用 -- > 立即接入 -- >应用分类 -> 选择网页应用
2. 应用信息
   1. 基本信息   存 App Key ,App Secret
   2. 高级信息  配置授权回调页面

### 授权(授权码模式)

1. 前端点击授权按钮发起请求

2. 拼接授权url  返回给前端, 前端跳转至授权界面.

   ```python
       params = {
           "response_type": 'code', #授权模式
           'client_id': settings.WEIBO_CLIEND_ID,	# App Key
           'redirect_uri': settings.WEIBO_REDIRECT_URL, #回调路由
           'scope': '', #获取权限  默认全开
       }
       url = "https://api.weibo.com/oauth2/authorize?" + urlencode(params)
   ```

3. 如果用户同意授权

   1. 第三方平台会跳转至 备案2.2中配置的回调页面url
   2. url中会拼接code授权码
   3. 前端将code发给后台

4. 后台向第三方平法发post请求,用code换token

   1. token返回内容

      ```python
      {
          'access_token': 'xxxxxxxxxxxxxxx',  #周旋了半天拿的就是它
          'remind_in': '157679999', 				
          'expires_in': 157679999, 					 # 有效期
          'uid': '5865720694', 							   # 第三方中的用户id 即微博用户id 微信用户id 
          'isRealName': 'true'							  
      }
      
      ```

   ```python
   #发送请求 获取token
   def get_access_token(code):
       import requests
       token_url = 'https://api.weibo.com/oauth2/access_token'
       post_data = {
           'client_id': settings.WEIBO_CLIEND_ID, # App Key
           'client_secret': settings.WEIBO_CLIENT_SECRET, # App Secret
           'grant_type': 'authorization_code',  #授权类型  授权码模式
           'redirect_uri': settings.WEIBO_REDIRECT_URL,  # 回调url
           'code': code	# 授权码
       }
       try:
           res = requests.post(token_url, data=post_data)
       except Exception as e:
           raise
       if res.status_code == 200:  # 如果为200 返回token 
           return json.loads(res.text)
       raise
   ```

5. 得到token之后,等待用户绑定信息 

   - 查这个第三方(微博)之前是否登录过
     - 没登录 立刻存表  等待用户注册  绑定账号 (不能发给前端   以免被截获)
     - 登录过  查是否绑定
       - 绑定了 直接登录签发token
       - 没绑定 重定向到注册     
         - 创建用户  绑定第三方id   (注意事务  绑定失败重新注册)

### 隐藏式（implicit）

```python
#todo
```

### 密码式（password）

```python
#todo
```

### 客户端凭证（client credentials）

```python
#todo
```