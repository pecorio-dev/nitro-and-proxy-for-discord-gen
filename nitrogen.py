import os
import random
import string
import ctypes
import asyncio
import aiohttp
import json
import logging
import re
import time
from concurrent.futures import ThreadPoolExecutor
from queue import PriorityQueue
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.prompt import Prompt, IntPrompt
from bs4 import BeautifulSoup
import ipaddress
import heapq
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style

# Initialize rich console and logging
console = Console()
logging.basicConfig(filename='nitrogen.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Global variables
seen_proxies = set()
working_proxies = PriorityQueue()
blacklisted_proxies = set()
proxy_scores = {}
start_time = time.time()

# CLI styling for prompt_toolkit (galactic theme)
prompt_style = Style.from_dict({
    'prompt': 'cyan bold',
    '': 'yellow',
})

# Galactic pixel art logo for Nitrogen by Pecorio
GALACTIC_LOGO = """
[bold yellow]
       🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟
       ☄️       NITROGEN BY PECORIO       ☄️
       🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟
       ✨          GALACTIC EDITION          ✨
       ╔══════════════════════════════════════╗
       ║  ███╗   ██╗██╗████████╗██████╗   █████╗  ║
       ║  ████╗  ██║██║╚══██╔══╝██╔══██╗ ██╔══██╗ ║
       ║  ██╔██╗ ██║██║   ██║   ██████╔╝ ██║  ██║ ║
       ║  ██║╚██╗██║██║   ██║   ██╔══██╗ ██╔══██║ ║
       ║  ██║ ╚████║██║   ██║   ██║  ██║ ██║  ██║ ║
       ║  ╚═╝  ╚═══╝╚═╝   ╚═╝   ╚═╝  ╚═╝╚ █████╚═╝ ║
       ╚══════════════════════════════════════╝
       🌌 [cyan]POWERED BY COSMIC PROXIES[/cyan] 🌌
       ✨ [cyan]v1.0 - SUPERNOVA RELEASE[/cyan] ✨
       🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟
[/bold yellow]
"""

# Console title setter
def set_title(title):
    if os.name == "nt":
        try:
            ctypes.windll.kernel32.SetConsoleTitleW(title)
        except:
            pass
    else:
        try:
            os.system(f"echo -ne '\033]0;{title}\007'")
        except:
            pass

# Display title with galactic logo
def display_title():
    console.clear()
    console.print(Panel(
        GALACTIC_LOGO + "\n[white]Generate and check Discord Nitro codes with advanced proxy management[/white]",
        title="🌟 Nitrogen by Pecorio 🌟",
        border_style="yellow",
        expand=False
    ))

# Load configuration
def load_config():
    default_config = {
        "proxy_sources": [
            {"name": "ProxyScrape", "type": "api", "url": "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http,socks4,socks5&timeout=10000&country=all&ssl=all&anonymity=all"},
            {"name": "OpenProxy", "type": "api", "url": "https://api.openproxy.space/lists/http"},
            {"name": "FreeProxyList", "type": "html", "url": "https://free-proxy-list.net/", "selector": "table.table tbody tr"},
            {"name": "SpysOne", "type": "html", "url": "http://spys.one/en/http-proxy-list/", "selector": "table tr"},
            {"name": "ProxyListDownload", "type": "api", "url": "https://www.proxy-list.download/api/v1/get?type=http,socks5"},
            {"name": "HideMyName", "type": "html", "url": "https://hidemy.name/en/proxy-list/", "selector": "table tbody tr"},
            {"name": "FreeProxyWorld", "type": "html", "url": "https://www.freeproxy.world/", "selector": "table tbody tr"},
            {"name": "ProxyNova", "type": "html", "url": "https://www.proxynova.com/proxy-server-list/", "selector": "table#tbl_proxy_list tbody tr"},
            {"name": "SSLProxies", "type": "html", "url": "https://www.sslproxies.org/", "selector": "table.table tbody tr"},
            {"name": "GeoNode", "type": "api", "url": "https://proxylist.geonode.com/api/proxy-list?limit=50&page=1&sort_by=lastChecked&sort_type=desc&protocols=http,socks5"},
            {"name": "ProxyScan", "type": "api", "url": "https://www.proxyscan.io/api/proxy?type=http,socks5&limit=100"},
            {"name": "CheckerProxy", "type": "api", "url": "https://checkerproxy.net/api/archive"},
            {"name": "ProxyListPlus", "type": "html", "url": "https://list.proxylistplus.com/Fresh-HTTP-Proxy-List", "selector": "table tbody tr"},
            {"name": "SocksProxy", "type": "html", "url": "https://www.socks-proxy.net/", "selector": "table tbody tr"},
            {"name": "ProxyMesh", "type": "api", "url": "https://proxymesh.com/free-proxy-list/"},
            {"name": "Proxy11", "type": "api", "url": "https://proxy11.com/api/proxy.txt?type=http,socks5"},
            {"name": "AdvancedName", "type": "html", "url": "https://advanced.name/freeproxy", "selector": "table tbody tr"},
            {"name": "ProxyDB2", "type": "html", "url": "https://proxydb.net/?protocol=http&protocol=socks5", "selector": "table tbody tr"},
            {"name": "ProxyListIO", "type": "api", "url": "https://proxylist.io/api/proxies?protocol=http,socks5"},
            {"name": "FreeProxyCZ2", "type": "html", "url": "http://free-proxy.cz/en/proxylist/country/ALL/socks5/ping/all", "selector": "table#proxy_list tbody tr"},
            {"name": "Proxifly", "type": "api", "url": "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/all/data.txt"},
            {"name": "ClarkTM", "type": "api", "url": "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt"},
            {"name": "TheSpeedX", "type": "api", "url": "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"},
            {"name": "Vakhov", "type": "api", "url": "https://vakhov.github.io/fresh-proxy-list/http.txt"},
            {"name": "Monosans", "type": "api", "url": "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt"},
            {"name": "ShiftyTR", "type": "api", "url": "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt"},
            {"name": "Yemixzy", "type": "api", "url": "https://raw.githubusercontent.com/yemixzy/proxy-list/main/http.txt"},
            {"name": "Mishakorzik", "type": "api", "url": "https://raw.githubusercontent.com/mishakorzik/Free-Proxy/main/Proxy.txt"},
            {"name": "Dpangestuw", "type": "api", "url": "https://raw.githubusercontent.com/dpangestuw/Free-Proxy/main/http.txt"},
            {"name": "ProxyDaily", "type": "api", "url": "https://proxydaily.com/api/free-proxy-list?protocol=http,socks5"},
            {"name": "CoolProxy", "type": "api", "url": "https://www.cool-proxy.net/proxies.json"},
            {"name": "MyProxy", "type": "html", "url": "https://www.my-proxy.com/free-proxy-list.html", "selector": "table tbody tr"},
            {"name": "FreeProxyListCC", "type": "html", "url": "https://freeproxylist.cc/", "selector": "table tbody tr"},
            {"name": "ProxyLists", "type": "api", "url": "http://www.proxylists.net/http_highanon.txt"},
            {"name": "GatherProxy", "type": "html", "url": "http://www.gatherproxy.com/proxylist/anonymity/?t=Elite", "selector": "table tbody tr"},
            {"name": "ProxyRoid", "type": "api", "url": "https://proxyroid.net/api/proxies?protocol=http,socks5"},
            {"name": "NordVPN", "type": "html", "url": "https://nordvpn.com/free-proxy-list/", "selector": "table tbody tr"},
            {"name": "Proxy4Free", "type": "html", "url": "https://www.proxy4free.com/en/proxy-list/", "selector": "table tbody tr"},
            {"name": "AliveProxy", "type": "html", "url": "http://aliveproxy.com/high-anonymity-proxy-list/", "selector": "table tbody tr"},
            {"name": "FreeProxyAPI", "type": "api", "url": "http://pubproxy.com/api/proxy?limit=20&format=txt&type=http"},
            {"name": "GetFreeProxy", "type": "api", "url": "https://getfreeproxy.com/api/proxies?protocol=http,socks5"},
            {"name": "ProxyListMe", "type": "html", "url": "https://proxylist.me/", "selector": "table tbody tr"},
            {"name": "ProxyServerList", "type": "html", "url": "https://www.proxyserverlist24.top/", "selector": "table tbody tr"},
            {"name": "FreeProxyOnline", "type": "html", "url": "https://freeproxyonline.com/", "selector": "table tbody tr"},
            {"name": "ProxyListOrg", "type": "html", "url": "https://proxy-list.org/english/index.php", "selector": "table tbody tr"},
            {"name": "ProxyHub", "type": "html", "url": "https://proxyhub.me/en/all-http-proxy-list.html", "selector": "table tbody tr"},
            {"name": "FreeProxyCZ", "type": "html", "url": "http://free-proxy.cz/en/proxylist/country/ALL/http/ping/all", "selector": "table#proxy_list tbody tr"}
        ],
        "user_agents": [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
        ],
        "default_ports": [80, 8080, 3128, 8888, 1080]
    }
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        config = default_config
        with open("config.json", "w") as f:
            json.dump(config, f, indent=4)
    return config

async def fetch_url(session, url, headers=None, proxy=None, timeout=5):
    """Fetch URL with aiohttp"""
    try:
        async with session.get(url, headers=headers, proxy=proxy, timeout=timeout) as response:
            if response.status == 200 and response.content_type in ["application/json", "text/plain"]:
                return await response.text()
            return None
    except Exception as e:
        logging.error(f"Failed to fetch {url}: {str(e)}")
        return None

async def check_anonymity(proxy, session):
    """Check proxy anonymity level"""
    try:
        headers = {"User-Agent": random.choice(load_config()["user_agents"])}
        async with session.get("http://httpbin.org/ip", proxy=f"http://{proxy}", headers=headers, timeout=5) as response:
            if response.status == 200:
                data = await response.json()
                proxy_ip = proxy.split(":")[0]
                return "elite" if data["origin"] == proxy_ip else "anonymous"
        return "transparent"
    except:
        return "transparent"

async def scrape_proxies_source(source, session):
    """Scrape proxies from a single source"""
    proxies = set()
    try:
        if source["type"] == "api":
            text = await fetch_url(session, source["url"])
            if text:
                if source["name"] in ["OpenProxy", "GeoNode", "CheckerProxy"]:
                    try:
                        data = json.loads(text)
                        for proxy in (data if source["name"] == "CheckerProxy" else data.get("data", data)):
                            proxy_str = proxy.get("addr") or f"{proxy['ip']}:{proxy['port']}"
                            if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}$", proxy_str) and proxy_str not in seen_proxies:
                                proxies.add(proxy_str)
                                seen_proxies.add(proxy_str)
                    except json.JSONDecodeError:
                        logging.error(f"{source['name']}: Invalid JSON response")
                else:
                    for line in text.splitlines():
                        proxy_str = line.strip()
                        if proxy_str and re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}$", proxy_str) and proxy_str not in seen_proxies:
                            proxies.add(proxy_str)
                            seen_proxies.add(proxy_str)
        elif source["type"] == "html":
            headers = {"User-Agent": random.choice(load_config()["user_agents"])}
            text = await fetch_url(session, source["url"], headers)
            if text:
                soup = BeautifulSoup(text, 'html.parser')
                for row in soup.select(source.get("selector", "table tbody tr")):
                    cols = row.find_all("td")
                    if len(cols) >= 2:
                        proxy = f"{cols[0].text.strip()}:{cols[1].text.strip()}"
                        if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}$", proxy) and proxy not in seen_proxies:
                            proxies.add(proxy)
                            seen_proxies.add(proxy)
        console.print(f"[green]✔ Scraped {len(proxies)} unique proxies from {source['name']}[/green]")
        return proxies
    except Exception as e:
        logging.error(f"Failed to scrape {source['name']}: {str(e)}")
        console.print(f"[red]✘ Failed to scrape {source['name']}: {str(e)}[/red]")
        return set()

