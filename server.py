#!/usr/bin/env python3
# 改进版 ARL MCP 服务器 - 支持环境变量配置
import os
import re
import requests
import tldextract
import urllib3
from mcp.server.fastmcp import FastMCP

# 从环境变量读取配置
ARL_URL = os.getenv("ARL_URL", "https://127.0.0.1:5192")
ARL_TOKEN = os.getenv("ARL_TOKEN", "")

if not ARL_TOKEN:
    raise ValueError("ARL_TOKEN 环境变量未设置！请在 MCP 配置中设置 ARL_TOKEN")

# 初始化 MCP 服务
mcp = FastMCP("ARL-Improved")

# 关闭 HTTPS 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 全局语言设置
REPLY_IN_CHINESE = True


@mcp.tool()
def extract_main_domain(RequestBody: str) -> str:
    """
    从原始 HTTP 数据包中提取主域名。

    参数：
    - RequestBody：包含 Host 字段的原始 HTTP 请求包

    返回：
    - 主域名，例如 'baidu.com'、'dzhsj.cn'。
    """
    match = re.search(r"Host:\s*([^\s:]+)", RequestBody)
    if not match:
        return "host not found"

    host = match.group(1).strip()
    extracted = tldextract.extract(host)
    if extracted.domain and extracted.suffix:
        return f"{extracted.domain}.{extracted.suffix}"
    return host


@mcp.tool()
def extract_domain_or_ip(text: str) -> str:
    """
    功能：根据输入文本判断并返回主域名、IP 地址或 IP 段。
    支持输入：域名字符串、IP 地址、IP 段（如 192.168.0.0/24）。
    注意：不解析完整 URL，只提取纯域名/IP。

    参数：
    - text: str，用户输入，如 www.baidu.com、1.1.1.1、192.168.0.0/24

    返回：
    - str：提取出的主域名或 IP 内容。
    """
    if "/" in text or re.match(r"^\d+\.\d+\.\d+\.\d+", text):
        return text.strip()
    else:
        extracted = tldextract.extract(text)
        if extracted.domain and extracted.suffix:
            return f"{extracted.domain}.{extracted.suffix}"
        return text


@mcp.tool()
def detect_reply_language(user_prompt: str) -> str:
    """
    根据用户输入自动检测语言，设置全局 REPLY_IN_CHINESE 标志。

    参数：
    - user_prompt: 用户输入的原始提示

    返回：
    - 确认设置的语言提示信息
    """
    global REPLY_IN_CHINESE
    if re.search(r"[\u4e00-\u9fff]", user_prompt):
        REPLY_IN_CHINESE = True
        return "已自动切换为中文回复模式。"
    else:
        REPLY_IN_CHINESE = False
        return "Auto-switched to English reply mode."


@mcp.tool()
def add_scan_task_and_prompt(
    name: str,
    target: str,
    domain_brute: bool = True,
    alt_dns: bool = True,
    dns_query_plugin: bool = True,
    arl_search: bool = True,
    port_scan: bool = True,
    skip_scan_cdn_ip: bool = True,
    site_identify: bool = True,
    search_engines: bool = True,
    site_spider: bool = True,
    file_leak: bool = True,
    findvhost: bool = True
) -> dict:
    """
    工具名称：add_scan_task_and_prompt
    功能：向 ARL 平台提交扫描任务，并向用户返回预计完成时间提示。
    """
    url = f"{ARL_URL}/api/task/"
    headers = {
        "Content-Type": "application/json",
        "Token": ARL_TOKEN,
        "Accept": "application/json"
    }
    payload = {
        "name": name,
        "target": target,
        "domain_brute_type": "big",
        "port_scan_type": "top1000",
        "domain_brute": domain_brute,
        "alt_dns": alt_dns,
        "dns_query_plugin": dns_query_plugin,
        "arl_search": arl_search,
        "port_scan": port_scan,
        "service_detection": False,
        "os_detection": False,
        "ssl_cert": False,
        "skip_scan_cdn_ip": skip_scan_cdn_ip,
        "site_identify": site_identify,
        "search_engines": search_engines,
        "site_spider": site_spider,
        "site_capture": False,
        "file_leak": file_leak,
        "findvhost": findvhost,
        "nuclei_scan": False
    }
    try:
        resp = requests.post(url, headers=headers, json=payload, verify=False, timeout=30)
        if resp.status_code != 200:
            return {
                "status": "fail",
                "reason": f"HTTP {resp.status_code}",
                "response": resp.text,
                "next_step": "请稍后手动查询任务状态"
            }

        data = resp.json()
        msg = (
            f"任务已成功创建：{name}\n"
            f"目标：{target}\n"
            f"预估子域名枚举完成时间：5-10 分钟\n"
            f"预估文件泄露检测完成时间：15-30 分钟\n"
            f"请稍后输入：查询任务状态 {name}\n"
            f"以检查扫描进度并决定是否提取数据。"
        )
        return {
            "status": "success",
            "task_info": data,
            "message": msg
        }

    except Exception as e:
        return {
            "status": "error",
            "reason": str(e),
            "next_step": "请稍后手动查询任务状态"
        }
