import time
import uuid
import requests
BACKEND_URL = "http://localhost:8000/chat_bot"
database_password = "G6669963."
def processjson2response(scale_name, json_details):
    session_id = str(uuid.uuid4())
    prompt = "患者前来医院就诊睡眠障碍的相关问题，你需要作为一个医生来对他做出初步的诊断、提供接下来要做的检查和提出相应的治疗建议" + \
            "该患者现在填写了" + str(scale_name) + \
            "其填写的详细数据如接下来的json格式所示" + \
            str(json_details) + \
            "请你给出初步的诊断、提供接下来患者要做的检查并提出相应的治疗建议"+\
            "术语要专业、丰富"
    # 构建请求数据
    payload = {
        "uri": "bolt://localhost:7687",  # 示例值，根据实际需求修改
        "database": "neo4j",    # 数据库的信息在sleepkg
        "userName": "neo4j",
        "password": database_password,
        "question": prompt,
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
        print(backend_data)
        assistant_response = backend_data["data"]["message"]
        # sources = "\n\nSources:\n" + "\n".join(backend_data["data"]["info"]["sources"])

        # # 合并消息和 sources
        # final_response = assistant_response + sources
        # assistant_response = final_response
        


    except requests.RequestException as e:
        assistant_response = f"Error communicating with backend: {str(e)}"
    return assistant_response

def submit_form(*inputs):
    # 根据每个问题的标签构建字典
    form_data = {
        "姓名": inputs[0],  # 姓名
        "性别": inputs[1],  # 性别
        "年龄": inputs[2],  # 年龄
        "文化程度": inputs[3],  # 文化程度
        "职业": inputs[4],  # 职业
        "评定日期": inputs[5],
        "第几次评定": inputs[6],  # 第几次评定
        "编号": inputs[7],  # 编号
        "临床诊断": inputs[8],  # 临床诊断

        # 睡眠习惯
        "上床睡觉的时间": inputs[9],  # 上床睡觉的时间
        "入睡时间（分钟）": inputs[10],  # 入睡时间（分钟）
        "早晨起床时间": inputs[11],  # 早晨起床时间
        "每晚实际睡眠时间（分钟）": inputs[12],  # 每晚实际睡眠时间（分钟）

        # 睡眠问题
        "不能在30分钟内入睡": inputs[13],  # 不能在30分钟内入睡
        "在晚上睡眠中醒来或早醒": inputs[14],  # 在晚上睡眠中醒来或早醒
        "晚上有无起床上洗手间": inputs[15],  # 晚上有无起床上洗手间
        "不舒服的呼吸": inputs[16],  # 不舒服的呼吸
        "大声咳嗽或打鼾声": inputs[17],  # 大声咳嗽或打鼾声
        "做不好的梦": inputs[18],  # 做不好的梦
        "感到寒冷": inputs[19],  # 感到寒冷
        "感到太热": inputs[20],  # 感到太热
        "出现疼痛": inputs[21],  # 出现疼痛
        "请描述其他原因": inputs[22],  # 其他原因描述
        "总睡眠质量评分": inputs[23],  # 总睡眠质量评分
        "是否经常服药才能入睡": inputs[24],  # 是否经常服药才能入睡
        "是否难以保持清醒": inputs[25],  # 是否难以保持清醒
        "任务完成难度": inputs[26],  # 任务完成难度

        # 睡眠环境
        "是否与人同睡一床或有室友": inputs[27],  # 是否与人同睡一床或有室友
        "睡觉时是否打鼾": inputs[28],  # 睡觉时是否打鼾
        "是否有呼吸停顿": inputs[29],  # 是否有呼吸停顿
        "是否有腿部抽动": inputs[30],  # 是否有腿部抽动
        "睡觉时是否有方向混乱": inputs[31],  # 睡觉时是否有方向混乱
        "是否有其他睡不安宁的情况": inputs[32],  # 是否有其他睡不安宁的情况
    }

    # 处理 CheckboxGroup 的多选选项
    def handle_checkbox_group(checkbox_input):
        if isinstance(checkbox_input, list):
            return ', '.join(checkbox_input)  # 多选框选项拼接为字符串
        return checkbox_input

    # 遍历所有字段并处理 CheckboxGroup
    for key in form_data:
        if isinstance(form_data[key], list):  # 如果是列表（多选框的返回值）
            form_data[key] = handle_checkbox_group(form_data[key])

    # 返回格式化后的表单数据
    response = processjson2response("匹兹堡睡眠量表", form_data)
    return response

def submit_rbd_survey(*inputs):
    # 创建一个字典，键是问题本身，值是用户的选择
    form_data = {
        "1、我有时做很生动的梦": inputs[0],
        "2、我梦里常出现带攻击或暴力行为": inputs[1],
        "3、我睡着后所做的动作大部分与我梦境一致": inputs[2],
        "4、我知道睡着时我的手或脚会动": inputs[3],
        "5、我睡觉时曾发生或几乎要发生自己受伤或伤及床伴的事": inputs[4],
        "6、我睡觉时发生过或现在存在下列情况": {
            "6.1 说梦话、大喊大叫、咒骂、大笑": inputs[5],
            "6.2 突发肢体大动作，如“打斗”": inputs[6],
            "6.3 睡觉时没必要的手势、复杂动作，如挥手、敬礼、拍蚊子、手伸出床外": inputs[7],
            "6.4 东西掉下床，如床头灯、书本、眼镜等": inputs[8]
        },
        "7、我曾被睡觉后做出的动作惊醒": inputs[9],
        "8、醒后梦的大部分内容我记得很清楚": inputs[10],
        "9、我的睡眠常受上述情况影响": inputs[11],
        "10、我曾患或正患神经系统疾病（如脑卒中、脑外外伤后帕金森综合征、不安腿综合征、发作性睡病、抑郁、癫痫、脑炎等）": inputs[12]
    }
    response = processjson2response("RBDSQ问卷",form_data)

    return response

# 汉密顿抑郁量表
def submit_hamd(*scores):
    # 定义问题列表
    questions = [
        "抑郁情绪", "有罪感", "自杀", "入睡困难", "睡眠不深", "早醒", 
        "工作和兴趣", "阻滞", "激越", "精神性焦虑", "躯体性焦虑", 
        "胃肠道症状", "全身症状", "性症状", "疑病", "体重减轻", "自知力", 
        "日夜变化早", "日夜变化晚", "人格或现实解体", "偏执症状", 
        "强迫症状", "能力减退感", "绝望感", "自卑感"
    ]
    
    # 将得分转换为整数并存储在字典中
    scores_int = [int(score) for score in scores]
    
    # 生成问题与得分的字典
    question_scores = {questions[i]: scores_int[i] for i in range(len(questions))}
    
    # 计算总分
    total_score = sum(scores_int)
    
    # 判断抑郁程度
    if total_score > 35:
        depression_level = "可能为严重抑郁"
    elif total_score > 20:
        depression_level = "中等程度的抑郁"
    elif total_score >= 8:
        depression_level = "可能有轻度抑郁"
    else:
        depression_level = "没有抑郁症状"
    
    # 将总分与抑郁程度添加到结果中
    result = {
        "问题与得分": question_scores,
        "总分": total_score,
        "评分细则": "按照Davis JM的划界分，总分超过35分，可能为严重抑郁；超过20分，中等程度的抑郁；8到20分可能有轻度抑郁，如小于8分，病人就没有抑郁症状",
        "抑郁程度": depression_level
    }
    response = processjson2response("汉密顿焦虑量表", result)

    return response

# 汉密顿焦虑量表
def submit_hama(*scores):
    # 创建问题列表
    questions = [
        "焦虑心境", "紧张", "害怕", "失眠", "认知功能", "抑郁心境",
        "躯体性焦虑", "精神性焦虑", "心血管系统症状", "呼吸系统症状", 
        "胃肠道症状", "生殖泌尿神经系统症状", "植物神经系统症状", "会谈时行为表现"
    ]
    
    # 将评分转换为整数
    scores = [int(score) for score in scores]
    
    # 创建问题与得分的字典
    question_scores = {questions[i]: scores[i] for i in range(len(questions))}
    
    # 计算总分
    total_score = sum(scores)
    
    # 判断焦虑程度
    if total_score > 29:
        anxiety_level = "可能为严重焦虑"
    elif total_score > 21:
        anxiety_level = "肯定有明显焦虑"
    elif total_score > 14:
        anxiety_level = "肯定有焦虑"
    elif total_score > 7:
        anxiety_level = "可能有焦虑"
    else:
        anxiety_level = "没有焦虑症状"
    
    # 构建最终的结果字典
    result = {
        "问题与得分": question_scores,
        "总分": total_score,
        "评分细则": "总分超过29分，可能为严重焦虑，超过21分，肯定有明显焦虑，超过14分肯定有焦虑，超过7分，可能有焦虑，如小于6分，病人没有焦虑症状",
        "焦虑程度": anxiety_level
    }
    response = processjson2response("汉密顿焦虑量表",result)
    
    # 将结果字典转换为 JSON 字符串，方便显示为 Markdown
    return response
# Epworth嗜睡量表
import json

def submit_epworth(*scores):
    # 创建问题列表
    situations = [
        "坐着阅读书刊", "看电视", "在公共场所坐着不动（例如在剧场或开会）", 
        "作为乘客在汽车中坐1小时，中间不休息", "在环境许可时，下午躺下休息", 
        "坐下与人谈话", "午餐不喝酒，餐后安静地坐着", "遇堵车时停车数分钟"
    ]
    
    # 将评分转换为整数
    scores = [int(score) for score in scores]
    
    # 创建问题与得分的字典
    situation_scores = {situations[i]: scores[i] for i in range(len(situations))}
    
    # 计算总分
    total_score = sum(scores)
    
    # 判断嗜睡程度
    if total_score >= 16:
        sleep_level = "极可能打瞌睡"
    elif total_score >= 11:
        sleep_level = "中度嗜睡"
    elif total_score >= 5:
        sleep_level = "轻度嗜睡"
    else:
        sleep_level = "几乎没有嗜睡"
    
    # 构建最终的结果字典
    result = {
        "问题与得分": situation_scores,
        "总分": total_score,
        "评分标准": "0=从不打瞌睡；1= 轻度可能打瞌睡；2=中度可能打瞌睡；3= 很可能打瞌睡。",
        "嗜睡程度": sleep_level
    }
    
    # 将结果字典转换为 JSON 字符串，方便显示为 Markdown
    response = processjson2response("Epworth嗜睡量表", result)    
    return response

# stop_bang
def submit_stopbang(snoring, tiredness, observed_stop_breathing, high_blood_pressure, 
                     bmi, age, neck_circumference, gender):
    # 定义每个问题和其得分
    questions = {
        "1. 您是否经常打鼾？": snoring,
        "2. 您白天是否经常感到疲劳或困倦？": tiredness,
        "3. 您是否被别人注意到夜间有呼吸暂停？": observed_stop_breathing,
        "4. 您是否患有高血压？": high_blood_pressure,
        "5. 您的BMI是否超过35？": bmi,
        "6. 您的年龄是否超过50岁？": age,
        "7. 您的颈围是否超过40厘米？": neck_circumference,
        "8. 您是男性吗？": gender
    }
    
    # 计算总分
    score = sum([int(value) for value in questions.values()])
    
    # 判断是否存在睡眠呼吸暂停风险
    if score >= 3:
        result = "根据您的回答，您可能存在较高的睡眠呼吸暂停风险,为OSAS 高危人群，建议进一步就诊。"
    else:
        result = "您的回答没有明显提示睡眠呼吸暂停的症状。"
    
    # 生成结果的JSON
    json_result = {
        "问题和得分": questions,
        "总分": score,
        "评分标准": "有3项及以上回答为是的人为OSAS 高危人群，小于3项回答为是的为低风险。",
        "评判结果": result
    }
    response = processjson2response("Stop-Bang评判表", json_result)
    return response
# 阿森斯失眠量表
def submit_ais(*answers):
    # 将每个问题的答案组合成一个字典
    score = {
        "入睡时间": answers[0],
        "夜间苏醒": answers[1],
        "比期望的时间早醒": answers[2],
        "总睡眠时间": answers[3],
        "总睡眠质量": answers[4],
        "白天情绪": answers[5],
        "白天身体功能": answers[6],
        "白天思睡": answers[7]
    }
    
    # 构建JSON结果
    json_result = {
        "问题和得分": score,
        "评分标准": "本表主要用于记录遇到过的睡眠障碍的自我评估。"
    }
    response = processjson2response("阿森斯失眠量表", json_result)

    return response
# 国际不宁腿综合征研究组评分标准(IRLSSG）
def calculate_score(*answers):
    questions = [
        "腿部不适症状的严重程度",
        "因腿部不适需要活动的欲望",
        "活动后症状缓解程度",
        "RLS症状对睡眠的影响",
        "RLS症状对疲劳的影响",
        "RLS症状对生活的影响",
        "RLS症状出现的频率",
        "RLS症状的持续时间",
        "RLS症状对日常生活事务的影响",
        "RLS症状对情绪的影响"
    ]
    answers_dict = {questions[i]: answers[i] for i in range(len(answers))}
    response = processjson2response("国际不宁腿综合征研究组评分标准(IRLSSG)", answers_dict)
    # 将答案和对应的问题匹配
    return response