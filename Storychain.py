# STORYCHAIN-BOT
# Author    : @fakinsit
# Date      : 16/09/24

import os
import time
import json
import random
import requests
import urllib.parse
from pyfiglet import Figlet
from colorama import Fore
from datetime import datetime, timedelta
requests.urllib3.disable_warnings()

TOKEN_FILE = 'account_token.json'
TASKS_URL = 'https://api2.storychain.ai/telegram/tasks'
CLAIM_URL = 'https://api2.storychain.ai/telegram/claim'
FRIENDS_URL = 'https://api2.storychain.ai/telegram/friends'
NFT_RANDOM_URL = 'https://api2.storychain.ai/telegram/ongoing/random'
THEME_RANDOM_URL = 'https://api2.storychain.ai/telegram/themes/ongoing/random'
SWIPE_URL = 'https://api2.storychain.ai/telegram/swipe'
SWIPE_THEME_URL = 'https://api2.storychain.ai/telegram/themes/swipe'
AUTH_URL = 'https://api2.storychain.ai/telegram/auth'

GLOBAL_HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'no-cache',
    'Origin': 'https://quests.storychain.ai',
    'Pragma': 'no-cache',
    'Priority': 'u=1, i',
    'Referer': 'https://quests.storychain.ai/',
    'Sec-CH-UA': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128", "Microsoft Edge WebView2";v="128"',
    'Sec-CH-UA-Mobile': '?0',
    'Sec-CH-UA-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
}

start_color = (255, 250, 250)
end_color = (128, 0, 128)

def display_banner():
    custom_fig = Figlet(font='slant')
    if os.name == "nt":
        custom_fig = Figlet(font='Stforek')
    os.system("title STORYCHAIN BOT" if os.name == "nt" else "clear")
    os.system("cls" if os.name == "nt" else "clear")
    
    print('')
    print_gradient_text(custom_fig.renderText('STORYCHAIN'), start_color, end_color)
    print(f"{Fore.RED}[#] [C] R E G E X{Fore.RESET}  |  {Fore.GREEN}[STORYCHAIN BOT] $${Fore.RESET}")
    print(f"{Fore.GREEN}[+] Welcome & Enjoy Sir !{Fore.RESET}")
    print(f"{Fore.YELLOW}[+] Error? PM Telegram [t.me/fakinsit]{Fore.RESET}")
    print('')

