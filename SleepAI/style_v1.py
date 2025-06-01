self_css = """/* 全局背景和字体设置 */
/* 全局背景和字体设置 */
.gradio-container {
    background-color: #f9f9f9;  /* 背景颜色（温和的灰白色） */
    font-family: 'Arial', sans-serif;  /* 设置字体 */
    color: #444444;  /* 设置文本颜色 */
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 轻微的阴影效果 */
}

/* 设置标题样式 */
h1, h2, h3, h4, h5, h6 {
    color: #3b9d9d;  /* 标题颜色（柔和的蓝绿色） */
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;  /* 设置标题字体 */
    font-weight: 600; /* 设置稍微加粗的字体样式 */
}

/* Gradio Markdown 样式 */
.gradio-markdown {
    font-size: 16px;  /* 调整文本大小 */
    color: #666666;  /* 温和的灰色文字颜色 */
}

/* 设置按钮样式 
button {
    background-color: #66b2b2;  /* 按钮背景颜色（清新的淡蓝绿色） */
    color: white;  /* 按钮文字颜色 */
    font-size: 15px;  /* 按钮文字大小 */
    border: none;  /* 去掉按钮边框 */
    border-radius: 12px;  /* 更大的圆角 */
    padding: 12px 25px;  /* 设置内边距 */
    cursor: pointer;  /* 设置鼠标样式 */
    transition: background-color 0.3s ease, transform 0.2s ease;  /* 鼠标悬停时改变背景颜色并添加点击动画 */
}
*/
/* 针对特定按钮的样式 */
#example {
    background-color: #66b2b2;  /* 按钮背景颜色（清新的淡蓝绿色） */
    color: white;  /* 按钮文字颜色 */
    font-size: 15px;  /* 按钮文字大小 */
    padding: 12px 25px;  /* 设置内边距 */
    border-radius: 12px;  /* 更大的圆角 */
    border: none;  /* 去掉边框 */
    cursor: pointer;  /* 设置鼠标样式 */
    transition: background-color 0.3s ease, transform 0.2s ease;  /* 鼠标悬停时改变背景颜色并添加点击动画 */
}

#example:hover {
    background-color: #4d9f9f;  /* 悬停时的背景颜色 */
    transform: translateY(-2px);  /* 鼠标悬停时按钮微微上升 */
}

#example:active {
    transform: translateY(1px);  /* 点击时按钮轻微下沉 */
}
button:hover {
    background-color: #4d9f9f;  /* 按钮悬停时的背景颜色 */
    transform: translateY(-2px);  /* 鼠标悬停时按钮微微上升 */
}

button:active {
    transform: translateY(1px);  /* 点击时按钮轻微下沉 */
}

/* 设置文本框样式 */
input[type="text"], textarea {
    padding: 12px;
    font-size: 14px;
    border-radius: 8px;
    border: 1px solid #e0e0e0;  /* 较浅的边框颜色 */
    width: 100%;  /* 占满全宽 */
    box-sizing: border-box;
    transition: border-color 0.3s ease; /* 聚焦时平滑变色 */
}

/* 调整输入框的焦点样式 */
input[type="text"]:focus, textarea:focus {
    outline: none;
    border-color: #66b2b2;  /* 焦点框颜色（与按钮相同的颜色，增强统一性） */
}

/* 更好的排版布局 */
.gradio-column {
    margin-bottom: 25px;  /* 适当增加列之间的间隔 */
}

.gradio-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 25px;
}

/* 提交按钮样式 */
button[type="submit"] {
    background-color: #5cb85c;  /* 提交按钮绿色（温暖活力） */
    color: white;
    padding: 12px 30px;
    border-radius: 12px;
}

button[type="submit"]:hover {
    background-color: #4cae4c;  /* 提交按钮悬停颜色 */
}
"""