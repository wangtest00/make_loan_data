import re,os
# 创建一个函数来替换文本
def replacetext(search_text, replace_text,path):
    # 以读写模式打开文件
    with open(path, 'r+') as f:
        # 读取文件数据并将其存储在文件变量中
        file = f.read()
        # 用文件数据中的字符串替换模式
        file = re.sub(search_text, replace_text, file)
        # 设置位置到页面顶部插入数据
        f.seek(0)
        # 在文件中写入替换数据
        f.write(file)
        # 截断文件大小
        f.truncate()
    # 返回“文本已替换”字符串
    print("文本已替换")

# 调用replacetext函数并打印返回的语句
replacetext("D:/Project", "/home/wangshuang/Downloads","/var/lib/jenkins/workspace/lanaplus_app_test/pubspec.yaml")
replacetext("F:/QUANT", "/home/wangshuang/Downloads/QUANT","/var/lib/jenkins/workspace/lanaplus_app_test/pubspec.yaml")

replacetext("D:/Project", "/home/wangshuang/Downloads/QUANT","/var/lib/jenkins/workspace/lanaplus_app_test/android/key.properties")
replacetext("F:/QUANT", "/home/wangshuang/Downloads/QUANT","/var/lib/jenkins/workspace/lanaplus_app_test/android/key.properties")

os.system('rm /var/lib/jenkins/workspace/lanaplus_app_test/lib/lana_config.dart')
os.system('cp /home/wangshuang/Downloads/QUANT/lana_config.dart /var/lib/jenkins/workspace/lanaplus_app_test/lib/')
print("tihuan success for lana_config.dart")
os.system('rm /var/lib/jenkins/workspace/lanaplus_app_test/pubspec.lock')
os.system('cp /home/wangshuang/Downloads/QUANT/pubspec.lock /var/lib/jenkins/workspace/lanaplus_app_test/')
print("tihuan success for pubspec.lock")