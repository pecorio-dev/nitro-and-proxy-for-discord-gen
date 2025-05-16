# **Nitro Generator and Checker** 🚀

Welcome to the **Nitro Generator and Checker**! This Python tool generates and checks Discord Nitro gift codes using a robust proxy pool to bypass rate limits. Designed for educational purposes, it features advanced proxy scraping, verification, and efficient code checking. 🎉

## **Table of Contents** 📋
- [Features](#features-✨)
- [Prerequisites](#prerequisites-🛠️)
- [Installation](#installation-⚙️)
- [Usage](#usage-🚀)
- [Configuration](#configuration-🔧)
- [Troubleshooting](#troubleshooting-🛡️)
- [Contributing](#contributing-🤝)
- [License](#license-📜)

## **Features** ✨
- 🌐 Scrape proxies from **40+ sources**, including HTTP and SOCKS5.
- 🔍 Verify proxy quality with **response time and anonymity scoring**.
- 🔄 **Rapid proxy switching** on Discord rate limits (429 responses).
- 📊 **Progress tracking** with visual progress bars.
- 📝 **JSON configuration** for easy source management.
- 🔔 **Webhook support** for valid Nitro code notifications.
- 📈 **Detailed logging** for debugging and monitoring.

## **Prerequisites** 🛠️
Before running the tool, ensure you have:
- 🐍 **Python 3.8 or higher** installed.
- 📦 **pip** for installing dependencies.
- 🌐 An **active internet connection**.
- (Optional) A **Discord webhook URL** for notifications.

## **Installation** ⚙️
Follow these steps to set up the project:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Pecorio17/nitro-generator.git
   cd nitro-generator
   ```

2. **Install Dependencies**:
   Use the provided **batch script** to automate dependency installation on Windows, or run the commands manually.

   ### **Batch Script for Windows**
   Save the following as `install.bat` and run it **as administrator**:

   ```batch
   @echo off
   echo Installing Python dependencies...
   python --version >nul 2>&1
   if %ERRORLEVEL% neq 0 (
       echo Python is not installed! Please install Python 3.8 or higher.
       pause
       exit /b
   )
   echo Installing required packages...
   pip install aiohttp colorama beautifulsoup4 tqdm requests
   if %ERRORLEVEL% equ 0 (
       echo Dependencies installed successfully!
   ) else (
       echo Failed to install dependencies. Check your internet or pip configuration.
   )
   pause
   ```

   ### **Manual Installation**
   Run the following command to install dependencies:
   ```bash
   pip install aiohttp colorama beautifulsoup4 tqdm requests
   ```

3. **Verify Installation**:
   Ensure all dependencies are installed:
   ```bash
   pip list
   ```

## **Usage** 🚀
1. **Run the Script**:
   ```bash
   python nitro_generator.py
   ```

2. **Follow the Prompts**:
   - Choose a **proxy management option** (1-5).
   - Specify the **number of proxies** to scrape (or 'all').
   - Set the **number of verification threads** (default: 30, max: 50).
   - Provide an **output file** for proxies (default: `proxy.txt`).
   - Decide whether to **proceed to Nitro generation** automatically.
   - Enter the **number of Nitro codes** to generate and check.
   - Specify the **number of threads** for checking.
   - (Optional) Provide a **Discord webhook URL**.

3. **View Results**:
   - **Valid Nitro codes** are saved to `output/NitroCodes.txt` and `output/NitroCodes.json`.
   - **Logs** are written to `nitro_generator.log` for debugging.

## **Configuration** 🔧
The script uses a `config.json` file to manage **proxy sources** and **settings**. The default configuration includes:
- **Proxy Sources**: **40+ APIs and websites** for proxy scraping.
- **User Agents**: A list of **browser user-agents** for rotation.
- **Default Ports**: Common ports for **random IP generation** (80, 8080, 3128, 8888, 1080).

To customize, edit `config.json`:
```json
{
    "proxy_sources": [
        {"name": "ProxyScrape", "type": "api", "url": "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http,socks4,socks5"},
        ...
    ],
    "user_agents": [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...",
        ...
    ],
    "default_ports": [80, 8080, 3128, 8888, 1080]
}
```

## **Troubleshooting** 🛡️
- **No Proxies Found**:
  - Ensure your **internet connection** is stable.
  - Check `config.json` for **valid proxy source URLs**.
  - Increase the **number of proxies** to scrape or use pre-scraped proxies.

- **Rate Limit Errors (429)**:
  - The script **automatically switches proxies** on rate limits.
  - If persistent, **reduce the number of threads** or **increase proxies**.

- **Dependency Issues**:
  - Verify **Python and pip** are correctly installed.
  - Run `pip install -r requirements.txt` if you create a `requirements.txt` file.

- **Logs**:
  - Check `nitro_generator.log` for **detailed error messages**.

## **Contributing** 🤝
Contributions are welcome! To contribute:
1. **Fork** the repository.
2. Create a **new branch** (`git checkout -b feature/your-feature`).
3. **Commit** your changes (`git commit -m "Add your feature"`).
4. **Push** to the branch (`git push origin feature/your-feature`).
5. Open a **pull request**.

Please ensure your code follows **PEP 8 guidelines** and includes appropriate tests.

## **License** 📜
This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

**Happy Nitro hunting!** 🎯 If you encounter issues or have suggestions, open an issue on GitHub. ⭐
