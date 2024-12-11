## Chat Program 数据传输格式开发文档

### 数据传输格式
所有数据通过 JSON 格式传输，包含以下基本字段：
- **action**: 指明当前动作。
- **其他字段**: 根据具体的 action 定义。

#### 常见的数据格式

1. **登录请求**
   - **客户端发送**：
     ```json
     {
         "action": "login",
         "name": "<用户名>"
     }
     ```
   - **服务端响应**：
     - 登录成功：
       ```json
       {
           "action": "login",
           "status": "ok"
       }
       ```
     - 用户名重复：
       ```json
       {
           "action": "login",
           "status": "duplicate"
       }
       ```

2. **连接请求**
   - **客户端发送**：
     ```json
     {
         "action": "connect",
         "target": "<目标用户名>"
     }
     ```
   - **服务端响应**：
     - 连接成功：
       ```json
       {
           "action": "connect",
           "status": "success"
       }
       ```
     - 用户忙碌：
       ```json
       {
           "action": "connect",
           "status": "busy"
       }
       ```
     - 用户名不存在：
       ```json
       {
           "action": "connect",
           "status": "no-user"
       }
       ```
     - 自己连接自己：
       ```json
       {
           "action": "connect",
           "status": "self"
       }
       ```

3. **断开连接请求**
   - **客户端发送**：
     ```json
     {
         "action": "disconnect"
     }
     ```
   - **服务端响应**：
     ```json
     {
         "action": "disconnect"
     }
     ```

4. **消息交换**
   - **客户端发送**：
     ```json
     {
         "action": "exchange",
         "from": "<发送者用户名>",
         "message": "<消息内容>"
     }
     ```
   - **服务端转发**：
     ```json
     {
         "action": "exchange",
         "from": "<发送者用户名>",
         "message": "<消息内容>"
     }
     ```

5. **获取在线用户列表**
   - **客户端发送**：
     ```json
     {
         "action": "list"
     }
     ```
   - **服务端响应**：
     ```json
     {
         "action": "list",
         "results": "<在线用户列表>"
     }
     ```

6. **获取时间**
   - **客户端发送**：
     ```json
     {
         "action": "time"
     }
     ```
   - **服务端响应**：
     ```json
     {
         "action": "time",
         "results": "<当前时间>"
     }
     ```

7. **搜索历史消息**
   - **客户端发送**：
     ```json
     {
         "action": "search",
         "target": "<搜索关键词>"
     }
     ```
   - **服务端响应**：
     ```json
     {
         "action": "search",
         "results": "<搜索结果>"
     }
     ```

8. **请求诗句**
   - **客户端发送**：
     ```json
     {
         "action": "poem",
         "target": <诗句编号>
     }
     ```
   - **服务端响应**：
     ```json
     {
         "action": "poem",
         "results": "<诗句内容>"
     }
     ```

9. **游戏邀请**
   - **客户端发送**：
     ```json
     {
         "action": "game_invite",
         "game": "<游戏名称>"
     }
     ```
   - **服务端转发**：
     ```json
     {
         "action": "game_invite",
         "game": "<游戏名称>",
         "from": "<发送者用户名>"
     }
     ```

10. **游戏邀请响应**
    - **客户端发送**：
      ```json
      {
          "action": "game_response",
          "game": "<游戏名称>",
          "response": "y/n",
          "invitation_from": "<邀请者用户名>"
      }
      ```
    - **服务端转发**：
      ```json
      {
          "action": "game_response",
          "game": "<游戏名称>",
          "response": "y/n",
          "from": "<发送者用户名>"
      }
      ```

### 状态与行为

#### 状态列表
- **S_OFFLINE**: 离线状态。
- **S_LOGGEDIN**: 登录状态。
- **S_CHATTING**: 聊天状态。
- **S_GAME_INVITING**: 游戏邀请发送状态。
- **S_GAME_DECIDING**: 游戏邀请决定状态。
- **S_GAMING**: 游戏进行状态。

#### 状态行为
1. **S_OFFLINE**
   - **接收消息**：无。
   - **发送消息**：登录。

2. **S_LOGGEDIN**
   - **接收消息**：
     - 收到连接请求，切换到 S_CHATTING。
     - 收到消息或指令，执行对应操作（获取时间、获取用户列表、搜索、请求诗句）。

3. **S_CHATTING**
   - **接收消息**：
     - 收到对方消息，显示。
     - 收到游戏邀请，切换到 S_GAME_DECIDING。
   - **发送消息**：
     - 普通聊天消息。
     - 游戏邀请，切换到 S_GAME_INVITING。

4. **S_GAME_INVITING**
   - **接收消息**：
     - 游戏邀请被接受，切换到 S_GAMING。
     - 游戏邀请被拒绝，返回 S_CHATTING。

5. **S_GAME_DECIDING**
   - **接收消息**：无。
   - **发送消息**：
     - 接受游戏邀请，切换到 S_GAMING。
     - 拒绝游戏邀请，返回 S_CHATTING。

6. **S_GAMING**
   - **接收消息**：根据游戏逻辑处理。
   - **发送消息**：根据游戏逻辑处理。

本文档适用于开发与调试使用，请确保传输内容严格符合定义的格式与状态机逻辑。

