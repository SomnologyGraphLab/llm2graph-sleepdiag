from neo4j import GraphDatabase
from wordcloud import WordCloud
import os

class Neo4jQueryService:
    def __init__(self):
        # 配置 Neo4j 数据库连接
        self.uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.username = os.getenv("NEO4J_USERNAME", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD", "G6669963.")
        self.driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))
    
    def execute_query(self, query, params=None):
        """执行查询的通用方法"""
        try:
            with self.driver.session() as session:
                return session.run(query, params or {}).data()
        except Exception as e:
            print(f"Query execution failed: {str(e)}")
            return None
    
    def get_entity_types(self, limit=50):
        """
        获取所有实体类型
        :param limit: 返回结果的最大数量
        :return: (status, data) 
                 status: "success" 或 "error"
                 data: 成功时为实体类型列表，失败时为错误消息
        """
        query = "MATCH (n) RETURN DISTINCT labels(n) AS entityType LIMIT $limit"
        result = self.execute_query(query, {"limit": limit})
        
        if result is None:
            return ("error", "Database query failed")
            
        try:
            entity_types = [record['entityType'][0] for record in result]
            return ("success", entity_types)
        except Exception as e:
            return ("error", str(e))
    
    def get_relationship_types(self, limit=50):
        """
        获取所有关系类型
        :param limit: 返回结果的最大数量
        :return: (status, data)
                 status: "success" 或 "error"
                 data: 成功时为关系类型列表，失败时为错误消息
        """
        query = "MATCH ()-[r]->() RETURN DISTINCT type(r) AS relationshipType LIMIT $limit"
        result = self.execute_query(query, {"limit": limit})
        
        if result is None:
            return ("error", "Database query failed")
            
        try:
            relationship_types = [record['relationshipType'] for record in result]
            return ("success", relationship_types)
        except Exception as e:
            return ("error", str(e))
    
    def health_check(self):
        """检查数据库连接是否正常"""
        try:
            self.execute_query("RETURN 1")
            return True
        except Exception:
            return False
    
    def close(self):
        """关闭数据库连接"""
        self.driver.close()


# 关闭连接
def create_wordcloud_E():
    """
    创建实体类型词云
    :param service: Neo4jQueryService 实例
    :return: 生成的图片路径
    """
    service = Neo4jQueryService()
    status, data = service.get_entity_types()
    
    if status == "success":
        text = " ".join(data)
        print("Entities text:", text)
    else:
        print("Error fetching entity data:", data)
        text = ""
    font_path = os.path.join(os.path.dirname(__file__), 'simhei.ttf')  # 替换为实际字体路径

    wc = WordCloud(
        font_path=font_path,
        width=800,
        height=400,
        background_color='white',
        colormap='viridis',
        max_words=200,
        min_font_size=10,
        max_font_size=100,
        random_state=42,
        contour_color='black',
        contour_width=1,
        relative_scaling=0.5
    ).generate(text)
    
    output_path = 'img_E.jpg'
    wc.to_file(output_path)
    return output_path

def create_wordcloud_R():
    """
    创建关系类型词云
    :param service: Neo4jQueryService 实例
    :return: 生成的图片路径
    """
    service = Neo4jQueryService()
    status, data = service.get_relationship_types()
    
    if status == "success":
        text = " ".join(data)
        print("Relationships text:", text)
    else:
        print("Error fetching relationship data:", data)
        text = ""
    font_path = os.path.join(os.path.dirname(__file__), 'simhei.ttf')  # 替换为实际字体路径
    wc = WordCloud(
        font_path=font_path, 
        width=800,
        height=400,
        background_color='white',
        colormap='viridis',
        max_words=200,
        min_font_size=10,
        max_font_size=100,
        random_state=42,
        contour_color='black',
        contour_width=1,
        relative_scaling=0.5
    ).generate(text)
    
    output_path = 'img_R.jpg'
    wc.to_file(output_path)
    return output_path


