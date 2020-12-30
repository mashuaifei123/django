import time
import requests
import json


class WeChat:
    def __init__(self):
        self.CORPID = 'ww31f12b15e58c1b05'  #企业ID，在管理后台获取
        self.CORPSECRET = 'H5slR0jzWlhtxkGmSt1o5AF0mKpTJoixDaVPwvJ1W2s'#自建应用的Secret，每个自建应用里都有单独的secret
        self.AGENTID = '1000058'  #应用ID，在后台应用中获取
        # self.TOUSER = "17610|39262"  # 接收者用户名,多个用户用|分割

    def _get_access_token(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {'corpid': self.CORPID,
                  'corpsecret': self.CORPSECRET,
                  }
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        return data["access_token"]

    def get_access_token(self):
        try:
            with open('access_token.conf', 'r') as f:
                t, access_token = f.read().split()
        except:
            with open('access_token.conf', 'w') as f:
                access_token = self._get_access_token()
                cur_time = time.time()
                f.write('\t'.join([str(cur_time), access_token]))
                return access_token
        else:
            cur_time = time.time()
            if 0 < cur_time - float(t) < 7260:
                return access_token
            else:
                with open('access_token.conf', 'w') as f:
                    access_token = self._get_access_token()
                    f.write('\t'.join([str(cur_time), access_token]))
                    return access_token

    def send_data(self, touser, info, intoname, ds, techname, address, data_w, time_w, sendtime):
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token()
        '''
        send_values = {
            "touser": self.TOUSER,
            "msgtype": "text",
            "agentid": self.AGENTID,
            "text": {
                "content": message
                },
            "safe": "0"
            }
        '''
        send_values = {
                   "touser" : touser,
                   "msgtype": "markdown",
                   "agentid" : self.AGENTID,
                   "markdown": {
                        "content": '`{}` \n\
                                >**培训详情** \n\
                                >主　题：<font color=\"info\">{}</font> \n\
                                >描　述：{} \n\
                                >组织者：{} \n\
                                >会议室：<font color=\"info\">{}</font> \n\
                                >日　期：<font color=\"warning\">{}</font> \n\
                                >时　间：<font color=\"comment\">{}</font> \n\
                                > \n\
                                >消息时间:{} \n\
                                >请准时参加会议。'.format(info, intoname, ds, techname, address, data_w, time_w, sendtime)
                   },
                   "enable_duplicate_check": 0,
                   "duplicate_check_interval": 1800
                }
        send_msges=(bytes(json.dumps(send_values), 'utf-8'))
        respone = requests.post(send_url, send_msges)
        respone = respone.json()   #当返回的数据是json串的时候直接用.json即可将respone转换成字典
        return respone["errmsg"]


if __name__ == "__main__":
    touser = "17610|20877" 
    intoname = '信息管理SOP培训标题'
    info = '您有新的培训邀请'
    ds = ''
    techname = '培训老师名称丁老师'
    address = '1126'
    data_w = '2020年5月18日'
    time_w = '上午9:00-11:00'
    wx = WeChat()
    wx.send_data(touser, info, intoname, ds, techname, address, data_w, time_w, sendtime)
    pass