async def scrape_proxies(config, num_proxies=500):
    """Scrape proxies from all sources"""
    proxies = set()
    async with aiohttp.ClientSession() as session:
        tasks = [scrape_proxies_source(source, session) for source in config["proxy_sources"]]
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeRemainingColumn(),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Scraping proxies...", total=len(tasks))
            for future in asyncio.as_completed(tasks):
                result = await future
                proxies.update(result)
                progress.advance(task, advance=1/len(tasks)*100)
    
    if num_proxies != "all":
        proxies = list(proxies)[:num_proxies]
    else:
        proxies = list(proxies)
    console.print(f"[bold green]✔ Total scraped unique proxies: {len(proxies)}[/bold green]")
    return proxies

def generate_random_ips(num_ips=100, ports=None):
    """Generate random IPv4 addresses"""
    if not ports:
        ports = load_config()["default_ports"]
    proxies = []
    attempts = 0
    max_attempts = num_ips * 2
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeRemainingColumn(),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Generating IPs...", total=num_ips)
        while len(proxies) < num_ips and attempts < max_attempts:
            ip = str(ipaddress.IPv4Address(random.randint(0, 2**32 - 1)))
            port = random.choice(ports)
            proxy = f"{ip}:{port}"
            if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}$", proxy) and proxy not in seen_proxies:
                proxies.append(proxy)
                seen_proxies.add(proxy)
                progress.advance(task)
            attempts += 1
    console.print(f"[bold green]✔ Generated {len(proxies)} unique random IPs[/bold green]")
    return proxies

