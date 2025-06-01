import math
import uuid
from datetime import time
from tkinter import Image
import gradio as gr
from Test4Func.admin import verify_login
from chat_bot_assist.wc import *
import plotly.express as px
import numpy as np
import os
import requests
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from chat_bot_assist.submit_forms import *
from chat_bot_assist.introduction import intro
from chat_bot_assist.KG_details import *
from chat_bot_assist.bot_funcs import  respond, handle_like, handle_retry,handle_undo
from chat_bot_assist.subimit_files import submit_files
from chat_bot_assist import *
from style import self_css
from radio import custom_css

#文本数据
# text = "Chunk Document Person Tests and examinations Session Message Sleep disorder types Symptoms and clinical manifestations Preventive measures and treatment recommendations Related disorders Complications Group Location Organization Diagnostic criteria Risk factors Concept Demographics Entity Email Disease Sleep disorder Therapy Publication Hospital Research center Treatment recommendations"

small_and_beautiful_theme = gr.themes.Soft(
    primary_hue=gr.themes.Color(
        c50="#EAF6FF",  # 浅蓝系列
        c100="#CDEAFE",
        c200="#A0D7FD",
        c300="#6CC0FB",
        c400="#38A9F9",
        c500="#1E90FF",  # 核心蓝色
        c600="#006ED8",
        c700="#005FB8",
        c800="#004E98",
        c900="#003D78",
        c950="#002D58",
        name="small_and_beautiful",
    ),
    secondary_hue=gr.themes.Color(
        c50="#576b95",
        c100="#576b95",
        c200="#576b95",
        c300="#576b95",
        c400="#576b95",
        c500="#576b95",
        c600="#576b95",
        c700="#576b95",
        c800="#576b95",
        c900="#576b95",
        c950="#576b95",
    ),
    neutral_hue=gr.themes.Color(
        name="gray",
        c50="#f6f7f8",
        c100="#F2F2F2",
        c200="#e5e7eb",
        c300="#d1d5db",
        c400="#B2B2B2",
        c500="#808080",
        c600="#636363",
        c700="#515151",
        c800="#393939",
        c900="#2B2B2B",
        c950="#171717",
    ),
    radius_size=gr.themes.sizes.radius_sm,
).set(
    # background_fill_primary="url('https://via.placeholder.com/1500x1000')",  # 设置背景图片
    # background_fill_primary_dark="url('https://via.placeholder.com/1500x1000')",  # 暗色模式下背景图片
    button_primary_background_fill_dark="*primary_600",
    button_primary_border_color_dark="*primary_600",
    button_primary_text_color="white",
    button_primary_text_color_dark="white",
    button_secondary_background_fill="*neutral_50",
    button_secondary_background_fill_hover="*primary_400",
    button_secondary_background_fill_dark="*neutral_800",
    button_secondary_text_color="*neutral_800",
    button_secondary_text_color_dark="white",
    input_background_fill="#F6F6F6",
    block_title_background_fill_dark="*primary_900",
    block_label_background_fill_dark="*primary_900",
)

# spark 总结
from Document_upload_summary import Document_Upload_Summary
# spark 问答
from Document_Q_And_A import Document_Q_And_A,on_error,on_close,on_open,run,on_message
# 在Document_Q_And_A.py中的全局变量不会生效，所以不能通过直接print(recep_mesg)拿到答案


APPId = "xxx"
APISecret = "xxxxxxxx"

dus = Document_Upload_Summary(APPId, APISecret)
doc_qa = Document_Q_And_A(APPId, APISecret)


# 文件
valid_files_group = {'背影.txt':'xxx',
                     '人工智能生成内容白皮书 2022.pdf':'xxx',
                     '2023AIGC市场研究报告及ChatGPT推动的变革趋势与投资机会-甲子光年.pdf':'xxx',
                     'AIGC+AI生成内容产业展望报告-量子位-34页.pdf':'44xx'
                     }


