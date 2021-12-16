from prettytable import PrettyTable
from PIL import Image, ImageDraw, ImageFont

tab = PrettyTable()
#tab.add_row(["select * from apr_appr_pool_dtl where CUST_NO='C2012102038045509285306597376';"])
# 设置表头
tab.field_names = ['ID', 'APPR_NO', 'LOAN_NO', 'CUST_NO', 'CUST_NAME', 'IS_VALID', 'INST_TIME', 'INST_USER_NO', 'UPDT_TIME', 'UPDT_USER_NO']
# 表格内容插入
tab.add_row(['061481c0fe5311eba70e0242109c82d9', '201001', 'L2012108168115481621656674304', 'C2012102038045509285306597376', 'TEST', '10000000', '2021-08-16 00:30:10', None, None, None])
tab.add_row(['187e4cd003bf11eca70e0242109c82d9', '201001', 'L2012108228117982149762523136', 'C2012102038045509285306597376', 'TEST', '10000000', '2021-08-22 22:06:23', None, None, None])
tab.add_row(['1f08ad0003bc11eca70e0242109c82d9', '201001', 'L2012108228117976791501414400', 'C2012102038045509285306597376', 'TEST', '10000000', '2021-08-22 21:45:05', None, None, None])
tab_info = str(tab)
space = 10

# PIL模块中，确定写入到图片中的文本字体
# windows
font = ImageFont.truetype('C:\\WINDOWS\\Fonts\\msyh.ttc', 40, encoding='utf-8')
# Image模块创建一个图片对象
im = Image.new('RGB',(10, 10),(0,0,0,0))
# ImageDraw向图片中进行操作，写入文字或者插入线条都可以
draw = ImageDraw.Draw(im, "RGB")
# 根据插入图片中的文字内容和字体信息，来确定图片的最终大小
img_size = draw.multiline_textsize(tab_info, font=font)
# 图片初始化的大小为10-10，现在根据图片内容要重新设置图片的大小
im_new = im.resize((img_size[0]+space*2, img_size[1]+space*2))
del draw
del im
draw = ImageDraw.Draw(im_new, 'RGB')
# 批量写入到图片中，这里的multiline_text会自动识别换行符
# python3
draw.multiline_text((space,space), tab_info, fill=(255,255,255), font=font)
im_new.save('12345.png', "png")
del draw