def get_formatted_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def rgb_to_ansi(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

def interpolate_color(start_color, end_color, factor: float):
    return (
        int(start_color[0] + (end_color[0] - start_color[0]) * factor),
        int(start_color[1] + (end_color[1] - start_color[1]) * factor),
        int(start_color[2] + (end_color[2] - start_color[2]) * factor),
    )

def print_gradient_text(text, start_color, end_color):
    colored_text = ""
    for i, char in enumerate(text):
        factor = i / (len(text) - 1) if len(text) > 1 else 1
        r, g, b = interpolate_color(start_color, end_color, factor)
        colored_text += rgb_to_ansi(r, g, b) + char
    print(colored_text + "\033[0m")

def load_tokens():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as f:
            tokens = json.load(f)
            for username, token_data in tokens.items():
                if isinstance(token_data, str):
                    tokens[username] = {
                        'token': token_data,
                        'timestamp': get_formatted_time()
                    }
            return tokens
    return {}

def save_token(username, token):
    tokens = load_tokens()
    tokens[username] = {
        'token': token,
        'timestamp': get_formatted_time()
    }
    with open(TOKEN_FILE, 'w') as f:
        json.dump(tokens, f, indent=4)

def is_token_expired(token_data):
    token_timestamp = datetime.strptime(token_data['timestamp'], "%Y-%m-%d %H:%M:%S")
    return datetime.now() - token_timestamp > timedelta(minutes=30)

def validate_token(telegram_token):
    headers = GLOBAL_HEADERS.copy()
    headers['Cookie'] = f'telegramToken={telegram_token}'
    response = requests.get(FRIENDS_URL, headers=headers)
    return response.status_code != 403

def run_forever():
    try:
        with open('quentod.txt', 'r') as file:
            query_data_list = file.read().splitlines()
        while True:
            any_nft_found = False
            for index, query_data in enumerate(query_data_list, start=1):
                timestamp = Fore.MAGENTA + get_formatted_time() + Fore.RESET
                init_data = makeinitdata(query_data)
                username = init_data['initDataUnsafe']['user']['username']
                tokens = load_tokens()
                token_data = tokens.get(username)
                if token_data:
                    token = token_data['token']
                    if is_token_expired(token_data) or not validate_token(token):
                        print(f"[{timestamp}] - {Fore.YELLOW}Token expired or missing for {Fore.GREEN}@{username}{Fore.YELLOW}, generating a new one...")
                        token = get_token_profile(init_data)
                        if token:
                            print(f"[{timestamp}] - {Fore.GREEN}Success obtained new token for {Fore.YELLOW}@{username}{Fore.RESET}")
                            save_token(username, token)
                        else:
                            print(f"[{timestamp}] - {Fore.RED}Failed to generate a new token for {username}. Skipping...{Fore.RESET}")
                            continue
                    else:
                        print(f"[{timestamp}] - Using existing {Fore.GREEN}valid {Fore.RESET}token{Fore.RESET}")
                else:
                    print(f"[{timestamp}] - No token found for {Fore.GREEN}@{username}{Fore.RESET}. Generating a new one.")
                    token = get_token_profile(init_data)
                    if token:
                        print(f"[{timestamp}] - Success obtained new token for {Fore.GREEN}{username}{Fore.RESET}")
                        save_token(username, token)
                    else:
                        print(f"[{timestamp}] - {Fore.RED}Failed to generate a new token for {username}. Skipping...{Fore.RESET}")
                        continue
                if token:
                    nft_found = perfom_act(token)
                    if nft_found:
                        any_nft_found = True
            if not any_nft_found:
                turudek(1800)
    except Exception as e:
        timestamp = Fore.MAGENTA + get_formatted_time() + Fore.RESET
        print(f"[{timestamp}] - {Fore.RED}[ERROR] Restarting due to {e}{Fore.RESET}")
        run_forever()

def makeinitdata(query_data):
    timestamp = Fore.MAGENTA + get_formatted_time() + Fore.RESET
    encoded_str = query_data
    parsed_data = urllib.parse.parse_qs(encoded_str)
    user_data = {}
    if 'user' in parsed_data:
        try:
            user_data = json.loads(parsed_data['user'][0])
        except json.JSONDecodeError:
            print(f"[{timestamp}] - {Fore.RED}Error decoding user data JSON.{Fore.RESET}")
    init_data_unsafe = {
        "user": user_data,
        "chat_instance": parsed_data.get('chat_instance', [None])[0],
        "chat_type": parsed_data.get('chat_type', [None])[0],
        "auth_date": parsed_data.get('auth_date', [None])[0],
        "hash": parsed_data.get('hash', [None])[0],
    }
    start_param = parsed_data.get('start_param', [None])[0]
    if start_param:
        init_data_unsafe["start_param"] = start_param
    result = {
        "initDataUnsafe": init_data_unsafe,
        "bypass": None,
        "referralCode": parsed_data.get('referralCode', ["5d26292c"])[0],
        "staging": False,
        "devbot": False
    }
    username = user_data.get('username', 'unknown')
    print(f"[{timestamp}] - Loaded account {Fore.GREEN}@{username}{Fore.RESET}")
    return result

def get_token_profile(initdata):
    timestamp = Fore.MAGENTA + get_formatted_time() + Fore.RESET
    payload = initdata
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Content-Length': str(len(payload)),
        'Content-Type': 'application/json',
        'Origin': 'https://quests.storychain.ai',
        'Pragma': 'no-cache',
        'Priority': 'u=1, i',
        'Referer': 'https://quests.storychain.ai/',
        'Sec-CH-UA': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128", "Microsoft Edge WebView2";v="128"',
        'Sec-CH-UA-Mobile': '?0',
        'Sec-CH-UA-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
    }
    try:
        response = requests.post(AUTH_URL, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"[{timestamp}] - User : {Fore.GREEN}{data['username']}{Fore.RESET}")
            print(f"[{timestamp}] - Total score : {Fore.GREEN}{data['score']}{Fore.RESET}")
            print(f"[{timestamp}] - Check-in day : {Fore.GREEN}{data['loginStreak']}{Fore.RESET}")
            cookies = response.cookies
            cookies_dict = requests.utils.dict_from_cookiejar(cookies)
            telegram_token = cookies_dict.get('telegramToken')
            if telegram_token:
                return telegram_token
            else:
                print(f"[{timestamp}] - {Fore.RED}telegramToken not found.{Fore.RESET}")
        else:
            print(f"[{timestamp}] - {Fore.RED}Request failed with status code: {response.status_code}{Fore.RESET}")
    except requests.exceptions.SSLError as ssl_error:
        print(f"[{timestamp}] - {Fore.RED}SSL Error occurred: {ssl_error}{Fore.RESET}")