@mcp.tool()
def add_scan_task_with_policy(
    name: str,
    target: str,
    policy_id: str,
    task_tag: str = "task"
) -> dict:
    """
    使用指定策略创建扫描任务

    参数：
    - name: 任务名称
    - target: 扫描目标（域名、IP或IP段）
    - policy_id: 策略ID（从list_policies获取）
    - task_tag: 任务类型标签，默认为"task"

    返回：
    - 任务创建结果和预计完成时间
    """
    url = f"{ARL_URL}/api/task/"
    headers = {
        "Content-Type": "application/json",
        "Token": ARL_TOKEN,
        "Accept": "application/json"
    }
    payload = {
        "name": name,
        "target": target,
        "policy_id": policy_id,
        "task_tag": task_tag
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, verify=False, timeout=30)
        if resp.status_code != 200:
            return {
                "status": "fail",
                "reason": f"HTTP {resp.status_code}",
                "response": resp.text
            }

        data = resp.json()
        msg = (
            f"任务已成功创建：{name}\n"
            f"目标：{target}\n"
            f"使用策略ID：{policy_id}\n"
            f"预估子域名枚举完成时间：5-10 分钟\n"
            f"预估完整扫描完成时间：30-60 分钟\n"
            f"请稍后输入：查询任务状态 {name}\n"
            f"以检查扫描进度并决定是否提取数据。"
        )
        return {
            "status": "success",
            "task_info": data,
            "message": msg
        }

    except Exception as e:
        return {
            "status": "error",
            "reason": str(e)
        }




@mcp.tool()
def list_all_tasks(page: int = 1, size: int = 10, status: str = "") -> dict:
    """
    列出所有任务
    
    参数：
    - page: 页码，默认为 1
    - size: 每页数量，默认为 10
    - status: 任务状态过滤，可选值：waiting, running, done, stop, error
    
    返回：
    - 任务列表，包含任务名称、目标、状态、开始时间、结束时间等信息
    """
    url = f"{ARL_URL}/api/task/"
    headers = {
        "Token": ARL_TOKEN,
        "Accept": "application/json"
    }
    params = {"page": str(page), "size": str(size)}
    
    if status:
        params["status"] = status
    
    try:
        resp = requests.get(url, headers=headers, params=params, verify=False, timeout=30)
        
        # 详细的错误信息
        if resp.status_code != 200:
            return {
                "status": "error",
                "reason": f"HTTP {resp.status_code}",
                "response_text": resp.text[:500],
                "url": url,
                "params": params
            }
        
        # 解析响应
        try:
            data = resp.json()
        except Exception as json_err:
            return {
                "status": "error",
                "reason": "JSON解析失败",
                "error": str(json_err),
                "response_text": resp.text[:500]
            }
        
        # 检查响应格式
        if not isinstance(data, dict):
            return {
                "status": "error",
                "reason": "响应格式错误，期望dict",
                "data_type": str(type(data)),
                "data": str(data)[:500]
            }
        
        items = data.get("items", [])
        total = data.get("total", 0)
        code = data.get("code", 200)
        
        # 检查 API 返回的状态码
        if code != 200:
            return {
                "status": "error",
                "reason": f"API返回错误码: {code}",
                "message": data.get("message", ""),
                "data": data
            }
        
        # 简化任务信息
        tasks = []
        for item in items:
            task_info = {
                "任务ID": item.get("_id", ""),
                "任务名": item.get("name", ""),
                "目标": item.get("target", ""),
                "状态": item.get("status", ""),
                "开始时间": item.get("start_date", ""),
                "结束时间": item.get("end_date", ""),
                "统计": item.get("statistic", {})
            }
            tasks.append(task_info)
        
        return {
            "status": "success",
            "total": total,
            "page": page,
            "size": size,
            "tasks": tasks,
            "message": f"共找到 {total} 个任务，当前显示第 {page} 页"
        }
        
    except requests.exceptions.Timeout:
        return {
            "status": "exception",
            "reason": "请求超时，请检查 ARL 服务是否正常运行"
        }
    except requests.exceptions.ConnectionError as e:
        return {
            "status": "exception",
            "reason": f"连接错误: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "exception",
            "reason": f"未知错误: {str(e)}",
            "error_type": type(e).__name__
        }


