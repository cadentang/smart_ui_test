# -*- coding: utf-8 -*-
from utils.operation_mysql import Mysql

my = Mysql()


def get_top_navigations(env):
    """获取顶部导航有哪些栏目"""
    """env: ['test0', 'reg', 'stage']"""
    top_nav_sql = """SELECT b.id, b.title, b.show_pos, b.parent_id FROM haixue_cms.navigation b WHERE b.id in 
    (SELECT DISTINCT c.parent_id FROM haixue_cms.navigation c WHERE 
    c.parent_id in 
    (
    SELECT n.parent_id 
    FROM haixue_cms.navigation n WHERE n.show_pos=0 and n.state=5 and n.parent_id is not NULL
    ) and c.state=5);
    """
    top_second_nav_sql = """
    SELECT d.id, d.title, d.parent_id, d.template_id, t.view_tpl_key FROM haixue_cms.navigation d left join haixue_cms.content_template t on d.template_id=t.id WHERE d.parent_id in (
SELECT b.id FROM haixue_cms.navigation b WHERE b.id in 
    (SELECT DISTINCT c.parent_id FROM haixue_cms.navigation c WHERE 
    c.parent_id in 
    (
    SELECT n.parent_id 
    FROM haixue_cms.navigation n WHERE n.show_pos=0 and n.state=5 and n.parent_id is not NULL
    ) and c.state=5)
) and d.state = 5;"""

    my.connect_db()
    data = my.execute_sql(top_nav_sql)
    second_data = my.execute_sql(top_second_nav_sql)
    my.close_db()
    top_nav = {}
    for i in range(len(data)):
        tmp_dict = {}
        tmp_dict["top_id"] = data[i][0]
        tmp_dict["top_name"] = data[i][1]
        for j in range(len(second_data)):
            tmp1_dict = {}
            if data[i][0] == second_data[j][2]:
                tmp1_dict["second_nav_id"] = second_data[j][0]
                tmp1_dict["second_nav_name"] = second_data[j][1]
                tmp1_dict["second_nav_parent_id"] = second_data[j][2]
                tmp1_dict["second_nav_template_id"] = second_data[j][3]
                tmp1_dict["second_nav_view_tpl_key"] = second_data[j][4]
                tmp1_dict["second_nav_url"] = '/template/' + str(second_data[j][2]) + '/' + str(
                    second_data[j][0]) + '/' + second_data[j][4]
                tmp_dict["second_nav"] = tmp1_dict
        top_nav[i] = tmp_dict
    return top_nav


def get_bottom_navigations():
    """获取底部导航数据"""
    """获取顶部导航有哪些栏目"""
    bottom_nav_sql = """SELECT b.id, b.title, b.show_pos, b.parent_id FROM haixue_cms.navigation b WHERE b.id in 
        (SELECT DISTINCT c.parent_id FROM haixue_cms.navigation c WHERE 
        c.parent_id in 
        (
        SELECT n.parent_id 
        FROM haixue_cms.navigation n WHERE n.show_pos=1 and n.state=5 and n.parent_id is not NULL
        ) and c.state=5);
        """
    bottom_second_nav_sql = """
        SELECT d.id, d.title, d.parent_id, d.template_id, t.view_tpl_key FROM haixue_cms.navigation d left join haixue_cms.content_template t on d.template_id=t.id WHERE d.parent_id in (
    SELECT b.id FROM haixue_cms.navigation b WHERE b.id in 
        (SELECT DISTINCT c.parent_id FROM haixue_cms.navigation c WHERE 
        c.parent_id in 
        (
        SELECT n.parent_id 
        FROM haixue_cms.navigation n WHERE n.show_pos=1 and n.state=5 and n.parent_id is not NULL
        ) and c.state=5)
    ) and d.state = 5;"""

    my.connect_db()
    data = my.execute_sql(bottom_nav_sql)
    second_data = my.execute_sql(bottom_second_nav_sql)
    my.close_db()
    bottom_nav = {}
    for i in range(len(data)):
        tmp_dict = {}
        tmp_dict["top_id"] = data[i][0]
        tmp_dict["top_name"] = data[i][1]
        for j in range(len(second_data)):
            tmp1_dict = {}
            if data[i][0] == second_data[j][2]:
                tmp1_dict["second_nav_id"] = second_data[j][0]
                tmp1_dict["second_nav_name"] = second_data[j][1]
                tmp1_dict["second_nav_parent_id"] = second_data[j][2]
                tmp1_dict["second_nav_template_id"] = second_data[j][3]
                tmp1_dict["second_nav_view_tpl_key"] = second_data[j][4]
                tmp1_dict["second_nav_url"] = '/template/' + str(second_data[j][2]) + '/' + str(
                    second_data[j][0]) + '/' + second_data[j][4]
                tmp_dict["second_nav"] = tmp1_dict
        bottom_nav[i] = tmp_dict
    return bottom_nav


def get_sku_detail():
    """获取首页sku数据"""
    pass

if __name__ == "__main__":
    print(get_top_navigations())