def load_pre_scraped_proxies(file_path="pre_scraped_proxies.txt"):
    """Load user-provided proxies"""
    proxies = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                proxy = line.strip()
                if proxy and re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}$", proxy) and proxy not in seen_proxies:
                    proxies.append(proxy)
                    seen_proxies.add(proxy)
        console.print(f"[bold green]✔ Loaded {len(proxies)} unique pre-scraped proxies[/bold green]")
    except FileNotFoundError:
        console.print(f"[yellow]⚠ {file_path} not found[/yellow]")
    return proxies

async def test_proxy(proxy, config):
    """Test proxy with thorough verification"""
    headers = {"User-Agent": random.choice(config["user_agents"])}
    proxy_url = f"http://{proxy}"
    start_time = time.time()
    success_count = 0
    tests = [
        ("https://discord.com/api/v9/entitlements/gift-codes/test", [400, 429, 401]),
        ("https://discord.com/api/v9/users/@me", [401, 429]),
        ("http://httpbin.org/ip", [200]),
        ("https://api.ipify.org?format=json", [200])
    ]
    max_retries = 2

    for attempt in range(max_retries):
        try:
            async with aiohttp.ClientSession() as session:
                for url, valid_statuses in tests:
                    try:
                        async with session.get(url, proxy=proxy_url, headers=headers, timeout=5) as response:
                            response_time = time.time() - start_time
                            if response.status in valid_statuses and response.content_type in ["application/json", "text/plain"]:
                                success_count += 1
                                if url == "http://httpbin.org/ip":
                                    anonymity = await check_anonymity(proxy, session)
                                else:
                                    anonymity = "anonymous"  # Default for non-httpbin tests
                            else:
                                console.print(f"[yellow]⚠ Proxy {proxy} failed test {url} (Status: {response.status})[/yellow]")
                    except Exception as e:
                        console.print(f"[yellow]⚠ Proxy {proxy} failed test {url} ({str(e)})[/yellow]")
                        if attempt == max_retries - 1:
                            blacklisted_proxies.add(proxy)
                            return None, 0
                if success_count >= 3:  # Require 3/4 tests to pass
                    score = (success_count / len(tests)) * (1.0 / (response_time + 0.1)) * (2 if anonymity == "elite" else 1.5 if anonymity == "anonymous" else 1)
                    proxy_scores[proxy] = score
                    console.print(f"[green]✔ Working proxy: {proxy} (Score: {score:.2f}, Anonymity: {anonymity})[/green]")
                    return proxy, score
                else:
                    console.print(f"[yellow]⚠ Proxy {proxy} passed {success_count}/{len(tests)} tests, retrying[/yellow]")
                    await asyncio.sleep(0.5)
        except Exception as e:
            console.print(f"[red]✘ Proxy {proxy} failed all tests ({str(e)})[/red]")
            blacklisted_proxies.add(proxy)
            return None, 0
    blacklisted_proxies.add(proxy)
    console.print(f"[red]✘ Proxy {proxy} failed after {max_retries} attempts[/red]")
    return None, 0