@mcp.tool()
def query_task_status(name: str) -> dict:
    """
    查询任务状态
    """
    url = f"{ARL_URL}/api/task/"
    headers = {"Token": ARL_TOKEN}
    params = {"name": name, "size": "1"}

    try:
        resp = requests.get(url, headers=headers, params=params, verify=False, timeout=10)
        if resp.status_code != 200:
            return {
                "state": "error",
                "reason": f"HTTP {resp.status_code}"
            }
        data = resp.json()
        items = data.get("items", [])
        if not items:
            return {
                "state": "not_found"
            }

        item = items[0]
        completed_services = [s.get("name") for s in item.get("service", []) if s.get("name")]

        status_map = {
            "子域名爆破": "arl_search" in completed_services,
            "IP收集": "port_scan" in completed_services,
            "站点探测": "site_spider" in completed_services,
            "文件泄露检测": "file_leak" in completed_services
        }

        all_done = all(status_map.values())
        if all_done:
            next_step = f"全部模块已完成！请输入：提取任务结果 {name} <主域名> 获取全部扫描数据。"
        else:
            next_step = f"部分模块尚未完成，请稍后再次查询。"

        return {
            "任务名": name,
            "子域名爆破": "已完成" if status_map["子域名爆破"] else "未完成",
            "IP收集": "已完成" if status_map["IP收集"] else "未完成",
            "站点探测": "已完成" if status_map["站点探测"] else "未完成",
            "文件泄露检测": "已完成" if status_map["文件泄露检测"] else "未完成",
            "next_step": next_step
        }
    except Exception as e:
        return {
            "state": "exception",
            "reason": str(e)
        }


@mcp.tool()
def query_and_extract(name: str, domain: str) -> dict:
    """
    提取任务结果
    """
    status = query_task_status(name)

    if status.get("state") in ["error", "exception", "not_found"]:
        return {
            "status": status.get("state"),
            "reason": status.get("reason", "任务未找到或出错"),
            "next_step": f"请检查任务名称或稍后重新调用"
        }

    extracted_data = {}
    pending_modules = []

    if status.get("子域名爆破") == "已完成":
        extracted_data["subdomains"] = get_all_subdomains(domain)
    else:
        pending_modules.append("子域名爆破")

    if status.get("IP收集") == "已完成":
        extracted_data["ips"] = query_ip_list(domain)
    else:
        pending_modules.append("IP收集")

    if status.get("站点探测") == "已完成":
        extracted_data["sites"] = query_site_list(domain)
    else:
        pending_modules.append("站点探测")

    if status.get("文件泄露检测") == "已完成":
        extracted_data["fileleaks"] = query_fileleak_list(domain)
    else:
        pending_modules.append("文件泄露检测")

    all_done = len(pending_modules) == 0

    return {
        "status": "done" if all_done else "running",
        "已完成模块": [k for k in ["子域名爆破", "IP收集", "站点探测", "文件泄露检测"] if k not in pending_modules],
        "未完成模块": pending_modules,
        "extracted_data": extracted_data,
        "next_step": "全部数据已提取，无需再次查询。" if all_done else f"以下模块尚未完成：{', '.join(pending_modules)}。"
    }


@mcp.tool()
def get_all_subdomains(domain: str) -> list[str]:
    """
    获取所有子域名
    """
    url = f"{ARL_URL}/api/domain/"
    headers = {"Token": ARL_TOKEN}
    page = 1
    size = 100
    subdomains = []

    try:
        while True:
            params = {"domain": domain, "page": page, "size": size}
            response = requests.get(url, headers=headers, params=params, verify=False, timeout=10)
            if response.status_code != 200:
                return [f"Request failed: {response.status_code}"]

            json_data = response.json()
            items = json_data.get("items", [])
            if not items:
                break

            subdomains += [item.get("domain") for item in items if item.get("domain")]

            if len(items) < size:
                break

            page += 1

        return list(set(subdomains))
    except Exception as e:
        return [f"Error: {str(e)}"]


