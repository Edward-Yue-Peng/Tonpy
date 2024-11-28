class Database:
    def __init__(self):
        self.user_name = None
        self.user_list = ["qwen", "AIBot"]
        self.selected_user = None
        self.chat_history = {}
        # 这里直接和王兆南那个state machine结合一下
        # 1. offline：没有用户名，还在第一个页面
        # 2. login：已经登录，有用户名，在选择用户聊天中
        # 3. chatting：在与人激情对线中
        self.state = "offline"
#TODO 与后端结合