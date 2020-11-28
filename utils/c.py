# -*- coding: utf-8 -*-
from utils.operation_mysql import Mysql

my = Mysql()


def get_top_navigations():
    """获取顶部导航有哪些栏目"""

    sql_list = []
    for i in range(10000):
        pra_key = 298546810 + i
        top_nav_sql = """
        INSERT INTO `wealth_activity`.`customer_prize` (
`activity_prize_id`,
`activity_id`,
`prize_id`,
`order_no`,
`order_id`,
`prize_type`,
`status`,
`type`,
`amount`,
`customer_id`,
`mobile`,
`platform`,
`use_start`,
`use_end`,
`ext`,
`creator_id`,
`creator_name`,
`create_time`,
`lock_time`,
`use_time`,
`expire_time`,
`update_time`,
`deleted`,
`parent_id` 
)
VALUES
	(
	2462,
	464,
	902,
	NULL,
	NULL,
	11,
	0,
	1,
	500.00,
	11577427,
	'17955550001',
	'5',
	'2020-10-28 00:00:00',
	'2020-12-27 23:59:59',	'{\"activityName\":\"2020压测商品优惠券\",\"couponName\":\"2020性能下单可用优惠券500\",\"limitMoney\":600.00,\"supportGoodsIdList\":[289000,288500]}',
	NULL,
	NULL,
	'2020-10-28 17:45:04',
	NULL,
	NULL,
	NULL,
	'2020-10-28 17:45:04',
	0,
NULL 
	);
        """
        sql_list.append(top_nav_sql)
        print(top_nav_sql)

    my.connect_db()
    for i in range(len(sql_list)):
        my.execute_sql(top_nav_sql)
    my.close_db()



if __name__ == "__main__":
    get_top_navigations()


