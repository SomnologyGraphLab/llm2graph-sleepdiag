import gradio as gr

# 登录验证函数
def verify_login(username, password):
    if username == "admin" and password == "123456":
        jump_html = """
        <meta http-equiv="refresh" content="1;url=http://localhost:5173">
        <h3 style='color: green;'>✅ 登录成功！正在跳转中...</h3>
        """
        return gr.HTML(jump_html), ""
    else:
        return gr.HTML(""), "<span style='color:red;'>❌ 用户名或密码错误</span>"


