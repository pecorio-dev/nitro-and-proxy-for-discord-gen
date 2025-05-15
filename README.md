Discord Nitro Generator & Proxy Scraper
A Python script to scrape/verify proxies and generate/check Discord Nitro codes. Created by Pecorio17.
Features

Scrapes proxies from 15 sources or generates random IPs.
Verifies proxies for Discord API compatibility.
Generates and checks Discord Nitro codes.
Customizable: number of proxies, threads, output file.
Option to auto-proceed to Nitro generation.

Installation

Clone the repository:git clone https://github.com/yourusername/nitro-generator.git
cd nitro-generator


Install dependencies:pip install httpx==0.27.2 colorama beautifulsoup4



Usage

Run the script:python nitrogen.py


Proxy Management:
Choose from 5 options:
1: Scrape proxies from 15 sources.
2: Use pre_scraped_proxies.txt.
3: Combine scraped and pre-scraped.
4: Use proxy.txt (no verification).
5: Generate random IPs.


Specify number of proxies, verification threads, output file.
Option to auto-proceed to Nitro generation.


Nitro Generator:
Enter number of codes and threads.
Optionally provide a Discord webhook.


Outputs:
Verified proxies: proxy.txt (or custom file).
Valid Nitro codes: output/NitroCodes.txt.



Example pre_scraped_proxies.txt
45.77.245.138:8080
103.153.154.147:80
47.251.43.115:3128

Usage Tips

Premium Proxies: Free proxies are often blocked by Discord. Use premium proxies (e.g., Bright Data, Smartproxy) in pre_scraped_proxies.txt for better results.
Performance: Use 100–200 proxies and 30–40 threads for optimal speed.
Random IPs: Option 5 generates random IPs; use cautiously as it may connect to arbitrary hosts.
Rate Limits: The script handles Discord’s rate limits automatically.
Debugging: Run standalone (python nitrogen.py) to isolate issues from atio.py.

Ethical Note

Generating/checking Nitro codes without permission violates Discord’s terms and may lead to bans or legal issues.
Use for educational purposes or with authorization only.

Author

Pecorio17
For custom scripts, development requests, or project inquiries, contact: stream2free.pecorio@gmail.com

License
MIT License. See LICENSE for details.
