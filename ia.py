import aiohttp
import asyncio
import os
import xml.etree.ElementTree as ET
from tqdm import tqdm
import sys
import time

def print_intro():
    intro_text = """
IA Downloader

Welcome to IA Downloader! This nifty tool lets you dive into the vast sea of files on the Internet Archive. 
Simply enter an Identifier, and we'll fetch all the goodies for you. Sit back and relax as we handle 
the technical stuff while you enjoy the show. Download speeds may vary based on the archive's mood!
"""
    print(intro_text)

def format_size(size):
    if size < 1024:
        return f"{size} B"
    elif size < 1024**2:
        return f"{size / 1024:.2f} KB"
    elif size < 1024**3:
        return f"{size / 1024**2:.2f} MB"
    elif size < 1024**4:
        return f"{size / 1024**3:.2f} GB"
    else:
        return f"{size / 1024**4:.2f} TB"

async def get_redirect_url(session, identifier):
    base_url = f"https://s3.us.archive.org/{identifier}/"
    async with session.get(base_url, allow_redirects=True) as response:
        if response.status == 200:
            return str(response.url)
        elif response.status == 403:
            content = await response.text()
            root = ET.fromstring(content)
            code = root.find('.//Code')
            if code is not None and code.text == 'NoSuchBucket':
                print("Oops! That Identifier seems to have gone on vacation. It’s not here!")
            else:
                print(f"Yikes! Something went wrong. Status code: {response.status}. Maybe try a different Identifier?")
        else:
            print(f"Uh-oh! Failed to retrieve the file list. Status code: {response.status}. It might be a wild goose chase!")
        return None

async def list_files(session, redirect_url):
    async with session.get(redirect_url) as response:
        if response.status == 200:
            content = await response.text()
            root = ET.fromstring(content)
            files = []
            total_size = 0
            
            for content in root.findall('.//Contents'):
                key = content.find('Key').text
                size = int(content.find('Size').text)
                files.append((key, size))
                total_size += size
            
            return files, total_size
        else:
            print(f"Oopsie! Failed to retrieve the file list. Status code: {response.status}. The files are playing hide and seek!")
            return [], 0

async def download_file(session, redirect_url, file_name, save_path):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    file_url = f"{redirect_url}/{file_name}"
    async with session.get(file_url) as response:
        if response.status == 200:
            total_size = int(response.headers.get('content-length', 0))
            with open(save_path, 'wb') as file, tqdm(
                desc=file_name,
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
                bar_format="{l_bar}{bar} [{elapsed}<{remaining}, {rate_fmt}]",
            ) as bar:
                async for chunk in response.content.iter_any():
                    if chunk:
                        file.write(chunk)
                        bar.update(len(chunk))
            print(f"Success! '{file_name}' has been downloaded. You’re on a roll!")
        else:
            print(f"Uh-oh! Failed to download '{file_name}'. Status code: {response.status}. Maybe it's playing hard to get?")

async def download_all_files(session, redirect_url, files, save_folder):
    tasks = []
    for file_name, _ in files:
        save_path = os.path.join(save_folder, file_name.replace(' ', ''))
        tasks.append(download_file(session, redirect_url, file_name, save_path))
    
    await asyncio.gather(*tasks)

def print_archive_joke():
    jokes = [
        "Why did the Internet Archive go to therapy? It had too many old issues!",
        "Why did the book get a job at the Internet Archive? It wanted to make a 'page' in history!",
        "How does the Internet Archive keep its files so fresh? It always ‘revisions’ them!",
        "Why did the archive get a standing ovation? Because it had a ‘great collection’ of content!",
        "What did the archivist say to the broken file? 'You need to be 'restored' to your former self!'",
        "Why don’t secrets last long in the Internet Archive? Because everything eventually gets ‘archived’!",
        "What’s an Internet Archive’s favorite exercise? ‘Backups’ and ‘restorations’!",
        "Why did the Internet Archive file cross the road? To get to the other ‘server’!"
    ]
    sys.stdout.write("\033[F" * 5)
    sys.stdout.write("\033[J")  
    joke = jokes[int(time.time()) % len(jokes)]
    print(joke)

async def main():
    print_intro()
    
    async with aiohttp.ClientSession() as session:
        while True:
            identifier = input("Enter the Identifier of the Internet Archive item (or 'exit' to quit): ")
            identifier = identifier.replace(' ', '')
            
            if identifier.lower() == 'exit':
                print("Exiting the program. May your archives be ever accessible!")
                break
            
            redirect_url = await get_redirect_url(session, identifier)
            if not redirect_url:
                continue
            
            files, total_size = await list_files(session, redirect_url)
            if not files:
                continue
            
            print(f"\nTotal size of all files: {format_size(total_size)}")
            print("\nAvailable files:")
            for index, (file_name, _) in enumerate(files):
                print(f"{index + 1}. {file_name}")
            print(f"{len(files) + 1}. Download all files")
            
            try:
                choice = int(input("\nEnter the number of the file you want to download (or the number to download all files): ")) - 1
                
                save_folder = identifier.replace(' ', '')
                os.makedirs(save_folder, exist_ok=True)
                
                if 0 <= choice < len(files):
                    file_name, _ = files[choice]
                    save_path = os.path.join(save_folder, file_name.replace(' ', ''))
                    await download_file(session, redirect_url, file_name, save_path)
                elif choice == len(files):
                    print("Downloading all files... Let the download fiesta begin!")
                    start_time = time.time()
                    await download_all_files(session, redirect_url, files, save_folder)
                    if time.time() - start_time > 30:
                        print_archive_joke()
                else:
                    print("Oops! That’s not a valid choice. Let’s try this again.")
            except ValueError:
                print("Oops! That wasn’t a number. Try again with a number, please.")

if __name__ == "__main__":
    asyncio.run(main())