def get_tasks(token):
    timestamp = Fore.MAGENTA + get_formatted_time() + Fore.RESET
    headers = GLOBAL_HEADERS.copy()
    headers['Cookie'] = f'telegramToken={token}'
    try:
        response = requests.get(TASKS_URL, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data['tasks']
        else:
            print(f"[{timestamp}] - {Fore.RED}Failed to retrieve tasks, status code: {response.status_code}{Fore.RESET}")
    except requests.exceptions.RequestException as e:
        print(f"[{timestamp}] - {Fore.RED}Error while fetching tasks: {e}{Fore.RESET}")
    return []

def start_task(link, name, token):
    timestamp = Fore.MAGENTA + get_formatted_time() + Fore.RESET
    headers = GLOBAL_HEADERS.copy()
    headers['Cookie'] = f'telegramToken={token}'
    try:
        response = requests.get(link, headers=headers)
        if response.status_code == 200:
            print(f"[{timestamp}] - Task {Fore.YELLOW}{name}{Fore.RESET} started! {Fore.RESET}")
            return True
        else:
            print(f"[{timestamp}] - {Fore.RED}Failed to start task {name}, status code: {response.status_code}{Fore.RESET}")
    except requests.exceptions.RequestException as e:
        print(f"[{timestamp}] - {Fore.RED}Error while starting task: {e}{Fore.RESET}")
    return False

def claim_task(task_id, name, token):
    timestamp = Fore.MAGENTA + get_formatted_time() + Fore.RESET
    headers = GLOBAL_HEADERS.copy()
    headers['Content-Type'] = 'application/json'
    headers['Cookie'] = f'telegramToken={token}'
    payload = {"taskId": task_id}
    try:
        response = requests.post(CLAIM_URL, headers=headers, json=payload)
        if response.status_code == 200:
            print(f"[{timestamp}] - Task {Fore.GREEN}{name}{Fore.RESET} claimed!{Fore.RESET}")
        else:
            print(f"[{timestamp}] - {Fore.RED}Failed to claim task {name}, status code: {response.status_code}{Fore.RESET}")
    except requests.exceptions.RequestException as e:
        print(f"[{timestamp}] - {Fore.RED}Error while claiming task: {e}{Fore.RESET}")

def get_random_nfts(initdata):
    timestamp = Fore.MAGENTA + get_formatted_time() + Fore.RESET
    headers = GLOBAL_HEADERS.copy()
    headers['Cookie'] = f'telegramToken={initdata}'
    url = f'{NFT_RANDOM_URL}?count=5'
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            nftdata = response.json()
            if 'nfts' in nftdata:
                nfts = nftdata['nfts']
                if not nfts:
                    print(f"[{timestamp}] - {Fore.YELLOW}No more NFTs left.{Fore.RESET}")
                    return []
                nft_ids = [nft.get('_id', 'N/A') for nft in nfts]
                print(f"[{timestamp}] - Success get {Fore.GREEN}{len(nft_ids)} NFTs{Fore.RESET}")
                return nft_ids
            else:
                print(f"[{timestamp}] - {Fore.RED}'nfts' key not found in response{Fore.RESET}")
        else:
            print(f"[{timestamp}] - {Fore.RED}Request failed with status code: {response.status_code}{Fore.RESET}")
    except requests.exceptions.SSLError as ssl_error:
        print(f"[{timestamp}] - {Fore.RED}SSL Error occurred: {ssl_error}{Fore.RESET}")
    except json.JSONDecodeError as json_error:
        print(f"[{timestamp}] - {Fore.RED}Failed to decode JSON: {json_error}{Fore.RESET}")
    return []

def get_random_theme(initdata):
    timestamp = Fore.MAGENTA + get_formatted_time() + Fore.RESET
    headers = GLOBAL_HEADERS.copy()
    headers['Cookie'] = f'telegramToken={initdata}'
    url = f'{THEME_RANDOM_URL}?count=5'
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            themedata = response.json()
            if 'themes' in themedata:
                themes = themedata['themes']
                if not themes:
                    print(f"[{timestamp}] - {Fore.YELLOW}No more themes left.{Fore.RESET}")
                    return []
                theme_ids = [theme.get('_id', 'N/A') for theme in themes]
                print(f"[{timestamp}] - Success get {Fore.GREEN}{len(theme_ids)} themes{Fore.RESET}")
                return theme_ids
            else:
                print(f"[{timestamp}] - {Fore.RED}'themes' key not found in response{Fore.RESET}")
        else:
            print(f"[{timestamp}] - {Fore.RED}Request failed with status code: {response.status_code}{Fore.RESET}")
    except requests.exceptions.SSLError as ssl_error:
        print(f"[{timestamp}] - {Fore.RED}SSL Error occurred: {ssl_error}{Fore.RESET}")
    except json.JSONDecodeError as json_error:
        print(f"[{timestamp}] - {Fore.RED}Failed to decode JSON: {json_error}{Fore.RESET}")
    return []

def play_swipe(initdata, nft_ids):
    timestamp = Fore.MAGENTA + get_formatted_time() + Fore.RESET
    headers = GLOBAL_HEADERS.copy()
    headers['Cookie'] = f'telegramToken={initdata}'
    for nft_id in nft_ids:
        swipe_right = random.choice([True, False])
        payload = {"nftId": nft_id, "swipeRight": swipe_right, "inDeck": []}
        retry_count = 0
        max_retries = 5
        delay_between_requests = 1
        while retry_count <= max_retries:
            try:
                response = requests.post(SWIPE_URL, headers=headers, json=payload)
                if response.status_code == 200:
                    response_data = response.json()
                    if 'nfts' in response_data and len(response_data['nfts']) > 0:
                        nft = response_data['nfts'][0]
                        print(f"[{timestamp}] - Success swipe NFT {Fore.GREEN}{nft['_id']}{Fore.RESET}{Fore.RESET}")
                    else:
                        print(f"[{timestamp}] - {Fore.YELLOW}NFT unavailable to swipe{Fore.RESET}")
                    break
                elif response.status_code == 429:
                    retry_count += 1
                    retry_after = int(response.headers.get('Retry-After', delay_between_requests))
                    time.sleep(retry_after)
                else:
                    print(f"[{timestamp}] - {Fore.RED}Failed swipe {nft['title']} NFT | ID={nft_id}-{response.status_code}{Fore.RESET}")
                    break
            except requests.exceptions.SSLError as ssl_error:
                print(f"[{timestamp}] - {Fore.RED}SSL Error occurred: {ssl_error}{Fore.RESET}")
                break
            except json.JSONDecodeError as json_error:
                print(f"[{timestamp}] - {Fore.RED}Failed to decode JSON: {json_error}{Fore.RESET}")
                break

def play_theme_swipe(initdata, theme_ids):
    timestamp = Fore.MAGENTA + get_formatted_time() + Fore.RESET
    headers = GLOBAL_HEADERS.copy()
    headers['Cookie'] = f'telegramToken={initdata}'
    user_info = None
    for theme_id in theme_ids:
        swipe_right = random.choice([True, False])
        payload = {"themeId": theme_id, "swipeRight": swipe_right, "inDeck": []}
        retry_count = 0
        max_retries = 5
        delay_between_requests = 1
        while retry_count <= max_retries:
            try:
                response = requests.post(SWIPE_THEME_URL, headers=headers, json=payload)
                if response.status_code == 200:
                    response_data = response.json()
                    if 'themes' in response_data and len(response_data['themes']) > 0:
                        theme = response_data['themes'][0]
                        print(f"[{timestamp}] - Success swipe theme {Fore.GREEN}{theme['_id']}{Fore.RESET}{Fore.RESET}")
                    else:
                        print(f"[{timestamp}] - {Fore.YELLOW}Theme unavailable to swipe{Fore.RESET}")
                    if 'user' in response_data:
                        user_info = response_data['user']
                    break
                elif response.status_code == 429:
                    retry_count += 1
                    retry_after = int(response.headers.get('Retry-After', delay_between_requests))
                    time.sleep(retry_after)
                else:
                    print(f"[{timestamp}] - {Fore.RED}Failed swipe {theme['theme']} theme | ID={theme_id}-{response.status_code}{Fore.RESET}")
                    break
            except requests.exceptions.SSLError as ssl_error:
                print(f"[{timestamp}] - {Fore.RED}SSL Error occurred: {ssl_error}{Fore.RESET}")
                break
            except json.JSONDecodeError as json_error:
                print(f"[{timestamp}] - {Fore.RED}Failed to decode JSON: {json_error}{Fore.RESET}")
                break
    if user_info:
        print(f"[{timestamp}] - User : {Fore.GREEN}{user_info['username']}{Fore.RESET}")
        print(f"[{timestamp}] - Total score : {Fore.GREEN}{user_info['score']}{Fore.RESET}")
        print(f"[{timestamp}] - Check-in day : {Fore.GREEN}{user_info['loginStreak']}{Fore.RESET}")

def perfom_act(initdata):
    nft_found = False
    theme_found = False
    tasks = get_tasks(initdata)
    for task in tasks:
        if not task['completed']:
            start_task(task['link'], task['title'], initdata)
        if task['completed'] and not task['claimed']:
            claim_task(task['_id'], task['title'], initdata)
    nft_ids = get_random_nfts(initdata)
    if nft_ids:
        play_swipe(initdata, nft_ids)
        nft_found = True
    theme_ids = get_random_theme(initdata)
    if theme_ids:
        play_theme_swipe(initdata, theme_ids)
        theme_found = True
    print(f"{Fore.WHITE}-" * 50)
    turudek(5)
    return nft_found or theme_found

def turudek(total_seconds):
    timestamp = Fore.MAGENTA + get_formatted_time() + Fore.RESET
    bar_length = 22
    start_time = time.time()
    end_time = start_time + total_seconds
    while True:
        current_time = time.time()
        remaining_time = end_time - current_time
        if remaining_time <= 0:
            print(f"[{timestamp}] - {Fore.GREEN}Time's up!, waiting..{Fore.RESET}", end='\r')
            break
        elapsed_time = total_seconds - remaining_time
        blocks_filled = int(bar_length * (elapsed_time / total_seconds))
        progress_bar = ""
        for i in range(blocks_filled):
            factor = i / (blocks_filled - 1) if blocks_filled > 1 else 1
            r, g, b = interpolate_color(start_color, end_color, factor)
            progress_bar += rgb_to_ansi(r, g, b) + "#"
        empty_space = "-" * (bar_length - blocks_filled)
        hours = int(remaining_time // 3600)
        minutes = int((remaining_time % 3600) // 60)
        seconds = int(remaining_time % 60)
        time_remaining = f"{hours:02}:{minutes:02}:{seconds:02}"
        print(f"[{Fore.MAGENTA}{Fore.YELLOW}WAIT TIME: {time_remaining}{Fore.RESET}] - [{progress_bar}{Fore.WHITE}{empty_space}{Fore.RESET}]", end='\r')
        time.sleep(0.1)

if __name__ == "__main__":
    display_banner()
    run_forever()