@mcp.tool()
def query_ip_list(domain: str) -> list[str]:
    """
    获取IP列表
    """
    url = f"{ARL_URL}/api/ip/"
    headers = {"Token": ARL_TOKEN}
    page, size = 1, 100
    all_ips = []

    try:
        while True:
            params = {"domain": domain, "page": page, "size": size}
            resp = requests.get(url, headers=headers, params=params, verify=False, timeout=10)
            data = resp.json()
            items = data.get("items", [])
            all_ips.extend([item.get("ip") for item in items if item.get("ip")])
            if len(items) < size:
                break
            page += 1
        return all_ips
    except Exception as e:
        return [f"Error: {str(e)}"]


@mcp.tool()
def query_site_list(domain: str) -> list[str]:
    """
    获取站点列表
    """
    url = f"{ARL_URL}/api/site/"
    headers = {"Token": ARL_TOKEN}
    page, size = 1, 100
    all_sites = []

    try:
        while True:
            params = {"site": domain, "page": page, "size": size}
            resp = requests.get(url, headers=headers, params=params, verify=False, timeout=10)
            data = resp.json()
            items = data.get("items", [])
            all_sites.extend([item.get("site") for item in items if item.get("site")])
            if len(items) < size:
                break
            page += 1
        return all_sites
    except Exception as e:
        return [f"Error: {str(e)}"]


@mcp.tool()
def query_fileleak_list(domain: str) -> list[str]:
    """
    获取文件泄露列表
    """
    url = f"{ARL_URL}/api/fileleak/"
    headers = {"Token": ARL_TOKEN}
    page, size = 1, 100
    all_urls = []

    try:
        while True:
            params = {"url": domain, "page": page, "size": size}
            resp = requests.get(url, headers=headers, params=params, verify=False, timeout=10)
            data = resp.json()
            items = data.get("items", [])
            all_urls.extend([item.get("url") for item in items if item.get("url")])
            if len(items) < size:
                break
            page += 1
        return all_urls
    except Exception as e:
        return [f"Error: {str(e)}"]


@mcp.tool()
def delete_task(task_id: str) -> dict:
    """
    删除任务
    
    参数：
    - task_id: 任务ID（可以是单个ID或逗号分隔的多个ID）
    
    返回：
    - 删除结果
    """
    url = f"{ARL_URL}/api/task/delete/"
    headers = {
        "Content-Type": "application/json",
        "Token": ARL_TOKEN
    }
    
    # 支持单个或多个任务ID
    task_ids = [tid.strip() for tid in task_id.split(",")]
    payload = {"task_id": task_ids}
    
    try:
        resp = requests.post(url, headers=headers, json=payload, verify=False, timeout=10)
        if resp.status_code != 200:
            return {"status": "error", "reason": f"HTTP {resp.status_code}", "response": resp.text}
        
        data = resp.json()
        return {
            "status": "success",
            "message": f"成功删除 {len(task_ids)} 个任务",
            "deleted_ids": task_ids,
            "response": data
        }
    except Exception as e:
        return {"status": "exception", "reason": str(e)}


@mcp.tool()
def stop_task(task_id: str) -> dict:
    """
    停止正在运行的任务
    
    参数：
    - task_id: 任务ID
    
    返回：
    - 停止结果
    """
    url = f"{ARL_URL}/api/task/stop/{task_id}"
    headers = {"Token": ARL_TOKEN}
    
    try:
        resp = requests.get(url, headers=headers, verify=False, timeout=10)
        if resp.status_code != 200:
            return {"status": "error", "reason": f"HTTP {resp.status_code}", "response": resp.text}
        
        data = resp.json()
        return {
            "status": "success",
            "message": f"任务 {task_id} 已停止",
            "response": data
        }
    except Exception as e:
        return {"status": "exception", "reason": str(e)}


@mcp.tool()
def search_asset_domain(
    domain: str = "",
    scope_id: str = "",
    page: int = 1,
    size: int = 100
) -> dict:
    """
    搜索资产域名
    
    参数：
    - domain: 域名关键词
    - scope_id: 资产范围ID（可选）
    - page: 页码
    - size: 每页数量
    
    返回：
    - 域名列表及详细信息
    """
    url = f"{ARL_URL}/api/asset_domain/"
    headers = {"Token": ARL_TOKEN}
    params = {"page": page, "size": size}
    
    if domain:
        params["domain"] = domain
    if scope_id:
        params["scope_id"] = scope_id
    
    try:
        resp = requests.get(url, headers=headers, params=params, verify=False, timeout=10)
        if resp.status_code != 200:
            return {"status": "error", "reason": f"HTTP {resp.status_code}"}
        
        data = resp.json()
        items = data.get("items", [])
        
        domains = []
        for item in items:
            domains.append({
                "域名": item.get("domain", ""),
                "类型": item.get("type", ""),
                "解析值": item.get("record", ""),
                "IP列表": item.get("ips", []),
                "来源": item.get("source", "")
            })
        
        return {
            "status": "success",
            "total": data.get("total", 0),
            "domains": domains
        }
    except Exception as e:
        return {"status": "exception", "reason": str(e)}


