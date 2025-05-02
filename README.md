# Zonaprop Scraper

This project is a custom web scraper for extracting real estate listings from [Zonaprop Argentina](https://www.zonaprop.com.ar). It collects detailed property data such as price, address, features, and amenities. It uses **DrissionPage** for browser automation and includes a **Cloudflare bypasser** to handle protection layers.

---

## 🚀 Features

- Cloudflare-protected scraping using a custom bypass module.
- Extracts property data: location, price, rooms, area, orientation, garage, amenities, and more.
- Outputs results into an Excel file (`.xlsx`) per property type and operation (rent/sale).
- Handles both **for-sale** and **for-rent** listings.
- Resilient error-handling with automatic browser restarts if a page fails.

---

## 🗂 Project Structure

| File                        | Description |
|-----------------------------|-------------|
| `run.py`                   | Main scraping script. Requests input for property type and operation (e.g., "departamentos", "venta") and writes results to Excel. |
| `CloudflareBypasser.py`    | Module to automatically detect and bypass Cloudflare protection on page load. |
| `install_library.sh/.bat`  | Scripts to install required dependencies (Linux or Windows). |
| `run.sh/.bat`              | Scripts to run the scraper (Linux or Windows). |
| `zonaprop-*.xlsx`          | Example outputs for scraped listings (sale/rent). |
| `Readme.txt`               | Simple instructions for local use. |

---

## 💻 Installation

Make sure you have **Python 3.12.4+** installed.

### Windows
```bash
./install_library.bat
./run.bat
