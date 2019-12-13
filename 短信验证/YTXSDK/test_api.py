from CCPRestSDK import REST
import configparser

# 主账号
accountSid = xxxxx

# 主账号Token
accountToken = xxxxx

# 应用Id
appId = xxxx

# 请求地址，格式如下，不需要http://
serverIP = 'app.cloopen.com'

# 端口
serverPort = '8883'

# REST版本号
softVersion = '2013-12-26'

# 流程
# 荣联云
# 注册
# 创建应用
# ACCOUNT SID
# appid
# AUTH TOKEN

# 参数
# 发送短信
# @param to 手机号
# @param datas 数据内容  格式为数组如{'12','34'} 不需要用''替换
# @param $tempId 模板Id

def send_template_SMS(to, datas, tempId):
    # 初始化REST SDK
    rest = REST(serverIP, serverPort, softVersion)
    rest.setAccount(accountSid, accountToken)
    rest.setAppId(appId)

    return rest.sendTemplateSMS(to, datas, tempId)


if __name__ == '__main__':
    # 手机号  {验证码  3分钟内有效}
    send_template_SMS(17316184506, {"1234", 3}, 1)
