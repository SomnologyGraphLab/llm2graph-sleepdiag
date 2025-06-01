# from pyvis.network import Network
# from neo4j import GraphDatabase
# import gradio as gr

# # 连接到 Neo4j 数据库
# uri = "bolt://localhost:7687"  # 替换为你的 Neo4j URI
# username = "neo4j"             # 替换为你的 Neo4j 用户名
# password = "G6669963."     # 替换为你的 Neo4j 密码
# driver = GraphDatabase.driver(uri, auth=(username, password))

# # 从 Neo4j 查询数据并生成知识图谱的 HTML
# def generate_graph_html():
#     net = Network(height="750px", width="100%", directed=True)

#     # 从 Neo4j 数据库中查询节点和边
#     with driver.session() as session:
#         result = session.run("MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 50")
#         for record in result:
#             # 获取节点和边的属性
#             node_a = record["n"].get("name", "Unnamed Node")  # 如果 name 不存在，使用默认值
#             node_b = record["m"].get("name", "Unnamed Node")
#             relationship = record["r"].type

#             # 添加节点和边到网络图
#             net.add_node(node_a, label=str(node_a))
#             net.add_node(node_b, label=str(node_b))
#             net.add_edge(node_a, node_b, title=relationship)

#     # 返回 HTML 字符串
#     html_output = net.generate_html()
#     return html_output

# # Gradio 回调函数
# def display_graph():
#     graph_html = generate_graph_html()
#     print(graph_html)
#     return graph_html

# with gr.Blocks() as demo:
#     gr.Markdown("# Neo4j Knowledge Graph Viewer")
#     # 直接使用 gr.HTML 来显示 HTML 内容
#     graph_html = display_graph()  # 调用函数获取 HTML 内容
#     gr.HTML(str(graph_html))  # 使用 gr.HTML 组件显示 HTML 内容

# # 启动 Gradio 应用
# demo.launch()
import gradio as gr

# 定义返回 HTML 的函数
def display_graph():
    # 将 HTML 数据直接以字符串形式返回
    html_data = """
    <html>
        <head>
            <meta charset="utf-8">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/dist/vis-network.min.css" integrity="sha512-WgxfT5LWjfszlPHXRmBWHkV2eceiWTOBvrKCNbdgDYTHrT2AeLCGbF4sZlZw3UMN3WtL0tGUoIAKsu8mllg/XA==" crossorigin="anonymous" referrerpolicy="no-referrer" />
            <script src="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/dist/vis-network.min.js" integrity="sha512-LnvoEWDFrqGHlHmDD2101OrLcbsfkrzoSpvtSQtxK3RMnRV0eOkhhBN2dXHKRrUU8p2DGRTk35n4O8nWSVe1mQ==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
            <style type="text/css">
                #mynetwork {
                    width: 100%;
                    height: 750px;
                    background-color: #ffffff;
                    border: 1px solid lightgray;
                }
            </style>
        </head>
        <body>
            <div id="mynetwork"></div>
            <script type="text/javascript">
                var nodes = new vis.DataSet([
                    {"id": "1", "label": "Node 1"},
                    {"id": "2", "label": "Node 2"},
                    {"id": "3", "label": "Node 3"}
                ]);

                var edges = new vis.DataSet([
                    {"from": "1", "to": "2"},
                    {"from": "2", "to": "3"},
                    {"from": "3", "to": "1"}
                ]);

                var container = document.getElementById('mynetwork');
                var data = {nodes: nodes, edges: edges};
                var options = {
                    physics: {enabled: true}
                };
                var network = new vis.Network(container, data, options);
            </script>
        </body>
    </html>
    """
    return html_data

# 构建 Gradio 界面
with gr.Blocks() as demo:
    gr.Markdown("# Knowledge Graph Viewer")
    gr.HTML(display_graph())  # 直接嵌入 HTML 数据

# 启动 Gradio 服务
demo.launch()
