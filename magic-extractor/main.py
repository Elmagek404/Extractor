import argparse
import requests
from bs4 import BeautifulSoup ,XMLParsedAsHTMLWarning
import termcolor 
import pyfiglet
from tqdm import tqdm
import time
from urllib.parse import urljoin
import pyfiglet
from termcolor import colored
import uuid
import warnings 
import random
import datetime
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)


def red(s):return termcolor.colored(s,"red")
def green(s):return termcolor.colored(s,"green")
def yellow(s):return termcolor.colored(s,"yellow")
def blue(s):return termcolor.colored(s,"blue")
def deco(s):return pyfiglet.figlet_format(s,font="doom",width=80)
def banner(tool, author, channel):
    ascii = pyfiglet.figlet_format(tool, font="slant")
    print(colored("|==============================================================|", "cyan"))
    print(colored(ascii, "magenta"))
    print(colored("[+] Developed by: ", "cyan") + colored(author, "yellow"))
    print(colored("[+] YouTube     : ", "cyan") + colored(channel, "yellow"))
    print(colored("|==============================================================|", "cyan"))






def fetch_inputs(inputs,  output_file=None):
    for input_ in inputs:
        input_name = input_.get('name')
        input_value = input_.get('value')
        input_count=len(inputs)
        print(green(f"[+] Input Found:  name: {green(input_name) if input_name else yellow('empty name')} - Value:{green(input_value) if input_value else yellow('Empty Value')}"))
        if output_file:
            output_file.write(f"-name: {input_name if input_name else 'empty name'} - value: {input_value if input_value else 'Empty Value'}\n")
    print(green(f"Found {input_count}"))


def fetch_href(soap,base_url):
    a_tags=soap.find_all("a")
    if a_tags:
        for a_tag in a_tags:
            href=a_tag.get("href")
            if href:
                full_url = urljoin(base_url, href)
                print(green(f"[+] Extracted {full_url}"))
                with open("Automated_urls.txt","a") as fe:
                    fe.write(f"{full_url}\n")
    else: print(red("[-] Positive Crawling No Result Found"))

def fetch_js(scripts_, base_url="", time_out=5):
    for script in scripts_:
        script_src = script.get("src")
        if script_src:
            js_url = urljoin(base_url, script_src)
            try:
                js_response = requests.get(js_url, timeout=time_out)
                js_response.raise_for_status()
                script_name = js_url.replace("http://", "file_").replace("https://", "file_").replace("/", "_").split("?")[0]
                with open(f"{script_name}.js", "wb") as f:
                    f.write(js_response.content)
                print(green(f"[+] Saved JS File -> {script_name}.js"))
            except Exception as e:
                print(red(f"[-] Failed to download {js_url}: {e}"))

def fetch_froms(url,output_file=None,time_out=5,delay_=0):
    try:
        response=requests.get(url,timeout=time_out)
        time.sleep(delay_)
    except requests.RequestException:
        print(red(f"[-] Skipping {url} because it cause error"))
        return 
    soap=BeautifulSoup(response.text,"html.parser")
    forms=soap.find_all("form")
    form_count=len(forms)
    if forms:
        print(blue("[!] TIP: use option -o to save your result"))
        for form in forms:
            method=form.get('method')
            action=form.get('action')
            file_inputs = form.find_all("input",{"type":"file"})
            if file_inputs:
                print(green("[+] File upload inputs found"))
                for file_input in file_inputs:
                    name =file_input.get("name")
                    print(green(f"[+] File upload input Name: {name}"))
            if output_file:
                output_file.write(f"{url}: Found {form_count if form_count != 0 else form_count} Forms\n")
            print(green(f"Found Form\n- method {method}\n- action {action}"))
        print(f"[+]{green('Found')} {form_count} {green('forms')} ")