@mcp.tool()
def search_asset_ip(
    ip: str = "",
    domain: str = "",
    scope_id: str = "",
    page: int = 1,
    size: int = 100
) -> dict:
    """
    搜索资产IP
    
    参数：
    - ip: IP地址关键词
    - domain: 关联域名
    - scope_id: 资产范围ID（可选）
    - page: 页码
    - size: 每页数量
    
    返回：
    - IP列表及端口信息
    """
    url = f"{ARL_URL}/api/asset_ip/"
    headers = {"Token": ARL_TOKEN}
    params = {"page": page, "size": size}
    
    if ip:
        params["ip"] = ip
    if domain:
        params["domain"] = domain
    if scope_id:
        params["scope_id"] = scope_id
    
    try:
        resp = requests.get(url, headers=headers, params=params, verify=False, timeout=10)
        if resp.status_code != 200:
            return {"status": "error", "reason": f"HTTP {resp.status_code}"}
        
        data = resp.json()
        items = data.get("items", [])
        
        ips = []
        for item in items:
            port_info = item.get("port_info", [])
            ports = [f"{p.get('port_id')}({p.get('service_name', 'unknown')})" for p in port_info]
            
            ips.append({
                "IP": item.get("ip", ""),
                "域名": item.get("domain", []),
                "端口": ports,
                "地理位置": item.get("geo_asn", {}).get("location", ""),
                "CDN": item.get("cdn_name", "")
            })
        
        return {
            "status": "success",
            "total": data.get("total", 0),
            "ips": ips
        }
    except Exception as e:
        return {"status": "exception", "reason": str(e)}


@mcp.tool()
def search_site(
    site: str = "",
    title: str = "",
    status: int = 0,
    scope_id: str = "",
    page: int = 1,
    size: int = 100
) -> dict:
    """
    搜索站点
    
    参数：
    - site: 站点URL关键词
    - title: 站点标题关键词
    - status: HTTP状态码
    - scope_id: 资产范围ID（可选）
    - page: 页码
    - size: 每页数量
    
    返回：
    - 站点列表及指纹信息
    """
    url = f"{ARL_URL}/api/site/"
    headers = {"Token": ARL_TOKEN}
    params = {"page": page, "size": size}
    
    if site:
        params["site"] = site
    if title:
        params["title"] = title
    if status > 0:
        params["status"] = status
    if scope_id:
        params["scope_id"] = scope_id
    
    try:
        resp = requests.get(url, headers=headers, params=params, verify=False, timeout=10)
        if resp.status_code != 200:
            return {"status": "error", "reason": f"HTTP {resp.status_code}"}
        
        data = resp.json()
        items = data.get("items", [])
        
        sites = []
        for item in items:
            sites.append({
                "站点": item.get("site", ""),
                "标题": item.get("title", ""),
                "状态码": item.get("status", 0),
                "指纹": item.get("finger", []),
                "IP": item.get("ip", []),
                "favicon": item.get("favicon", {}).get("hash", "")
            })
        
        return {
            "status": "success",
            "total": data.get("total", 0),
            "sites": sites
        }
    except Exception as e:
        return {"status": "exception", "reason": str(e)}


@mcp.tool()
def list_asset_scopes(page: int = 1, size: int = 100) -> dict:
    """
    列出所有资产范围/分组
    
    参数：
    - page: 页码
    - size: 每页数量
    
    返回：
    - 资产范围列表
    """
    url = f"{ARL_URL}/api/asset_scope/"
    headers = {"Token": ARL_TOKEN}
    params = {"page": page, "size": size}
    
    try:
        resp = requests.get(url, headers=headers, params=params, verify=False, timeout=10)
        if resp.status_code != 200:
            return {"status": "error", "reason": f"HTTP {resp.status_code}"}
        
        data = resp.json()
        items = data.get("items", [])
        
        scopes = []
        for item in items:
            scopes.append({
                "ID": item.get("_id", ""),
                "名称": item.get("name", ""),
                "范围": item.get("scope_array", []),
                "创建时间": item.get("date", "")
            })
        
        return {
            "status": "success",
            "total": data.get("total", 0),
            "scopes": scopes
        }
    except Exception as e:
        return {"status": "exception", "reason": str(e)}


