import shutil
import os
from datetime import datetime
import re
from pathlib import Path
import sys

def FileModification(src,OriContent,NewContent):
    f = open(src, "r", encoding="utf-8")
    content = f.read()
    content = content.replace(OriContent, NewContent)
    f = open(src, "w", encoding="utf-8")
    f.write(content)
    f.close()

def FileBackup(path):
    nowtime = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_path = path + ".bak" + nowtime
    try:
        shutil.copy(path, backup_path)
        return True
    except:
        return False

def FilenameCheck(filename):
    if re.search(r'[^a-zA-Z0-9_]', filename) == None:
        return True
    else:
        return False

def GetOriFile():
    file_list = []
    for file in os.listdir("."):
        if file.endswith(".ioc"):
            file_list.append(file)
    if len(file_list) == 0:
        return False
    else:
        return file_list

def GetObjInfo(ObjPath):
    objInfo = {}
    f = open(ObjPath, "r", encoding="utf-8")
    content = f.read()
    for line in content.splitlines():
        if "ProjectManager.ProjectFileName" in line:
            objInfo[0] = line.strip()
        if "ProjectManager.ProjectName" in line:
            objInfo[1] = line.strip()
    return objInfo

def main():
    
    try:
        file_list = GetOriFile()
        print("输入\"\\q\"退出程序")
        if not file_list:
            print("当前目录下没有ioc文件，请将需要修改的ioc文件放在当前目录下")
            return
        else:
            print("当前目录下的ioc文件有：")
            for i, file in enumerate(file_list):
                print(f"{i + 1}. {file}")
    except Exception as e:
        print("发生错误：{}".format(e))
        return
    
    while True:
        try:
            choice = input("请输入要修改的文件编号：")
            if choice == "\\q":
                print("程序已退出")
                return
            choice = int(choice)
            if 1 <= choice <= len(file_list):
                ori_file = file_list[choice - 1]
                break
            else:
                print("输入的编号无效，请重新输入。")
        except ValueError:
            print("文件名只能包含字母、数字和下划线，请重新输入。")

    try:
        FileBackup(ori_file)
        print("文件备份成功，备份文件名为：{}.bak{}".format(ori_file, datetime.now().strftime("%Y%m%d%H%M%S")))
    except Exception as e:
        print("文件备份失败:{}".format(e))
        return
    
    while True:
        try:
            new_objname = input("请输入修改后的IOC工程名（只能包含字母、数字和下划线）：")
            if new_objname == "\\q":
                print("程序已退出")
                return
            if not FilenameCheck(new_objname):
                raise ValueError
            break
        except ValueError:
            print("文件名只能包含字母、数字和下划线，请重新输入。")

    try:
        obj_info = GetObjInfo(ori_file)
        FileModification(ori_file,obj_info[0], ("ProjectManager.ProjectFileName=" + new_objname + ".ioc"))
        FileModification(ori_file,obj_info[1], ("ProjectManager.ProjectName=" + new_objname))            
        os.rename(ori_file, new_objname + ".ioc")
        print("文件修改成功\n修改后的文件名为：{}.ioc".format(new_objname))
    except Exception as e:
        print("发生错误：{}".format(e))
        return

    try:
        if getattr(sys, 'frozen', False):
            current_dir = os.path.dirname(sys.executable)
        else:
            current_dir = os.path.dirname(os.path.abspath(__file__))
        build_dir = os.path.join(current_dir,"build")
        is_dir_exists = Path.exists(build_dir) and Path(build_dir).is_dir()
        if is_dir_exists:
            print("是否删除存在的文件夹{}？\ny:确认   n:取消".format(build_dir))
    except Exception as e:
        print("发生错误：{}".format(e))
        return
    
    while is_dir_exists:
        try:  
            user_input = input()
            if user_input != "y" and user_input != "n": 
                raise ValueError
            elif user_input == "n": 
                return
            else: 
                shutil.rmtree(build_dir)
                print("已成功删除文件夹{}".format(build_dir))
                break
        except ValueError:
            print("无效输入，请重试！")
        except Exception as e:
            print("发生错误：{}".format(e))
            return

    return

if __name__ == "__main__":
    main()
    input("回车以退出")