def main():
    banner("EXTRACTOR","Elm4g3k", "https://youtube.com/@Elmagek_403")
    parser=argparse.ArgumentParser(
        prog="extractor",
        description=yellow("Discover Your Target automatically"),
        usage='%(prog)s'+yellow('[options]')
        )

    parser.add_argument("-l",'--list',help=yellow("Path to the file contain URLs"))
    parser.add_argument("-t","--target-url")
    parser.add_argument("-o","--output",help=yellow("save result in file"))
    parser.add_argument("-f","--extract-file",help=yellow("Download javascript Files'"),action="store_true")
    parser.add_argument("--random-agents",help=yellow("send requests with random user-agent header"),action="store_true")
    parser.add_argument("--hide",help=yellow("Hide unnecessary output"),action="store_true")
    parser.add_argument("-H","--Header",help=yellow("Insert Custom HTTP header -H  key:value  "),action="append")
    parser.add_argument("--delay",help=yellow("Delay Between Requests "),type=int,default=0)
    parser.add_argument("--crawl",help=yellow("Crawling and Extracted Target URLs"),action="store_true")
    parser.add_argument("--time-out",help=yellow("ignore target after ammount of time default 5"),type=int,default=5)
    arg=parser.parse_args()
    try:
        url=arg.target_url if arg.target_url is not None else False
        input_file=open(arg.list,"r") if arg.list else None
        output_file=open(arg.output,"a") if arg.output is not None else False
        extract_file=arg.extract_file 
        delay_=arg.delay 
        time_out=arg.time_out
        crawling=arg.crawl 
        random_agent=arg.random_agents 
        hidden=arg.hide if arg.hide is not False else False 
        custome_header=arg.Header if arg.Header is not None else False
        if input_file:
            for i in tqdm(input_file.readlines()):
                i=i.strip("\n")
                if not i.startswith("https://"):
                    i="https://"+i
                try:
                    HEADERS = {}
                    if random_agent:
                        if custome_header:
                            for check in custome_header:
                                if ":" not in check :
                                    print(red("[-] invalid Header Format"))
                                    exit()
                                else:
                                    key,value=check.split(":",1)
                                    HEADERS[key.strip()]=value.strip()
                        if hidden:
                            with open("user-agents.txt","r")as f :
                                user_agent_file=f.readlines() 
                            user=random.choice(user_agent_file).strip()
                            HEADERS['User-Agent']=user
                            response=requests.get(i,timeout=time_out,headers=HEADERS)
                            time.sleep(delay_)
                            soap=BeautifulSoup(response.text,"html.parser")
                            if crawling:
                                fetch_href(soap,i)
                            inputs=soap.find_all("input")
                            if inputs:
                                fetch_inputs(inputs,output_file)
                            forms=soap.find_all("form")
                            if forms:
                                fetch_froms(i,output_file,time_out,delay_)
                            scripts_=soap.find_all("script")
                            if extract_file and scripts_:
                                fetch_js(scripts_,i,time_out)
                        else:
                            print(blue("[+] TIP to Hide user-agent From console use --hide"))
                            with open("user-agents.txt","r")as f :
                                user_agent_file=f.readlines() 
                            user=random.choice(user_agent_file).strip()
                            HEADERS={"User-Agent":user}
                            response=requests.get(i,timeout=time_out,headers=HEADERS)
                            print(yellow(f"[INF] done with {response.request.headers['user-agent']}"))
                            time.sleep(delay_)
                            soap=BeautifulSoup(response.text,"html.parser")
                            if crawling:
                                fetch_href(soap,i)
                            inputs=soap.find_all("input")
                            if inputs:
                                fetch_inputs(inputs,output_file)
                            forms=soap.find_all("form")
                            if forms:
                                fetch_froms(i,output_file,time_out,delay_)
                            scripts_=soap.find_all("script")
                            if extract_file and scripts_:
                                fetch_js(scripts_,i,time_out)
                    else:
                            response=requests.get(i,timeout=time_out)
                            time.sleep(delay_)
                            soap=BeautifulSoup(response.text,"html.parser")
                    if crawling:
                        fetch_href(soap,i)
                    inputs=soap.find_all("input")
                    if inputs:
                        fetch_inputs(inputs,output_file)
                    forms=soap.find_all("form")
                    if forms:
                        fetch_froms(i,output_file,time_out,delay_)
                    scripts_=soap.find_all("script")
                    if extract_file and scripts_:
                        fetch_js(scripts_,i,time_out)
                except requests.exceptions.RequestException :
                    print(red(f"[-] Skipping {i} due to error or not responding Try use --time-out "))
                    continue
                
                except KeyboardInterrupt: 
                    print(red("\nSee You Soon Hacker !"))
                    break
        elif url:
            try:
                HEADERS={}
                if random_agent:
                    if custome_header:
                        for head in custome_header:
                                try:
                                    key,value=head.split(":",1)
                                    HEADERS[key.strip()] = value.strip()
                                except ValueError:
                                    print(red("Invalid Header Format\n Header must be like key:value"))
                                    exit()
                    with open("user-agents.txt","r")as f :
                            user_agent_file=f.readlines() 
                            user=random.choice(user_agent_file).strip()
                            HEADERS['User-Agent']=user
                    url_response=requests.get(url,timeout=time_out,headers=HEADERS)
                    time.sleep(delay_)
                    if crawling:
                        soap=BeautifulSoup(url_response.text,"html.parser")
                        fetch_href(soap,url)
                    if extract_file:
                        soap=BeautifulSoup(url_response.text,"html.parser")
                        script_=soap.find_all("script")
                        fetch_js(script_,url,time_out)
                    soap=BeautifulSoup(url_response.text,"html.parser")
                    inputs=soap.find_all("inputs")
                    forms=soap.find_all("form")
                    if forms:
                        fetch_froms(url,output_file,time_out,delay_)
                else:
                    url_response=requests.get(url,timeout=time_out)
                    time.sleep(delay_)
                url_soap=BeautifulSoup(url_response.text,"html.parser")
                inputs=url_soap.find_all("input")
                scripts=url_soap.find_all("script")
                forms=url_soap.find_all("form")
                if extract_file:
                    if scripts:
                        script_=url_soap.find_all("script")
                        fetch_js(script_,url,time_out)
                    else:print(red(f"[-] Can't Found js Files"))
                if crawling:
                    fetch_href(url_soap,url)
                inputs=url_soap.find_all("input")
                if inputs:
                    fetch_inputs(inputs,output_file)
                if forms:
                    fetch_froms(url,output_file,time_out,delay_)
            except KeyboardInterrupt: 
                print(red("\nSee You Soon Hacker !!"))
            except requests.exceptions.RequestException: 
                print(red("The url You Entered Caused Error Please Check it and Try again"))
    except KeyboardInterrupt:
            print(red("\nSee You Soon Hacker !!"))
    except FileExistsError:
        print(red("The Filename Already Exist Please enter another one"))
    except FileNotFoundError:
        print(red("Error Happen Please Re-check the File "))

if __name__ == "__main__":
    main()