async def verify_proxies_async(proxies, config, verify_threads=10):
    """Verify proxies asynchronously with limited concurrency"""
    tasks = [test_proxy(proxy, config) for proxy in proxies if proxy not in blacklisted_proxies]
    results = []
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeRemainingColumn(),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Verifying proxies...", total=len(tasks))
        for future in asyncio.as_completed(tasks):
            proxy, score = await future
            if proxy:
                results.append((score, proxy))
                progress.advance(task)
    for score, proxy in results:
        heapq.heappush(working_proxies.queue, (-score, proxy))
    return [proxy for _, proxy in results]

def verify_proxies(proxies, config, verify_threads=10):
    """Wrapper for async proxy verification"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        working = loop.run_until_complete(verify_proxies_async(proxies, config, verify_threads))
        console.print(f"[bold green]✔ Found {len(working)} working proxies[/bold green]")
        return working
    finally:
        loop.close()

def save_proxies(proxies, file_path="proxy.txt"):
    """Save verified proxies"""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("\n".join(proxies) + "\n")
        console.print(f"[bold green]✔ Saved {len(proxies)} proxies to {file_path}[/bold green]")
    except Exception as e:
        logging.error(f"Failed to save proxies to {file_path}: {str(e)}")
        console.print(f"[red]✘ Failed to save proxies: {str(e)}[/red]")

def load_proxies(file_path="proxy.txt"):
    """Load proxies from file"""
    proxies = []
    try:
        if not os.path.exists(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write("")
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                proxy = line.strip()
                if proxy and re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}$", proxy) and proxy not in seen_proxies:
                    proxies.append(proxy)
                    seen_proxies.add(proxy)
        console.print(f"[bold green]✔ Loaded {len(proxies)} unique proxies from {file_path}[/bold green]")
    except Exception as e:
        logging.error(f"Failed to load proxies from {file_path}: {str(e)}")
        console.print(f"[red]✘ Failed to load proxies: {str(e)}[/red]")
    return proxies

async def check_nitro(code, config, webhook=None):
    """Check nitro code with proxy switching"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            proxy = None
            if not working_proxies.empty():
                _, proxy = working_proxies.get()
                if proxy in blacklisted_proxies:
                    continue
            proxy_url = f"http://{proxy}" if proxy else None
            headers = {"User-Agent": random.choice(config["user_agents"])}
            async with aiohttp.ClientSession() as session:
                url = f"https://discord.gift/{code}"
                async with session.get(
                    f"https://discord.com/api/v9/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true",
                    proxy=proxy_url,
                    headers=headers,
                    timeout=5
                ) as response:
                    if response.status == 200 and response.content_type == "application/json":
                        console.print(f"[bold green]✔ VALID NITRO: {url}[/bold green]")
                        if webhook:
                            try:
                                async with session.post(webhook, json={'content': url}):
                                    pass
                            except:
                                pass
                        os.makedirs("output", exist_ok=True)
                        with open("output/NitrogenCodes.txt", "a") as file:
                            file.write(url + "\n")
                        with open("output/NitrogenCodes.json", "a") as file:
                            json.dump({"code": url, "status": "valid"}, file)
                            file.write("\n")
                        if proxy:
                            working_proxies.put((-proxy_scores.get(proxy, 1), proxy))
                        return url, None
                    elif response.status == 429:
                        try:
                            data = await response.json()
                            retry_after = data.get('retry_after', 1000) / 1000
                            retry_after = min(retry_after, 10)  # Cap retry delay
                            console.print(f"[yellow]⚠ Rate limited, wait {retry_after:.3f} s[/yellow]")
                            if proxy:
                                blacklisted_proxies.add(proxy)
                            await asyncio.sleep(retry_after * (2 ** attempt))
                            continue
                        except json.JSONDecodeError:
                            console.print(f"[yellow]⚠ Rate limited with invalid JSON, retrying[/yellow]")
                            if proxy:
                                blacklisted_proxies.add(proxy)
                            await asyncio.sleep(0.1 * (2 ** attempt))
                            continue
                    else:
                        console.print(f"[red]✘ INVALID NITRO: {url}[/red]")
                        if proxy:
                            working_proxies.put((-proxy_scores.get(proxy, 1), proxy))
                        return None, 1
        except Exception as e:
            console.print(f"[red]✘ Error: {url} ({str(e)})[/red]")
            logging.error(f"Error checking {url}: {str(e)}")
            if proxy:
                blacklisted_proxies.add(proxy)
            if attempt < max_retries - 1:
                await asyncio.sleep(0.1 * (2 ** attempt))
    return None, None

