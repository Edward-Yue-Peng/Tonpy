# Tonpy

目前只有客户端部分，后端啥都没有

## 项目结构

- `main.py`: 应用程序的入口点，包含主要的路由逻辑和页面设置
- `login.py`: 处理用户登录
- `user_list.py`: 显示用户列表
- `chat_page.py`: 聊天页面
- `chat_control.py`: 这里应该是各种聊天的实现，但是目前只有一个与AI聊
- `data_control.py`: 数据管理类，用于存储和管理应用状态，还有疯狂传参
- `assets/`: 放各种性感小图标

## 主要功能和方法

### main.py

- `main(page: ft.Page)`: 主函数，设置页面标题和路由
- `route_change(route)`: 处理路由变化，加载相应的视图
- `view_pop(view)`: 处理视图返回

### login.py

- `login_view(page: ft.Page, data: Database)`: 创建登录视图
- `login_click(e)`: 登录按钮点击事件

### user_list.py

- `user_list_view(page: ft.Page, data: Database)`: 创建用户列表视图
- `on_select_user(user)`: 选择和谁聊事件
- `on_logout(e)`: 注销事件

### chat_page.py

- `chat_page_view(page: ft.Page, data: Database)`: 创建聊天页面视图
- `send_message_click(e)`: 处理消息发送事件
- `on_message(message: Message)`: 处理接收到的消息

### chat_control.py

- `chat_with_individual(input_prompt)`: 与 AI 进行对话的方法

### data_control.py

- `Database`: 管理应用状态的类，包括用户信息、聊天记录等

## 使用说明

1. 装一下`flet`和`openai`
2. 运行 `main.py`启动应用
3. 登录后可以选择用户进行聊天
4. 在聊天界面可以发送消息，与 AI 或其他用户交互