@mcp.tool()
def create_asset_scope(name: str, scope: str) -> dict:
    """
    创建资产范围/分组
    
    参数：
    - name: 范围名称
    - scope: 范围内容（域名、IP或IP段，多个用换行符分隔）
    
    返回：
    - 创建结果
    """
    url = f"{ARL_URL}/api/asset_scope/"
    headers = {
        "Content-Type": "application/json",
        "Token": ARL_TOKEN
    }
    payload = {
        "name": name,
        "scope": scope
    }
    
    try:
        resp = requests.post(url, headers=headers, json=payload, verify=False, timeout=10)
        if resp.status_code != 200:
            return {"status": "error", "reason": f"HTTP {resp.status_code}", "response": resp.text}
        
        data = resp.json()
        return {
            "status": "success",
            "message": f"成功创建资产范围: {name}",
            "response": data
        }
    except Exception as e:
        return {"status": "exception", "reason": str(e)}


@mcp.tool()
def search_nuclei_result(url: str = "", page: int = 1, size: int = 100) -> dict:
    """
    搜索 Nuclei 漏洞扫描结果
    
    参数：
    - url: URL关键词
    - page: 页码
    - size: 每页数量
    
    返回：
    - 漏洞列表
    """
    api_url = f"{ARL_URL}/api/nuclei_result/"
    headers = {"Token": ARL_TOKEN}
    params = {"page": page, "size": size}
    
    if url:
        params["url"] = url
    
    try:
        resp = requests.get(api_url, headers=headers, params=params, verify=False, timeout=10)
        if resp.status_code != 200:
            return {"status": "error", "reason": f"HTTP {resp.status_code}"}
        
        data = resp.json()
        items = data.get("items", [])
        
        results = []
        for item in items:
            results.append({
                "URL": item.get("url", ""),
                "模板ID": item.get("template_id", ""),
                "模板名称": item.get("template_name", ""),
                "严重程度": item.get("severity", ""),
                "匹配内容": item.get("matched", ""),
                "提取内容": item.get("extracted_results", [])
            })
        
        return {
            "status": "success",
            "total": data.get("total", 0),
            "results": results
        }
    except Exception as e:
        return {"status": "exception", "reason": str(e)}


@mcp.tool()
def list_policies(page: int = 1, size: int = 100) -> dict:
    """
    列出所有扫描策略
    
    参数：
    - page: 页码
    - size: 每页数量
    
    返回：
    - 策略列表
    """
    url = f"{ARL_URL}/api/policy/"
    headers = {"Token": ARL_TOKEN}
    params = {"page": page, "size": size}
    
    try:
        resp = requests.get(url, headers=headers, params=params, verify=False, timeout=10)
        if resp.status_code != 200:
            return {"status": "error", "reason": f"HTTP {resp.status_code}"}
        
        data = resp.json()
        items = data.get("items", [])
        
        policies = []
        for item in items:
            policies.append({
                "ID": item.get("_id", ""),
                "名称": item.get("name", ""),
                "策略": item.get("policy", {})
            })
        
        return {
            "status": "success",
            "total": data.get("total", 0),
            "policies": policies
        }
    except Exception as e:
        return {"status": "exception", "reason": str(e)}


@mcp.tool()
def export_task_data(task_id: str) -> dict:
    """
    导出任务数据（获取任务的完整导出数据）
    
    参数：
    - task_id: 任务ID
    
    返回：
    - 任务的完整数据导出
    """
    url = f"{ARL_URL}/api/export/{task_id}"
    headers = {"Token": ARL_TOKEN}
    
    try:
        resp = requests.get(url, headers=headers, verify=False, timeout=30)
        if resp.status_code != 200:
            return {"status": "error", "reason": f"HTTP {resp.status_code}"}
        
        # 返回原始数据
        try:
            data = resp.json()
            return {
                "status": "success",
                "task_id": task_id,
                "data": data
            }
        except:
            return {
                "status": "success",
                "task_id": task_id,
                "data": resp.text
            }
    except Exception as e:
        return {"status": "exception", "reason": str(e)}


def main():
    print(f"[+] ARL MCP 改进版正在运行")
    print(f"[+] ARL URL: {ARL_URL}")
    print(f"[+] Token: {ARL_TOKEN[:10]}...")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