def process_code(_, config, webhook):
    """Wrapper for nitro checking"""
    code = "".join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=16))
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(check_nitro(code, config, webhook))
        return result
    finally:
        loop.close()

def display_stats(proxies, valid, invalid):
    """Display runtime statistics with galactic theme"""
    table = Table(title="🌌 Nitrogen by Pecorio - Galactic Stats 🌌", border_style="yellow")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="white")
    table.add_column("Status", style="green")
    
    table.add_row("Working Proxies", str(len(proxies)), "[green]✔[/green]")
    table.add_row("Valid Nitro Codes", str(len(valid)), "[green]✔[/green]")
    table.add_row("Invalid Nitro Codes", str(invalid), "[red]✘[/red]")
    table.add_row("Runtime", f"{time.time() - start_time:.2f} s", "[cyan]🕒[/cyan]")
    
    console.print(table)

def main():
    """Main function"""
    global seen_proxies, working_proxies
    seen_proxies = set()
    working_proxies = PriorityQueue()
    config = load_config()
    set_title("Nitrogen by Pecorio - Galactic Edition")
    display_title()

    # Interactive CLI prompts
    prompt_session = PromptSession(style=prompt_style)
    
    console.print("[bold yellow]🌟 Proxy Management Options 🌟[/bold yellow]")
    console.print("  [1] Scrape new proxies from 50+ sources")
    console.print("  [2] Use pre-scraped proxies (pre_scraped_proxies.txt)")
    console.print("  [3] Combine scraped and pre-scraped proxies")
    console.print("  [4] Use existing proxy.txt (no verification)")
    console.print("  [5] Generate and verify random IPs")
    
    choice = IntPrompt.ask("[prompt]Select option (1-5)[/prompt]", default=1, choices=["1", "2", "3", "4", "5"])
    
    proxies = []
    num_proxies = 500
    verify_threads = 10
    output_file = "proxy.txt"
    auto_nitro = False

    if choice in [1, 3]:
        num_input = prompt_session.prompt("[prompt]Number of proxies to scrape (default 500, 'all' for all proxies)[/prompt]: ", default="500").strip().lower()
        num_proxies = "all" if num_input == "all" else int(num_input or 500)
    elif choice == 5:
        num_proxies = IntPrompt.ask("[prompt]Number of random IPs to generate (default 100)[/prompt]", default=100)

    if choice != 4:
        verify_threads = IntPrompt.ask("[prompt]Number of verification threads (default 10, max 20)[/prompt]", default=10, choices=[str(i) for i in range(1, 21)])
        output_file = prompt_session.prompt("[prompt]Output file for proxies (default proxy.txt)[/prompt]: ", default="proxy.txt").strip()
        auto_nitro = Prompt.ask("[prompt]Proceed to Nitro generator after proxy verification? (y/n, default n)[/prompt]", default="n", choices=["y", "n"]).lower() == "y"

    if choice == 1:
        proxies.extend(asyncio.run(scrape_proxies(config, num_proxies=num_proxies)))
    elif choice == 2:
        proxies.extend(load_pre_scraped_proxies())
    elif choice == 3:
        proxies.extend(asyncio.run(scrape_proxies(config, num_proxies=num_proxies)))
        proxies.extend(load_pre_scraped_proxies())
    elif choice == 4:
        proxies = load_proxies()
    elif choice == 5:
        ports_input = prompt_session.prompt("[prompt]Ports (comma-separated, e.g., 80,8080)[/prompt]: ", default="80,8080,3128,8888,1080").strip()
        ports = [int(p) for p in ports_input.split(",") if p.strip().isdigit()] or config["default_ports"]
        proxies = generate_random_ips(num_ips=num_proxies, ports=ports)

    if choice != 4 and proxies:
        proxies = verify_proxies(set(proxies), config, verify_threads=verify_threads)
        if proxies:
            save_proxies(proxies, file_path=output_file)
        else:
            console.print("[bold red]✘ No working proxies, continuing without proxies[/bold red]")
    elif not proxies:
        console.print("[yellow]⚠ No proxies provided, continuing without proxies[/yellow]")

    if not auto_nitro and choice != 4:
        proceed = Prompt.ask("[prompt]Proceed to Nitro generator? (y/n)[/prompt]", default="y", choices=["y", "n"]).lower()
        if proceed != "y":
            return

    num = IntPrompt.ask("[prompt]Number of Nitro codes to generate and check[/prompt]", default=100)
    threads = IntPrompt.ask("[prompt]Number of threads[/prompt]", default=10, choices=[str(i) for i in range(1, 21)])
    webhook = prompt_session.prompt("[prompt]Discord Webhook (Enter URL or press Enter to skip)[/prompt]: ", default="").strip() or None

    valid = []
    invalid = 0
    display_title()

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeRemainingColumn(),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Checking Nitro codes...", total=num)
        with ThreadPoolExecutor(max_workers=min(threads, 20)) as executor:
            results = list(executor.map(lambda _: process_code(_, config, webhook), range(num)))
            for result in results:
                progress.advance(task)
                if result[0]:
                    valid.append(result[0])
                if result[1]:
                    invalid += 1

    set_title(f"Nitrogen by Pecorio - {len(valid)} Valid | {invalid} Invalid")
    display_stats(proxies, valid, invalid)
    
    console.print(Panel(
        f"[bold green]Valid: {len(valid)}\n"
        f"[bold red]Invalid: {invalid}\n"
        f"[white]Valid Codes: {', '.join(valid) if valid else 'None'}[/white]",
        title="🌟 Results 🌟",
        border_style="yellow"
    ))
    
    Prompt.ask("[prompt]Press ENTER to exit[/prompt]")

if __name__ == "__main__":
    main()