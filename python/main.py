import random
import time
import threading
import requests
import urllib3
import os
from typing import List, Dict, Iterable
import sys
from fake_useragent import UserAgent

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TIMEOUT_SLEEP = 10
URL = "https://ngl.link/api/submit"

PRINT_LOCK = threading.Lock()
COUNTER_LOCK = threading.Lock()

INVALID_PROXIES: List[str] = []
MESSAGES: List[str] = []
PROXIES: List[str] = []

ua = UserAgent()

TERM_STYLES = {
    "error": "\033[38;5;196m",
    "success": "\033[38;5;82m",
    "warning": "\033[38;5;214m",
    "critical": "\033[38;5;200m",
    "reset": "\033[0m"
}

VERSION = "2.2.0"
GITHUB_RAW_URL = "https://raw.githubusercontent.com/borthdayzz/ngl-spammer/refs/heads/main/python/main.py"


def print_sync(msg: str) -> None:
    with PRINT_LOCK:
        print(msg, flush=True)


def print_status(status: str, msg: str) -> None:
    with PRINT_LOCK:
        indicators = {
            "error": "×",
            "success": "»",
            "warning": "!",
            "critical": "†"
        }
        style = TERM_STYLES.get(status, TERM_STYLES["reset"])
        indicator = indicators.get(status, "•")
        print(f"{style}{indicator} {msg}{TERM_STYLES['reset']}", flush=True)


def print_banner() -> None:
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                          boggle.cc                            ║
    ║                    Created by: borthdayzz                     ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def load_file_lines(filename: str) -> List[str]:
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
            if not lines:
                print_status("warning", f"Empty file: {filename}")
            return lines
    except FileNotFoundError:
        print_status("error", f"File not found: {filename}")
        return []


def build_headers(username: str) -> Dict[str, str]:
    return {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Referer": f"https://ngl.link/{username}",
        "Origin": "https://ngl.link",
        "User-Agent": ua.random,
    }


def proxy_worker(proxy: str, username: str, messages: List[str], counter: List[int], stop_event: threading.Event, delay: float = 0, total: int = 0) -> None:
    session = requests.Session()
    px = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    while not stop_event.is_set():
        with COUNTER_LOCK:
            if total > 0 and counter[0] >= total:
                stop_event.set()
                break

        headers = build_headers(username)
        data = {
            "username": username,
            "question": random.choice(messages),
            "deviceId": "".join(random.choices("0123456789abcdef", k=42)),
            "gameSlug": "",
            "referrer": "",
        }
        try:
            resp = session.post(URL, headers=headers, data=data, proxies=px, timeout=(2, 5))
            status = resp.status_code
            if status == 429:
                time.sleep(TIMEOUT_SLEEP)
                continue
            if status != 200:
                print_status("error", f"{status} | drop {proxy}")
                break
            with COUNTER_LOCK:
                counter[0] += 1
                print_status("success", f"Messages Sent: {counter[0]}")
                if total > 0 and counter[0] >= total:
                    stop_event.set()
                    break
                if delay > 0:
                    time.sleep(delay)
        except requests.exceptions.Timeout:
            print_status("warning", f"Timeout | {proxy}")
            break
        except (requests.exceptions.ProxyError, requests.exceptions.SSLError, requests.exceptions.ConnectionError):
            print_status("error", f"Failed | {proxy}")
            with COUNTER_LOCK:
                if proxy not in INVALID_PROXIES:
                    INVALID_PROXIES.append(proxy)
            break
        except Exception as e:
            print_status("critical", f"Error | {proxy} | {type(e).__name__}")
            break


def send_messages(username: str, messages: List[str], proxies: List[str], delay: float = 0, total: int = 0) -> None:
    counter = [0]
    stop_event = threading.Event()
    threads: List[threading.Thread] = []
    for proxy in proxies:
        if proxy in INVALID_PROXIES:
            continue
        t = threading.Thread(
            target=proxy_worker,
            args=(proxy, username, messages, counter, stop_event, delay, total),
            daemon=True,
        )
        threads.append(t)
        t.start()
    for t in threads:
        t.join()


def get_username() -> str:
    while True:
        try:
            username = input("\033[38;5;87m⟫ Target Username: \033[0m").strip()
            if not username:
                print_status("warning", "Username cannot be empty")
                continue
            return username
        except KeyboardInterrupt:
            print_status("critical", "\nOperation cancelled")
            raise


def clear_console() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def check_for_updates() -> bool:
    try:
        print_status("success", "Checking for updates...")
        response = requests.get(GITHUB_RAW_URL, timeout=5)
        if response.status_code == 200:
            github_version = response.text.split('VERSION = "')[1].split('"')[0]
            if github_version != VERSION:
                return True
        return False
    except requests.Timeout:
        print_status("warning", "Update check timed out - skipping")
        return False
    except requests.ConnectionError:
        print_status("warning", "Could not connect to update server - skipping")
        return False
    except Exception as e:
        print_status("warning", f"Update check failed: {str(e)}")
        return False


def update_script() -> None:
    try:
        response = requests.get(GITHUB_RAW_URL, timeout=10)
        if response.status_code == 200:
            with open(__file__, "w", encoding="utf-8") as f:
                f.write(response.text)
            print_status("success", "Update successful! Restarting...")
            python = sys.executable
            os.execl(python, python, *sys.argv)
    except requests.Timeout:
        print_status("error", "Update download timed out")
    except requests.ConnectionError:
        print_status("error", "Could not connect to update server")
    except Exception as e:
        print_status("error", f"Update failed: {str(e)}")


def get_spam_settings() -> tuple:
    while True:
        try:
            count_input = input("\033[38;5;87m⟫ How many messages to send?: \033[0m").strip()
            if not count_input.isdigit() or int(count_input) <= 0:
                print_status("warning", "Please enter a valid positive number")
                continue
            
            speed_input = input("\033[38;5;87m⟫ Delay between messages (0 for fast, in seconds): \033[0m").strip()
            try:
                delay = float(speed_input)
                if delay < 0:
                    print_status("warning", "Delay cannot be negative")
                    continue
            except ValueError:
                print_status("warning", "Please enter a valid number for delay")
                continue
            
            return int(count_input), delay
        except KeyboardInterrupt:
            print_status("critical", "\nOperation cancelled")
            raise


def main() -> None:
    clear_console()
    print_banner()
    
    if check_for_updates():
        print_status("warning", f"New version available! Current version: {VERSION}")
        response = input("\033[38;5;87m⟫ Update now? (y/n): \033[0m").strip().lower()
        if response == 'y':
            update_script()
            return
    
    print_status("success", "Loading resources...")
    global MESSAGES, PROXIES
    
    MESSAGES = load_file_lines("messages.txt")
    PROXIES = load_file_lines("proxy.txt")
    
    if not MESSAGES or not PROXIES:
        print_status("critical", "Required files missing or empty")
        return
        
    try:
        username = get_username()
        count, delay = get_spam_settings()
        print_status("success", f"Starting: {count} messages to {username} with {delay}s delay")
        send_messages(username, MESSAGES, PROXIES, delay, count)
    except KeyboardInterrupt:
        print_status("critical", "\nShutting down...")
        return


if __name__ == "__main__":
    main()
