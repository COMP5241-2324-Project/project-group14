from flask import Flask, request, render_template, jsonify
import hmac
import hashlib

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def handle_github_webhook():
    # 验证Webhook安全性的密钥，假设你在GitHub Webhook设置中定义了一个秘密
    secret_token = b'"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"'
    signature = 'sha1=' + hmac.new(secret_token, request.data, hashlib.sha1).hexdigest()
    
    # 确认请求的签名是否匹配
    if not hmac.compare_digest(signature, request.headers.get('X-Hub-Signature', '')):
        return jsonify({'message': 'Invalid signature'}), 403
        
    # 从GitHub请求头中获取事件类型
    event = request.headers.get('X-GitHub-Event', '')
    
    if event == 'pull_request':
        payload = request.json
        action = payload.get('action')
        
        # 检查Pull Request操作类型
        if action == 'closed':
            pr_number = payload.get('number')
            pr_title = payload.get('pull_request', {}).get('title')
            pr_author = payload.get('pull_request', {}).get('user', {}).get('login')
            # 检查Pull Request是否被合并
            is_merged = payload.get('pull_request', {}).get('merged', False)
            
            if is_merged:
                print(f"Pull Request #{pr_number} titled '{pr_title}' by {pr_author} was merged.")
            else:
                print(f"Pull Request #{pr_number} titled '{pr_title}' by {pr_author} was closed without merging.")
   
        

    return jsonify({'message': 'Received'}), 200
    
if __name__ == '__main__':
    app.run(debug=True)
