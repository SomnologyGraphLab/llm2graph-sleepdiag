import gradio as gr

# 弹窗显示和关闭逻辑
def toggle_popup(state):
    # 如果状态是关闭，打开弹窗
    if state == "closed":
        state = "open"
        popup_html = """
        <div id="popup" style="
            position: fixed; 
            top: 50%; 
            left: 50%; 
            transform: translate(-50%, -50%);
            width: 400px; 
            background-color: #28a745; 
            color: white; 
            padding: 20px; 
            border: 1px solid black; 
            border-radius: 5px; 
            box-shadow: 0 0 10px rgba(0,0,0,0.5); 
            z-index: 1000; 
            text-align: center;">
            <p>这是一个绿色背景的弹窗！</p>
            <img src="https://www.hit.edu.cn/_upload/site/00/ee/238/logo.png" alt="弹窗图片" style="max-width: 100%; height: auto; border-radius: 5px;" />
            <br>
            <button onclick="document.getElementById('popup').style.display='none';document.getElementById('popup-overlay').style.display='none';" 
                style="margin-top: 10px; 
                       padding: 5px 10px; 
                       background-color: #007BFF; 
                       color: white; 
                       border: none; 
                       border-radius: 3px; 
                       cursor: pointer;">关闭</button>
        </div>
        <div id="popup-overlay" style="
            position: fixed; 
            top: 0; 
            left: 0; 
            width: 100%; 
            height: 100%; 
            background-color: rgba(0,0,0,0.5); 
            z-index: 999;" 
            onclick="document.getElementById('popup').style.display='none';document.getElementById('popup-overlay').style.display='none';">
        </div>
        """
    # 如果状态是打开，关闭弹窗
    elif state == "open":
        state = "closed"
        popup_html = ""  # 清空 HTML 内容，隐藏弹窗

    return popup_html, state

with gr.Blocks() as demo:
    gr.Markdown("点击下面的按钮弹出绿色背景窗口：")
    button = gr.Button("弹出/关闭窗口")
    popup_output = gr.HTML()  # 用于显示弹窗
    state = gr.State("closed")  # 初始状态为关闭

    # 点击按钮时更新 HTML 内容并触发弹窗
    button.click(toggle_popup, inputs=state, outputs=[popup_output, state])

demo.launch()
