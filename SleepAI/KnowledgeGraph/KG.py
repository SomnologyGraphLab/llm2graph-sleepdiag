import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import networkx as nx
from py2neo import Graph
import gradio as gr

# 设置中文字体
def set_chinese_font():
    # 设置中文字体为 SimHei (黑体)
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
    plt.rcParams['axes.unicode_minus'] = False   # 正常显示负号

# Neo4j 数据库连接
class Neo4jConnector:
    def __init__(self, uri, user, password):
        self.graph = Graph(uri, auth=(user, password))

    def fetch_graph_data(self):
        query = """
        MATCH (n)-[r]->(m)
        WHERE n.id IS NOT NULL AND m.id IS NOT NULL AND labels(n)[0] IS NOT NULL AND labels(m)[0] IS NOT NULL
        RETURN n.id AS from_node, 
               labels(n)[0] AS from_label, 
               type(r) AS relationship, 
               m.id AS to_node, 
               labels(m)[0] AS to_label
        LIMIT 50
        """
        result = self.graph.run(query).data()
        return result

def build_graph(data):
    G = nx.DiGraph()
    for record in data:
        from_node = record["from_node"]
        to_node = record["to_node"]
        relationship = record["relationship"]
        G.add_node(from_node, label=record["from_label"])
        G.add_node(to_node, label=record["to_label"])
        G.add_edge(from_node, to_node, relationship=relationship)
    return G

def visualize_graph(G):
    set_chinese_font()  # 设置中文字体
    pos = nx.spring_layout(G, k=0.5)  # 调整节点间距
    plt.figure(figsize=(12, 10))

    # 获取节点标签，用于分配颜色
    labels = nx.get_node_attributes(G, 'label')

    # 基于标签类别分配颜色
    unique_labels = list(set(labels.values()))
    color_map = {label: idx for idx, label in enumerate(unique_labels)}
    node_colors = [plt.cm.tab20(color_map[labels[node]] / len(unique_labels)) for node in G.nodes()]

    # 绘制节点
    nx.draw_networkx_nodes(G, pos, node_size=800, node_color=node_colors)

    # 绘制边和边的关系
    nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=15, edge_color='gray')
    edge_labels = nx.get_edge_attributes(G, 'relationship')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    # 绘制节点标签（支持中文）
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=10, font_color='black')
    plt.title("知识图谱可视化", fontsize=16)  # 中文标题
    plt.axis('off')
    return plt.gcf()

def query_and_visualize():
    connector = Neo4jConnector("bolt://localhost:7687", "neo4j", "G6669963.")
    data = connector.fetch_graph_data()
    G = build_graph(data)
    fig = visualize_graph(G)
    return fig

# Gradio 界面
interface = gr.Interface(
    fn=query_and_visualize,
    inputs=[],
    outputs=gr.Plot(label="知识图谱"),
    live=False,
    title="Neo4j 知识图谱可视化"
)

interface.launch()
