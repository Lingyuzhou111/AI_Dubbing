# encoding:utf-8
import json
import requests
import plugins
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from common.log import logger
from plugins import *

@plugins.register(
    name="AI_Dubbing",
    desire_priority=100,
    desc="根据角色名和内容生成AI配音音频文件",
    version="1.0",
    author="Lingyuzhou",
)
class AIDubbing(Plugin):
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        logger.info("[AI_Dubbing] inited.")

        # 可用角色列表
        self.available_roles = [
            "AD学姐", "赛马娘", "奶龙", "蔡徐坤", "御姐茉莉", "懒羊羊", "喜羊羊",
            "齐司礼", "陆沉", "查理苏", "萧逸", "夏鸣星", "秦彻", "孙悟空",
            "熊二", "熊大", "海绵宝宝", "派大星", "蜡笔小新", "麦克阿瑟",
            "霸总", "青春男声", "东北男声", "文艺学姐", "青叔", "李白",
            "韩信", "妲己", "狄仁杰", "诸葛亮", "瑶", "公孙离", "伽罗",
            "亚连", "貂蝉", "朵莉亚", "武则天", "后羿", "孙策", "周瑜",
            "东方月初-大司命", "央视配音", "邓紫棋", "丁真", "光头强",
            "五条悟", "工藤新一", "毛利兰", "萧炎", "王者语音播报",
            "柯南", "磊哥游戏", "那英", "赤井秀一", "叶修", "李泽言",
            "秦彻", "姬小满", "两面宿傩(中)", "哆啦a梦", "小夫", "猪猪侠",
            "李佳琦", "K总", "狂魔哥"
        ]

    def on_handle_context(self, e_context: EventContext):
        content = e_context["context"].content  # 获取事件上下文中的消息内容

        # 检查消息内容是否以 "配音:" 开头
        if content.startswith("配音:"):
            # 分割消息内容，提取角色名和要合成的内容
            try:
                _, name_msg = content.split(":", 1)
                name, msg = map(str.strip, name_msg.split("+", 1))
            except ValueError:
                reply = Reply()
                reply.type = ReplyType.TEXT
                reply.content = "请按照格式输入: 配音: 角色名+内容"
                e_context["reply"] = reply
                e_context.action = EventAction.BREAK_PASS
                return

            # 调用 API 生成配音
            url = "https://www.hhlqilongzhu.cn/api/yuyin_All.php"
            params = {
                'name': name,
                'msg': msg
            }

            try:
                response = requests.post(url, data=params)
                if response.status_code == 200:
                    result = response.json()
                    if result['code'] == 200:
                        reply = Reply()
                        reply.type = ReplyType.TEXT
                        reply.content = f"合成成功！\n角色名: {result['name']}\n内容: {result['content']}\n音频链接: {result['url']}"
                    else:
                        reply = Reply()
                        reply.type = ReplyType.TEXT
                        reply.content = f"错误: {result['msg']}"
                else:
                    reply = Reply()
                    reply.type = ReplyType.TEXT
                    reply.content = f"请求失败，状态码: {response.status_code}"
            except Exception as e:
                reply = Reply()
                reply.type = ReplyType.TEXT
                reply.content = f"发生错误: {str(e)}"

            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS  # 事件结束，并跳过处理context的默认逻辑

    def get_help_text(self, **kwargs):
        roles = ", ".join(self.available_roles)
        help_text = f"""AI配音合成
***指令：输入【配音: 角色名称+语音内容】来生成对应的AI合成音频。
***例如：配音: 工藤新一+你好,我是工藤新一,是一名高中生侦探。
***可用角色: {roles}"""
        return help_text
