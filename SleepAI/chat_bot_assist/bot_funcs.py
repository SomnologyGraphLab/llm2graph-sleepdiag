import gradio as gr
import time
import uuid
import requests
BACKEND_URL = "http://localhost:8000/chat_bot"
database_password = "G6669963."
def respond(
        prompt: str,
        history,
):
    if not history:
        history = [{"role": "system", "content": "You are a friendly chatbot"}]
    history.append({"role": "user", "content": prompt})

    yield history + [{"role": "assistant", "content": "Waiting for response..."}]

    response_front = {"role": "assistant", "content": ""}
    session_id = str(uuid.uuid4())
    # 构建请求数据
    
    payload = {
        "uri": "bolt://localhost:7687",  # 示例值，根据实际需求修改
        "database": "neo4j",    # 数据库的信息在sleepkg
        "userName": "neo4j",
        "password": database_password,
        "question": prompt+"回答的内容要丰富专业",
        "session_id": session_id,  # 示例值，可以动态生成
        "model": "OpenAI GPT 4o",    # 示例值，按需调整
        "mode": "graph+vector",      # 示例值
        "document_names": "[]"     # 如果有文档名字，可传数组或 None
    }
    # 调用后端 API
    try:
        response = requests.post(
            BACKEND_URL,
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=100 # 设置超时时间
        )
        response.raise_for_status()  # 检查响应状态是否为成功
        backend_data = response.json()  # 假设后端返回的是 JSON 数据
        # print(backend_data)
        # assistant_response = backend_data["data"]["message"] 
        # sources = "\n\n"
        # 提取 message 和 sources
        assistant_response = backend_data["data"]["message"] 
        sources = "\n\n**Sources:**\n" + "\n".join(backend_data["data"]["info"]["sources"])

        # 合并消息和 sources
        final_response = assistant_response + sources
        assistant_response = final_response
      


    except requests.RequestException as e:
        assistant_response = f"Error communicating with backend: {str(e)}"


    # print(assistant_response)

    # print(response_front)
    
    # Simulate streaming response
    for char in assistant_response:
        response_front["content"] += char
        time.sleep(0.02)
        yield history + [response_front]

def handle_undo(history, undo_data: gr.UndoData):
    return history[:undo_data.index], history[undo_data.index]['content']
def handle_retry(history, retry_data: gr.RetryData):
    new_history = history[:retry_data.index]
    previous_prompt = history[retry_data.index]['content']
    yield from respond(previous_prompt, new_history)
def handle_like(data: gr.LikeData):
    if data.liked:
        print("You upvoted this response: ", data.value)
    else:
        print("You downvoted this response: ", data.value)