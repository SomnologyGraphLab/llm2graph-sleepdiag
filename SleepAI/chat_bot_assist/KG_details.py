import gradio as gr
import matplotlib.pyplot as plt
from neo4j import GraphDatabase
from matplotlib import font_manager

# 配置中文字体，使用 Windows 中的 SimHei 字体
font_path = "C:\\Windows\\Fonts\\simhei.ttf"  # 替换为适合你系统的字体路径
prop = font_manager.FontProperties(fname=font_path)

# 连接到 Neo4j 数据库
uri = "bolt://localhost:7687"  # 替换成你的 Neo4j 实例地址
username = "neo4j"  # 替换成你的 Neo4j 用户名
password = "G6669963."  # 替换成你的 Neo4j 密码

driver = GraphDatabase.driver(uri, auth=(username, password))

def run_query(query):
    with driver.session() as session:
        result = session.run(query)
        return [record.data() for record in result]

def get_entity_stats():
    # 查询实体总数
    entity_total_count_query = "MATCH (n) RETURN COUNT(n) AS entity_total_count"
    entity_total_count = run_query(entity_total_count_query)

    # 查询实体标签数量及每个标签的个数
    entity_label_query = """
    MATCH (n)
    UNWIND labels(n) AS label
    WITH label, COUNT(label) AS label_count
    ORDER BY label_count DESC
    SKIP 1  // Skip the first item
    LIMIT 10  // Limit the result to the next 8 items (i.e., 2nd to 9th)
    RETURN label, label_count
    """
    entity_label_stats_10 = run_query(entity_label_query)
    entity_label_query = """
    MATCH (n)
    UNWIND labels(n) AS label
    WITH label, COUNT(label) AS label_count
    ORDER BY label_count DESC
    RETURN label, label_count
    """
    entity_label_stats = run_query(entity_label_query)

    return entity_total_count, entity_label_stats_10, entity_label_stats

def get_relationship_stats():
    # 查询关系总数
    relationship_total_count_query = "MATCH ()-[r]->() RETURN COUNT(r) AS relationship_total_count"
    relationship_total_count = run_query(relationship_total_count_query)

    # 查询关系类型数量及类型下的关系数量前10个
    relationship_type_query = """
    MATCH ()-[r]->() 
    WITH type(r) AS relationshipType, COUNT(r) AS relCount
    ORDER BY relCount DESC  // Ensure it's sorted based on count
    SKIP 4  // Skip the most frequent relationship type
    LIMIT 10  // Limit the result to the next 8 relationship types (2nd to 9th)
    RETURN 
    COUNT(DISTINCT relationshipType) AS relationship_type_count,
    COLLECT({type: relationshipType, count: relCount}) AS relationship_type_stats
    """
    relationship_type_stats_10 = run_query(relationship_type_query)

    # 查询关系类型数量及类型下的关系数量
    relationship_type_query = """
    MATCH ()-[r]->() 
    WITH type(r) AS relationshipType, COUNT(r) AS relCount
    ORDER BY relCount DESC  // Ensure it's sorted based on count
    RETURN 
    COUNT(DISTINCT relationshipType) AS relationship_type_count,
    COLLECT({type: relationshipType, count: relCount}) AS relationship_type_stats
    """
    relationship_type_stats = run_query(relationship_type_query)
    return relationship_total_count, relationship_type_stats_10, relationship_type_stats

def generate_chart():
    # 获取实体统计信息
    entity_total_count, entity_label_stats_10, entity_label_stats = get_entity_stats()

    # 获取关系统计信息
    relationship_total_count, relationship_type_stats_10, relationship_type_stats = get_relationship_stats()

    # 获取前10个实体标签和数量
    labels = [item['label'] for item in entity_label_stats_10]
    counts = [item['label_count'] for item in entity_label_stats_10]

    # 绘制实体标签扇形图
    fig, ax1 = plt.subplots(figsize=(8, 6))

    ax1.pie(counts, labels=labels, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors, radius=0.75)
    ax1.axis('equal')  # 确保饼图是圆形的
    ax1.set_title('前10实体标签数量占比扇形图', fontproperties=prop, fontsize=16, fontweight='bold', color='darkblue')  # 增加标题字体大小

    # 添加实体总数的注释
    ax1.text(0, 1.1, f'实体总数: {entity_total_count[0]["entity_total_count"]}', 
             horizontalalignment='center', fontsize=12, color='black', fontproperties=prop)

    # 调整布局，避免标题重叠
    plt.subplots_adjust(top=0.8)

    # 绘制关系类型的饼图
    relationship_types = [item['type'] for item in relationship_type_stats_10[0]['relationship_type_stats']]
    relationship_counts = [item['count'] for item in relationship_type_stats_10[0]['relationship_type_stats']]

    fig2, ax2 = plt.subplots(figsize=(8, 6))
    ax2.pie(relationship_counts, labels=relationship_types, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors, radius=0.75)
    ax2.axis('equal')  # 确保饼图是圆形的
    ax2.set_title('前10关系类型数量占比扇形图', fontproperties=prop, fontsize=16, fontweight='bold', color='darkblue')  # 增加标题字体大小

    # 添加关系总数的注释
    ax2.text(0, 1.1, f'关系总数: {relationship_total_count[0]["relationship_total_count"]}', 
             horizontalalignment='center', fontsize=12, color='black', fontproperties=prop)

    # 调整布局，避免标题重叠
    plt.subplots_adjust(top=0.8)

    return fig, fig2, entity_label_stats, relationship_type_stats


# Gradio 接口
def display_stats():
    # 生成图表
    fig, fig2, E_labels, R_lables = generate_chart()
    return [fig, fig2, E_labels, R_lables]