with gr.Blocks(theme=small_and_beautiful_theme, css=custom_css, title="灵犀眠诊--基于GraphRAG的智能问答助手") as demo: # small_and_beautiful_theme
    with gr.Row(elem_id="header"):
        gr.Markdown("# 基于GraphRAG检索式增强的睡眠障碍智能诊断系统 🤗")
    with gr.Row(elem_id="content"):
        with gr.Tab(label="问答系统"):
            chatbot = gr.Chatbot(
                value=[
                    {"role": "user", "content": "Hello!"},
                    {"role": "assistant", "content": """您好！\n
                        您可以询问关于 睡眠障碍 的各种问题\n
                        🟢 覆盖范围：失眠、呼吸暂停、多导睡眠图等\n
                        🟡 输入你的问题，助手将为你提供详细解答。"""},
                ],
                label="""💤 智能睡眠问答助手 💤
                """,
                type="messages",
                avatar_images=(
                    "./sleep.png",
                    "./chat_bot.png",
                ),

            )
            prompt = gr.Textbox(max_lines=1, label="Chat Message",placeholder="请输入您的问题")
            prompt.submit(respond, [prompt, chatbot], [chatbot])
            prompt.submit(lambda: "", None, [prompt])
            chatbot.undo(handle_undo, chatbot, [chatbot, prompt])
            chatbot.retry(handle_retry, chatbot, [chatbot])
            chatbot.like(handle_like, None, None)

            examples = [
                "什么是睡眠障碍？",     
                "影响睡眠的因素有哪些？",          
                "如何改善睡眠质量？",
                "儿童中枢性呼吸暂停是什么，治疗方案有哪些？",
                "什么是日间过度思睡,诊断标准有哪些？",
                "成人因压力大导致的失眠的诊断和治疗方案有哪些？"
            ]

            with gr.Row():
                for i, example in enumerate(examples):
                    if i // 3 == 0:
                        example_box = gr.Button(example, elem_id=f"example")
                        # 当按钮被点击时，将示例文本传给聊天输入并调用 bot
                        example_box.click(
                            fn=lambda example_text: example_text,
                            inputs=[gr.Textbox(value=example, visible=False)],
                            outputs=[prompt]
                        ).then(
                            fn=respond,
                            inputs=[prompt, chatbot],
                            outputs=[chatbot],
                        ).then(
                            fn=lambda: "",
                            inputs=None,
                            outputs=[prompt]
                        )
            with gr.Row():
                for i, example in enumerate(examples):
                    if i // 3 == 1:
                        example_box = gr.Button(example, elem_id=f"example")
                        # 当按钮被点击时，将示例文本传给聊天输入并调用 bot
                        example_box.click(
                            fn=lambda example_text: example_text,
                            inputs=[gr.Textbox(value=example, visible=False)],
                            outputs=[prompt]
                        ).then(
                            fn=respond,
                            inputs=[prompt, chatbot],
                            outputs=[chatbot],
                        ).then(
                            fn=lambda: "",
                            inputs=None,
                            outputs=[prompt]
                        )

            # file_input = gr.Files(
            #     file_types=["file"],
            #     label="Upload Files",
            #     file_count="multiple"
            # )
            # 输入：[chatbot, chat_input]，即当前聊天记录和用户输入。
            # 输出：[更新后的 chatbot（聊天记录）和 chat_input（重置输入框）]
            # bot_msg.then(lambda: gr.MultimodalTextbox(interactive=True), None, [chat_input])
        with gr.Tab(label="量表诊断"):
            with gr.Tab("匹兹堡睡眠量表"):
                gr.HTML("<h3>请根据您的真实情况填写下列的量表调查：</h3>")        
                with gr.TabItem("基本信息"):
                    with gr.Column():
                        name = gr.Textbox(label="姓名", placeholder="请输入姓名")
                        gender = gr.Radio(choices=["男", "女"], label="性别")
                        age = gr.Slider(minimum=0, maximum=100, step=1, label="年龄", interactive=True)
                        education = gr.Dropdown(
                            choices=["小学", "初中", "高中", "专科", "本科", "硕士", "博士", "博士后", "其他"],
                            label="文化程度"
                        )
                        # 职业下拉列表，增加了更多选项
                        occupation = gr.Dropdown(
                            choices=["医生", "教师", "工程师", "学生", "护士", "律师", "会计", "程序员", "设计师", "市场营销", "行政人员", "项目经理", "科研人员", "其他"],
                            label="职业"
                        )
                        assessment_date = gr.DateTime(label="评定日期", type='date')
                        times_assessed = gr.Number(label="第几次评定")
                        patient_id = gr.Textbox(label="编号")
                        diagnosis = gr.Textbox(label="临床诊断")
                
                # 睡眠习惯 tab
                with gr.TabItem("睡眠习惯"):
                    with gr.Column():
                        # 使用 gr.TimePicker 选择时间
                        bed_time = gr.Textbox(label="上床睡觉的时间 (HH:MM)", placeholder="例如: 22:30")
                        wake_up_time = gr.Textbox(label="早晨起床时间 (HH:MM)", placeholder="例如: 06:30")
                        
                        sleep_time = gr.Textbox(
                            label="入睡时间（分钟）",
                            placeholder="请输入入睡时间（分钟）",
                        )
                        
                        # 同样，为实际睡眠时间使用 gr.Textbox 组件并设置 placeholder
                        actual_sleep_time = gr.Textbox(
                            label="每晚实际睡眠时间（分钟）",
                            placeholder="请输入实际睡眠时间（分钟）",
                        )

                with gr.TabItem("睡眠问题"):
                    with gr.Column():
                        # 问题 5
                        gr.HTML("<h3>过去一个月是否因为以下问题而经常睡眠不好，请按照您的实际情况进行选择：</h3>")
                        insomnia_a = gr.Radio(
                            label="不能在30分钟内入睡",
                            choices=["没有", "每周平均不足一个晚上", "每周平均一或两个晚上", "每周平均三个或更多晚上"]
                        )
                        insomnia_b = gr.Radio(
                            label="在晚上睡眠中醒来或早醒",
                            choices=["没有", "每周平均不足一个晚上", "每周平均一或两个晚上", "每周平均三个或更多晚上"]
                        )
                        insomnia_c = gr.Radio(
                            label="晚上有无起床上洗手间",
                            choices=["没有", "每周平均不足一个晚上", "每周平均一或两个晚上", "每周平均三个或更多晚上"]
                        )
                        insomnia_d = gr.Radio(
                            label="不舒服的呼吸",
                            choices=["没有", "每周平均不足一个晚上", "每周平均一或两个晚上", "每周平均三个或更多晚上"]
                        )
                        insomnia_e = gr.Radio(
                            label="大声咳嗽或打鼾声",
                            choices=["没有", "每周平均不足一个晚上", "每周平均一或两个晚上", "每周平均三个或更多晚上"]
                        )
                        insomnia_f = gr.Radio(
                            label="感到寒冷",
                            choices=["没有", "每周平均不足一个晚上", "每周平均一或两个晚上", "每周平均三个或更多晚上"]
                        )
                        insomnia_g = gr.Radio(
                            label="感到太热",
                            choices=["没有", "每周平均不足一个晚上", "每周平均一或两个晚上", "每周平均三个或更多晚上"]
                        )
                        insomnia_h = gr.Radio(
                            label="做不好的梦",
                            choices=["没有", "每周平均不足一个晚上", "每周平均一或两个晚上", "每周平均三个或更多晚上"]
                        )
                        insomnia_i = gr.Radio(
                            label="出现疼痛",
                            choices=["没有", "每周平均不足一个晚上", "每周平均一或两个晚上", "每周平均三个或更多晚上"]
                        )
                        other_reason_description = gr.Textbox(label="请描述其他原因")
                        sleep_quality = gr.Radio(
                            label="你对过去一个月总睡眠质量评分",
                            choices=["非常好", "尚好", "不好", "非常差"]
                        )
                        medication = gr.Radio(
                            label="过去一个月，你是否经常要服药才能入睡",
                            choices=["没有", "每周平均不足一个晚上", "每周平均一或两个晚上", "每周平均三个或更多晚上"]
                        )
                        alertness = gr.Radio(
                            label="过去一个月你在开车、吃饭或参加社会活动时难以保持清醒状态",
                            choices=["没有", "每周平均不足一个晚上", "每周平均一或两个晚上", "每周平均三个或更多晚上"]
                        )
                        task_difficulty = gr.Radio(
                            label="过去一个月，你在积极完成时事情上是否有困难",
                            choices=["没有困难", "有一点困难", "比较困难", "非常困难"]
                        )

                with gr.TabItem("睡眠环境"):
                    with gr.Column():
                        # 问题 10
                        bed_sharing = gr.Radio(
                            label="你是与人同睡一床（睡觉同伴，包括配偶）或有室友",
                            choices=["没有与人同睡一床或有室友", "同伴或室友在另外房间", "同伴在同一房间但不睡同床", "同伴在同一床上"]
                        )
                        gr.HTML("<h3>如果你是与人同睡一床或有室友，请询问他（她）你过去一个月是否出现以下情况:</h3>")
                        snoring = gr.Radio(
                            label="你在睡觉时，有无打鼾声",
                            choices=["没有", "每周平均不足一个晚上", "每周平均一或两个晚上", "每周平均三个或更多晚上"]
                        )
                        breathing_pause = gr.Radio(
                            label="在你睡觉时，呼吸之间有没有长时间停顿",
                            choices=["没有", "每周平均不足一个晚上", "每周平均一或两个晚上", "每周平均三个或更多晚上"]
                        )
                            # 睡眠问题部分
                        leg_movement = gr.Radio(
                            label="在你睡觉时，你的腿是否有抽动或者有痉挛",
                            choices=["没有", "每周平均不足一个晚上", "每周平均一或两个晚上", "每周平均三个或更多晚上"]
                        )
                        confusion = gr.Radio(
                            label="在你睡觉时是否出现不能辨认方向或混乱状态",
                            choices=["没有", "每周平均不足一个晚上", "每周平均一或两个晚上", "每周平均三个或更多晚上"]
                        )
                        other_sleep_problems = gr.Radio(
                            label="在你睡觉时是否有其他睡不安宁的情况",
                            choices=["没有", "每周平均不足一个晚上", "每周平均一或两个晚上", "每周平均三个或更多晚上"]
                        )
                        other_sleep_problems_description = gr.Textbox(
                            label="请描述其他睡不安宁的情况"
                        )
                with gr.TabItem("提交"):
                    gr.Button("提交", elem_id="submit").click(submit_form, 
                        inputs=[name, gender, age, education, occupation, assessment_date, times_assessed, patient_id, diagnosis,
                                    bed_time, sleep_time, wake_up_time, actual_sleep_time, insomnia_a, insomnia_b, insomnia_c, insomnia_d,
                                    insomnia_e, insomnia_f, insomnia_g, insomnia_h, insomnia_i,  other_reason_description,
                                    sleep_quality, medication, alertness, task_difficulty, bed_sharing, snoring, breathing_pause,
                                    leg_movement, confusion, other_sleep_problems],
                        outputs=gr.Markdown(
                            value="初步诊断和初步诊疗建议\n这里将显示您的诊断结果...", 
                            height="400px",  # 设置高度
                            max_height="900px",  # 设置最大高度
                            min_height="200px",  # 设置最小高度
                            show_copy_button=True,  # 显示复制按钮
                            container=True,  # 显示为容器
                            # elem_classes=["my-markdown"],  # 设置CSS类名
                            sanitize_html=True  # 启用HTML消毒
                        )           
                )
                    
            with gr.Tab("RBDSQ 问卷"):
                gr.HTML("<h3>请根据您的最近的睡眠情况填写下列的量表调查：</h3>")        

                with gr.Column():
                    # 问题1到问题10
                    dreams = gr.Radio(choices=["是", "否"], label="1、我有时做很生动的梦")
                    aggressive_dreams = gr.Radio(choices=["是", "否"], label="2、我梦里常出现带攻击或暴力行为")
                    actions_matching_dreams = gr.Radio(choices=["是", "否"], label="3、我睡着后所做的动作大部分与我梦境一致")
                    know_movement_when_sleeping = gr.Radio(choices=["是", "否"], label="4、我知道睡着时我的手或脚会动")
                    injury_or_nearly_injured_others = gr.Radio(choices=["是", "否"], label="5、我睡觉时曾发生或几乎要发生自己受伤或伤及床伴的事")
                    
                    sleep_issues_section = gr.Accordion("6、我睡觉时发生过或现在存在下列情况", open=False)
                    with sleep_issues_section:
                        talking_dreams = gr.Radio(choices=["是", "否"], label="6.1 说梦话、大喊大叫、咒骂、大笑")
                        violent_movements = gr.Radio(choices=["是", "否"], label="6.2 突发肢体大动作，如“打斗”")
                        unnecessary_movements = gr.Radio(choices=["是", "否"], label="6.3 睡觉时没必要的手势、复杂动作，如挥手、敬礼、拍蚊子、手伸出床外")
                        items_falling = gr.Radio(choices=["是", "否"], label="6.4 东西掉下床，如床头灯、书本、眼镜等")
                    
                    waking_from_own_movements = gr.Radio(choices=["是", "否"], label="7、我曾被睡觉后做出的动作惊醒")
                    remember_dreams = gr.Radio(choices=["是", "否"], label="8、醒后梦的大部分内容我记得很清楚")
                    sleep_affected_by_issues = gr.Radio(choices=["是", "否"], label="9、我的睡眠常受上述情况影响")
                    neurological_conditions = gr.Radio(choices=["是", "否"], label="10、我曾患或正患神经系统疾病（如脑卒中、脑外外伤后帕金森综合征、不安腿综合征、发作性睡病、抑郁、癫痫、脑炎等）")
                    gr.Button("提交", elem_id="submit").click(submit_rbd_survey, 
                        inputs=[
                            dreams, aggressive_dreams, actions_matching_dreams, know_movement_when_sleeping, injury_or_nearly_injured_others,
                            talking_dreams, violent_movements, unnecessary_movements, items_falling,
                            waking_from_own_movements, remember_dreams, sleep_affected_by_issues, neurological_conditions
                        ], 
                    outputs=gr.Markdown(
                        value="初步诊断和初步诊疗建议\n这里将显示您的诊断结果...", 
                        height="400px",  # 设置高度
                        max_height="900px",  # 设置最大高度
                        min_height="200px",  # 设置最小高度
                        show_copy_button=True,  # 显示复制按钮
                        container=True,  # 显示为容器
                        # elem_classes=["my-markdown"],  # 设置CSS类名
                        sanitize_html=True  # 启用HTML消毒
                    )
                )
            with gr.Tab("汉密顿抑郁量表"):
                gr.HTML("<h3>请根据您的真实情况选择相应的症状程度(0->4: 症状轻-> 症状重)：</h3>")        
                with gr.Column():
                    # 1-24 题的评分，范围 0-4
                    depression_mood = gr.Radio(["0", "1", "2", "3", "4"], label="1．抑郁情绪", value="0")
                    guilt_feelings = gr.Radio(["0", "1", "2", "3"], label="2．有罪感", value="0")
                    suicidal_tendency = gr.Radio(["0", "1", "2", "3", "4"], label="3．自杀", value="0")
                    sleep_difficulty = gr.Radio(["0", "1", "2"], label="4．入睡困难", value="0")
                    shallow_sleep = gr.Radio(["0", "1", "2"], label="5．睡眠不深", value="0")
                    early_waking = gr.Radio(["0", "1", "2"], label="6．早醒", value="0")
                    work_interest = gr.Radio(["0", "1", "2", "3", "4"], label="7．工作和兴趣", value="0")
                    retardation = gr.Radio(["0", "1", "2", "3", "4"], label="8．阻滞", value="0")
                    agitation = gr.Radio(["0", "1", "2", "3", "4"], label="9．激越", value="0")
                    anxiety_mental = gr.Radio(["0", "1", "2", "3", "4"], label="10．精神性焦虑", value="0")
                    anxiety_physical = gr.Radio(["0", "1", "2", "3", "4"], label="11．躯体性焦虑", value="0")
                    gastrointestinal = gr.Radio(["0", "1", "2"], label="12．胃肠道症状", value="0")
                    general_symptoms = gr.Radio(["0", "1", "2"], label="13．全身症状", value="0")
                    sexual_symptoms = gr.Radio(["0", "1", "2"], label="14．性症状", value="0")
                    hypochondriasis = gr.Radio(["0", "1", "2", "3", "4"], label="15．疑病", value="0")
                    weight_loss = gr.Radio(["0", "1", "2"], label="16．体重减轻", value="0")
                    self_awareness = gr.Radio(["0", "1", "2"], label="17．自知力", value="0")
                    
                    day_night_variation_early = gr.Radio(
                        label="18. 日夜变化A. 早",
                        choices=["0", "1", "2"],
                        value="0",  # 默认值
                        type="index"  # 返回索引值
                    )
                    
                    # 日夜变化 - 晚
                    day_night_variation_late = gr.Radio(
                        label="18. 日夜变化B. 晚",
                        choices=["0", "1", "2"],
                        value="0",  # 默认值
                        type="index"  # 返回索引值
                    )
                    
                    personality_dissociation = gr.Radio(["0", "1", "2", "3", "4"], label="19．人格或现实解体", value="0")
                    paranoia = gr.Radio(["0", "1", "2", "3", "4"], label="20．偏执症状", value="0")
                    compulsive_symptoms = gr.Radio(["0", "1", "2"], label="21．强迫症状", value="0")
                    ability_decline = gr.Radio(["0", "1", "2", "3", "4"], label="22．能力减退感", value="0")
                    despair = gr.Radio(["0", "1", "2", "3", "4"], label="23．绝望感", value="0")
                    inferiority = gr.Radio(["0", "1", "2", "3", "4"], label="24．自卑感", value="0")
                
                with gr.TabItem("提交"):
                    gr.Button("提交", elem_id="submit").click(submit_hamd, 
                        inputs=[
                            depression_mood, guilt_feelings, suicidal_tendency, sleep_difficulty, shallow_sleep, early_waking, 
                            work_interest, retardation, agitation, anxiety_mental, anxiety_physical, gastrointestinal, general_symptoms, 
                            sexual_symptoms, hypochondriasis, weight_loss, self_awareness, day_night_variation_early,day_night_variation_late, 
                            personality_dissociation, paranoia, compulsive_symptoms, ability_decline, despair, inferiority
                        ], 
                    outputs=gr.Markdown(
                        value="初步诊断和初步诊疗建议\n这里将显示您的诊断结果...", 
                        height="400px",  # 设置高度
                        max_height="900px",  # 设置最大高度
                        min_height="200px",  # 设置最小高度
                        show_copy_button=True,  # 显示复制按钮
                        container=True,  # 显示为容器
                        # elem_classes=["my-markdown"],  # 设置CSS类名
                        sanitize_html=True  # 启用HTML消毒
                    )
                    )
            with gr.Tab("汉密顿焦虑量表"):
                gr.HTML("<h3>请根据您的真实情况选择相应的症状程度(0->4: 症状轻-> 症状重)：</h3>")        
                with gr.Column():
                    # 1-14 题的评分，范围 0-4
                    anxiety_mood = gr.Radio(["0", "1", "2", "3", "4"], label="1．焦虑心境", value="0")
                    tension = gr.Radio(["0", "1", "2", "3", "4"], label="2．紧张", value="0")
                    fear = gr.Radio(["0", "1", "2", "3", "4"], label="3．害怕", value="0")
                    insomnia = gr.Radio(["0", "1", "2", "3", "4"], label="4．失眠", value="0")
                    cognitive_function = gr.Radio(["0", "1", "2", "3", "4"], label="5．认知功能", value="0")
                    depressive_mood = gr.Radio(["0", "1", "2", "3", "4"], label="6．抑郁心境", value="0")
                    somatic_anxiety = gr.Radio(["0", "1", "2", "3", "4"], label="7．躯体性焦虑", value="0")
                    mental_anxiety = gr.Radio(["0", "1", "2", "3", "4"], label="8．精神性焦虑", value="0")
                    cardiovascular_symptoms = gr.Radio(["0", "1", "2", "3", "4"], label="9．心血管系统症状", value="0")
                    respiratory_symptoms = gr.Radio(["0", "1", "2", "3", "4"], label="10．呼吸系统症状", value="0")
                    gastrointestinal_symptoms = gr.Radio(["0", "1", "2", "3", "4"], label="11．胃肠道症状", value="0")
                    genitourinary_neurological = gr.Radio(["0", "1", "2", "3", "4"], label="12．生殖泌尿神经系统症状", value="0")
                    autonomic_symptoms = gr.Radio(["0", "1", "2", "3", "4"], label="13．植物神经系统症状", value="0")
                    behavior_during_interview = gr.Radio(["0", "1", "2", "3", "4"], label="14．会谈时行为表现", value="0")
                
                with gr.TabItem("提交"):
                    gr.Button("提交", elem_id="submit").click(submit_hama, 
                        inputs=[
                            anxiety_mood, tension, fear, insomnia, cognitive_function, depressive_mood, 
                            somatic_anxiety, mental_anxiety, cardiovascular_symptoms, respiratory_symptoms, gastrointestinal_symptoms, 
                            genitourinary_neurological, autonomic_symptoms, behavior_during_interview
                        ], 
                    outputs=gr.Markdown(
                        value="初步诊断和初步诊疗建议\n这里将显示您的诊断结果...", 
                        height="400px",  # 设置高度
                        max_height="900px",  # 设置最大高度
                        min_height="200px",  # 设置最小高度
                        show_copy_button=True,  # 显示复制按钮
                        container=True,  # 显示为容器
                        # elem_classes=["my-markdown"],  # 设置CSS类名
                        sanitize_html=True  # 启用HTML消毒
                    )
                    )
            with gr.Tab("Epworth嗜睡量表"):
                gr.HTML("<h5>在下列情况下你打瞌睡（不仅仅是感到疲倦）的可能如何？这是指你最近几月的通常生活情况；假如你最近没有做过其中的某些事情，请试着填上它们可能会给你带来多大的影响。运用下列标度给每种情况选出最适当的数字，从每一行中选一个最符合你情况的数字，用  表示：0=从不打瞌睡；1= 轻度可能打瞌睡；2=中度可能打瞌睡；3= 很可能打瞌睡。</h5>")

                with gr.Column():
                    # 8个问题，每个问题的评分范围是 0 - 3
                    sitting_reading = gr.Radio([0, 1, 2, 3], label="1．坐着阅读书刊", value=0)
                    watching_tv = gr.Radio([0, 1, 2, 3], label="2．看电视", value=0)
                    sitting_in_public = gr.Radio([0, 1, 2, 3], label="3．在公共场所坐着不动（例如在剧场或开会）", value=0)
                    passenger_in_car = gr.Radio([0, 1, 2, 3], label="4．作为乘客在汽车中坐1小时，中间不休息", value=0)
                    afternoon_rest = gr.Radio([0, 1, 2, 3], label="5．在环境许可时，下午躺下休息", value=0)
                    talking_to_others = gr.Radio([0, 1, 2, 3], label="6．坐下与人谈话", value=0)
                    after_lunch_sitting = gr.Radio([0, 1, 2, 3], label="7．午餐不喝酒，餐后安静地坐着", value=0)
                    car_traffic_stop = gr.Radio([0, 1, 2, 3], label="8．遇堵车时停车数分钟", value=0)
                
                with gr.TabItem("提交"):
                    gr.Button("提交", elem_id="submit").click(submit_epworth, 
                        inputs=[
                            sitting_reading, watching_tv, sitting_in_public, passenger_in_car, afternoon_rest, 
                            talking_to_others, after_lunch_sitting, car_traffic_stop
                        ], 
                    outputs=gr.Markdown(
                        value="初步诊断和初步诊疗建议\n这里将显示您的诊断结果...", 
                        height="400px",  # 设置高度
                        max_height="900px",  # 设置最大高度
                        min_height="200px",  # 设置最小高度
                        show_copy_button=True,  # 显示复制按钮
                        container=True,  # 显示为容器
                        # elem_classes=["my-markdown"],  # 设置CSS类名
                        sanitize_html=True  # 启用HTML消毒
                    )
                    )
            with gr.Tab("Stop-Bang评判表"):
                gr.HTML("<h3>请根据您的真实情况如实回答下列的问题：</h3>")
                with gr.Column():
                    # 8个问题的可选框
                    snoring = gr.Checkbox(label="1. 您是否经常打鼾？", value=False)
                    tiredness = gr.Checkbox(label="2. 您白天是否经常感到疲劳或困倦？", value=False)
                    observed_stop_breathing = gr.Checkbox(label="3. 您是否被别人注意到夜间有呼吸暂停？", value=False)
                    high_blood_pressure = gr.Checkbox(label="4. 您是否患有高血压？", value=False)
                    bmi = gr.Checkbox(label="5. 您的BMI是否超过35？", value=False)
                    age = gr.Checkbox(label="6. 您的年龄是否超过50岁？", value=False)
                    neck_circumference = gr.Checkbox(label="7. 您的颈围是否超过40厘米？", value=False)
                    gender = gr.Checkbox(label="8. 您是男性吗？", value=False)
                
                with gr.TabItem("提交"):
                    gr.Button("提交", elem_id="submit").click(submit_stopbang, 
                        inputs=[snoring, tiredness, observed_stop_breathing, high_blood_pressure, bmi, age, neck_circumference, gender], 
                        outputs=gr.Markdown(
                            value="初步诊断和初步诊疗建议\n这里将显示您的诊断结果...", 
                            height="400px",  # 设置高度
                            max_height="900px",  # 设置最大高度
                            min_height="200px",  # 设置最小高度
                            show_copy_button=True,  # 显示复制按钮
                            container=True,  # 显示为容器
                            # elem_classes=["my-markdown"],  # 设置CSS类名
                            sanitize_html=True  # 启用HTML消毒
                    )
                    )
            with gr.Tab("阿森斯失眠量表 (AIS)"):
                # 表格头部提示
                gr.HTML("<h3>请根据您在过去一个月内的睡眠情况选择适当的选项：</h3>")
                
                with gr.Column():
                    # 问题1：入睡时间
                    sleep_onset = gr.Radio(
                        choices=["没问题", "轻微延迟", "显著延迟", "延迟严重或没有睡觉"],
                        label="1. 入睡时间（关灯后到睡着的时间）",
                        value="没问题"
                    )
                    # 问题2：夜间苏醒
                    night_awake = gr.Radio(
                        choices=["没问题", "轻微影响", "显著影响", "严重影响或没有睡觉"],
                        label="2. 夜间苏醒",
                        value="没问题"
                    )
                    # 问题3：比期望的时间早醒
                    early_wake = gr.Radio(
                        choices=["没问题", "轻微提早", "显著提早", "严重提早或没有睡觉"],
                        label="3. 比期望的时间早醒",
                        value="没问题"
                    )
                    # 问题4：总睡眠时间
                    sleep_duration = gr.Radio(
                        choices=["足够", "轻微不足", "显著不足", "严重不足或没有睡觉"],
                        label="4. 总睡眠时间",
                        value="足够"
                    )
                    # 问题5：总睡眠质量
                    sleep_quality = gr.Radio(
                        choices=["满意", "轻微不满", "显著不满", "严重不满或没有睡觉"],
                        label="5. 总睡眠质量（无论睡多长）",
                        value="满意"
                    )
                    # 问题6：白天情绪
                    daytime_mood = gr.Radio(
                        choices=["正常", "轻微低落", "显著低落", "严重低落"],
                        label="6. 白天情绪",
                        value="正常"
                    )
                    # 问题7：白天身体功能
                    daytime_function = gr.Radio(
                        choices=["足够", "轻微影响", "显著影响", "严重影响"],
                        label="7. 白天身体功能（体力或精神：如记忆力、认知力和注意力等）",
                        value="足够"
                    )
                    # 问题8：白天思睡
                    daytime_sleepiness = gr.Radio(
                        choices=["无思睡", "轻微思睡", "显著思睡", "严重思睡"],
                        label="8. 白天思睡",
                        value="无思睡"
                    )
                
                # 提交按钮
                with gr.TabItem("提交"):
                    gr.Button("提交", elem_id="submit").click(submit_ais, 
                        inputs=[sleep_onset, night_awake, early_wake, sleep_duration, sleep_quality,
                                daytime_mood, daytime_function, daytime_sleepiness],
                    outputs=gr.Markdown(
                        value="初步诊断和初步诊疗建议\n这里将显示您的诊断结果...", 
                        height="400px",  # 设置高度
                        max_height="900px",  # 设置最大高度
                        min_height="200px",  # 设置最小高度
                        show_copy_button=True,  # 显示复制按钮
                        container=True,  # 显示为容器
                        # elem_classes=["my-markdown"],  # 设置CSS类名
                        sanitize_html=True  # 启用HTML消毒
                    )
                    )

            with gr.Tab("国际不宁腿综合征评分标准 (IRLSSG)"):
                gr.HTML("<h3>请根据您最近1周的情况回答以下问题：</h3>")
                
                with gr.Column():
                    # 问题1：腿部不适症状的严重程度
                    q1 = gr.Radio(
                        choices=["A 非常严重", "B 严重", "C 中度", "D 轻度", "E 没有不适"],
                        label="1. 总体上讲，您腿部（或者：臂部）的不适症状达到何种程度？",
                        value="E 没有不适"
                    )
                    # 问题2：因腿部不适需要活动的欲望
                    q2 = gr.Radio(
                        choices=["A 非常严重", "B 严重", "C 中度", "D 轻度", "E 没有不适"],
                        label="2. 总体上讲，您因为腿部不适而需要起来活动的欲望达到何种程度？",
                        value="E 没有不适"
                    )
                    # 问题3：活动后症状缓解程度
                    q3 = gr.Radio(
                        choices=["A 没有缓解", "B 稍缓解", "C 中度缓解", "D 完全或几乎完全缓解", "E 没有RLS症状"],
                        label="3. 总体上讲，通过活动，您腿部（或：臂部）的不适症状得到多大程度的缓解？",
                        value="E 没有RLS症状"
                    )
                    # 问题4：RLS症状对睡眠的影响
                    q4 = gr.Radio(
                        choices=["A 非常严重", "B 严重", "C 中度", "D 轻度", "E 没有影响"],
                        label="4. 总体上讲，因为RLS症状，您的睡眠受到多大的影响？",
                        value="E 没有影响"
                    )
                    # 问题5：RLS症状对疲劳的影响
                    q5 = gr.Radio(
                        choices=["A 非常严重", "B 严重", "C 中度", "D 轻度", "E 完全没有"],
                        label="5. 因为RLS的症状，您的疲惫和困倦感达到何种程度？",
                        value="E 完全没有"
                    )
                    # 问题6：RLS症状对生活的影响
                    q6 = gr.Radio(
                        choices=["A 非常严重", "B 严重", "C 中度", "D 轻度", "E 没有影响"],
                        label="6. 总体上讲，您RLS症状对生活的影响有多严重？",
                        value="E 没有影响"
                    )
                    # 问题7：RLS症状出现的频率
                    q7 = gr.Radio(
                        choices=["A 非常频繁，6-7天/周", "B 频繁，4-5天/周", "C 中度，2-3天/周", "D 偶尔，<1次/周", "E 无症状出现"],
                        label="7. 您多久出现一次RLS症状？",
                        value="E 无症状出现"
                    )
                    # 问题8：RLS症状的持续时间
                    q8 = gr.Radio(
                        choices=["A 非常严重，≥8小时/日", "B 严重，3-8小时/日", "C 中度，1-3小时/日", "D 轻度，≤1小时/日", "E 无症状出现"],
                        label="8. 如果出现RLS症状，一天内的平均持续时间有多久？",
                        value="E 无症状出现"
                    )
                    # 问题9：RLS症状对日常生活事务的影响
                    q9 = gr.Radio(
                        choices=["A 非常严重", "B 严重", "C 中度", "D 轻度", "E 没有影响"],
                        label="9. 总体上讲，您的RLS症状对您处理日常生活事务的能力有多大影响？",
                        value="E 没有影响"
                    )
                    # 问题10：RLS症状对情绪的影响
                    q10 = gr.Radio(
                        choices=["A 非常严重", "B 严重", "C 中度", "D 轻度", "E 没有影响"],
                        label="10. 您的RLS症状对您情绪的影响有多严重？",
                        value="E 没有影响"
                    )
                
                    gr.Button("提交", elem_id="submit").click(calculate_score, 
                        inputs=[q1, q2, q3, q4, q5, q6, q7, q8, q9, q10],
                    outputs=gr.Markdown(
                        value="初步诊断和初步诊疗建议\n这里将显示您的诊断结果...", 
                        height="400px",  # 设置高度
                        max_height="900px",  # 设置最大高度
                        min_height="200px",  # 设置最小高度
                        show_copy_button=True,  # 显示复制按钮
                        container=True,  # 显示为容器
                        # elem_classes=["my-markdown"],  # 设置CSS类名
                        sanitize_html=True  # 启用HTML消毒
                    )
                    )

        with gr.Tab(label="词云"):
            # create_wordcloud(text)
            # gr.Image("img.jpg", label="Generated Word Cloud", show_label=False)
            button1 = gr.Button("Generate and Display The Entities")  # 按钮
            output_image1 = gr.Image(type="filepath", label="Generated Word Cloud", show_label=False)  # 图片输出

            # 按钮点击事件，生成并显示图片
            button1.click(create_wordcloud_E, outputs=[output_image1])

            button2 = gr.Button("Generate and Display The Relationships")
            output_image2 = gr.Image(type="filepath", label="Generated Word Cloud", show_label=False)
            button2.click(create_wordcloud_R, outputs=[output_image2])
        with gr.Tab(label="知识图谱详情"):
            # 按钮触发图表更新
            button1 = gr.Button("生成并显示实体和关系统计图", variant="primary", size="lg")
            
            # 结果区域
            with gr.Row():
                with gr.Column(scale=1):
                    fig1 = gr.Plot(label="实体统计图")
                with gr.Column(scale=1):
                    fig2 = gr.Plot(label="关系统计图")

            # JSON 统计区域
            with gr.Row():
                with gr.Column(scale=1):
                    json1 = gr.JSON(label="实体标签统计 (JSON)", open=False, height=300)
                with gr.Column(scale=1):
                    json2 = gr.JSON(label="关系标签统计 (JSON)", open=False, height=300)
                    
            button1.click(display_stats, outputs=[fig1, fig2, json1, json2])


        # 知识库编辑界面
        with gr.Tab(label="知识库编辑"):
            # 使用 Row 和 Column 组合排列组件
            with gr.Column():  # 将内容垂直排列
                # 样式美观的上传说明文字
                gr.Markdown("### 上传您的文本文件以用于知识图谱扩充")                
                # 上传文件组件
                index_files = gr.Files(label="上传文件", type="filepath", elem_id="upload-index-file")
                
                # 使用开关按钮表达用户满意度
                dissatisfy = gr.Checkbox(
                    label="我因为对该app回答的内容不满意，选择进行补充知识库",
                    value=False,
                    elem_classes="switch-checkbox",
                    elem_id="gr-websearch-cb"
                )
                
                # 提交按钮
                submit_button = gr.Button("提交该文本用于知识图谱扩充")
                submission_status = gr.Markdown("")  # 显示提交状态区域

                
            # 绑定提交按钮事件
            submit_button.click(
                fn=submit_files,
                inputs=[index_files, dissatisfy],
                outputs=submission_status
            )
        with gr.Tab(label="项目详情"):
            gr.Markdown(intro)
            # 构建 Gradio 页面
        with gr.Tab(label="登录管理后台"):
            with gr.Column(elem_classes="login-box",min_width=100):
                gr.Markdown("### 🔐 管理后台登录")

                username = gr.Textbox(label="👤 用户名", placeholder="请输入用户名")
                password = gr.Textbox(label="🔑 密码", type="password", placeholder="请输入密码")
                login_btn = gr.Button("🚪 登录")

                jump_area = gr.HTML()
                error_info = gr.HTML()

                login_btn.click(fn=verify_login, inputs=[username, password], outputs=[jump_area, error_info])
if __name__ == "__main__":
    # demo.queue().launch(show_api=False)

    # demo.queue().launch(server_name="0.0.0.0", server_port=9350, show_api=False)
    demo.queue().launch(server_name="127.0.0.1", server_port=9350, show_api=False)
