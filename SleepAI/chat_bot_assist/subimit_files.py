import os
# 提交文件的处理函数
def submit_files(files, dissatisfy):
    if not files:
        return "❌ 未上传任何文件！请先上传文件后再提交。"

    # 设置保存文件的目录
    save_dir = "./uploaded_files"  # 修改为您希望保存文件的目录
    os.makedirs(save_dir, exist_ok=True)  # 如果目录不存在则创建

    responses = []

    for filepath in files:
        try:
            # 获取文件的文件名
            filename = os.path.basename(filepath)
            if dissatisfy:
                filename = f"More_Important_{filename}"
            save_path = os.path.join(save_dir, filename)

            

            # 将文件复制到本地目录
            with open(filepath, "rb") as file:
                with open(save_path, "wb") as out_file:
                    out_file.write(file.read())

            responses.append(f"✅ 文件 `{filename}` 已成功上传，待管理员审核后即可更新知识库！")
        except Exception as e:
            responses.append(f"❌ 文件 `{filepath}` 文件上传失败，错误信息: {str(e)}")

    return "\n".join(responses)