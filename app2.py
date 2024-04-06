from flask import Flask, request, render_template, jsonify
import hmac
import hashlib

app = Flask(__name__)

# 存储PR信息的列表，用于保存接收到的Pull Request数据
pr_data = []

# 定义应用的根目录路由，返回主页
@app.route('/')
def home():
    # 使用Flask的render_template函数返回HTML页面
    return render_template('index.html')

# 定义处理GitHub Webhooks的路由，仅接受POST请求
@app.route('/webhook', methods=['POST'])
def handle_github_webhook():
    # GitHub设置中定义的密钥，用于验证Webhook请求的真实性
    secret_token = b'"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"'
    # 使用HMAC算法和SHA1哈希函数生成请求数据的签名
    signature = 'sha1=' + hmac.new(secret_token, request.data, hashlib.sha1).hexdigest()
    
    # 比较计算出的签名与请求中的签名是否一致，不一致则认为请求不可信
    if not hmac.compare_digest(signature, request.headers.get('X-Hub-Signature', '')):
        return jsonify({'message': 'Invalid signature'}), 403

    # 获取GitHub发送的事件类型
    event = request.headers.get('X-GitHub-Event', '')
    # 如果事件类型是Pull Request相关
    if event == 'pull_request':
        payload = request.json  # 解析请求体中的JSON数据
        action = payload.get('action')  # 获取Pull Request的具体操作类型
        
        # 如果Pull Request操作是关闭操作
        if action == 'closed':
            pr_number = payload.get('number')  # 获取Pull Request编号
            pr_title = payload.get('pull_request', {}).get('title')  # 获取标题
            pr_author = payload.get('pull_request', {}).get('user', {}).get('login')  # 获取作者用户名
            is_merged = payload.get('pull_request', {}).get('merged', False)  # 检查PR是否被合并

            # 将PR信息添加到全局列表中
            pr_data.append({
                'number': pr_number,
                'title': pr_title,
                'author': pr_author,
                'is_merged': is_merged
            })
            
    # 返回响应确认已接收处理请求
    return jsonify({'message': 'Received'}), 200

# 新增路由，用于前端获取保存的Pull Request数据
@app.route('/pr_data', methods=['GET'])
def get_pr_data():
    # 将存储的PR信息以JSON格式返回
    return jsonify(pr_data)

# 主程序入口，运行Flask应用
if __name__ == '__main__':
    app.run(debug=True)
