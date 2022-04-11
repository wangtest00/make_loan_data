from pyecharts import Bar
fruits = ['贷前“通过”','贷前“待提现”','正常贷款','逾期贷款','展期结清贷款','已结清贷款']
sales =[25,16,78,17108,65,44425]
bar = Bar('水果销售情况')
bar.add('',fruits,sales,is_stack=True)
bar.render()
# fruits = ['贷前“通过”','贷前“待提现”','正常贷款','逾期贷款','展期结清贷款','已结清贷款']
# shop1_sales = [25,16,78,17108,65,44425]
# pie = Pie('饼图示例')
# pie.add('芝麻饼', fruits, shop1_sales, is_label_show=True)
# pie.show_config()
# pie.render()
