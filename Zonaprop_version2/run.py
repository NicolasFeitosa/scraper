from DrissionPage import ChromiumPage, ChromiumOptions
from CloudflareBypasser import CloudflareBypasser
from DrissionPage.common import Actions
from datetime import datetime
from openpyxl import Workbook
from time import sleep
import pandas as pd
import logging
import random
import json
import os
import re

basic_url = "https://www.zonaprop.com.ar"

def get_chromium_options(arguments: list) -> ChromiumOptions:
    """
    Configures and returns Chromium options.
    
    :param browser_path: Path to the Chromium browser executable.
    :param arguments: List of arguments for the Chromium browser.
    :return: Configured ChromiumOptions instance.
    """
    options = ChromiumOptions()
    # options.set_argument('--auto-open-devtools-for-tabs', 'true') # we don't need this anymore
    for argument in arguments:
        options.set_argument(argument)
    return options

def bypass_get(driver,url: str):
    try:
        #Start bypass
        logging.info('Navigating to the demo page.')
        # driver.get('https://nopecha.com/demo/cloudflare')
        # driver.get('https://www.nettiauto.com/en/uusimmat?page=1')
        driver.get(url)

        # Where the bypass starts
        logging.info('Starting Cloudflare bypass.')
        cf_bypasser = CloudflareBypasser(driver)
        cf_bypasser.bypass()

        logging.info("Enjoy the content!")
        logging.info("Title of the page: %s", driver.title)

        # Sleep for a while to let the user see the result if needed
        sleep(1)
    except Exception as e:
        logging.error("An error occurred: %s", str(e))


def extract_main_features(text):
    start = text.find('"mainFeatures"')
    if start == -1:
        return None

    # Find the first '{' after "mainFeatures"
    start = text.find('{', start)

    count = 0
    end = start

    while end < len(text):
        if text[end] == '{':
            count += 1
        elif text[end] == '}':
            count -= 1
            if count == 0:
                break
        end += 1

    # Include the "mainFeatures" key manually
    return '"mainFeatures":' + text[start:end+1]

def scrap(page,url,property_type) -> list:

    global Location, Address, Neighborhood, Listing_price, Currency, Type_transaction, Monthly_fee, Location_building, Cardinal_orientation, Covered_area, Total_area, Number_rooms, Bedrooms, Bathrooms, Garage, Age_property, Bright, Amenities
    page.get(url)

    '--------------------------------------------------------------------Scraping Logic'
    # page.wait.ele_displayed('tag:article', timeout = 5)
    page.wait.ele_displayed('tag:div@@id=article-container')
    Main_container = page.ele('tag:div@@id=article-container', timeout = 1)


    #Extract main containers
    Price_container = Price_container2_ = Location_container = Property_container = Character_container = None

    if Main_container != None:
        Price_container = Main_container.ele('tag:div@@class=price-container-property', timeout=0.1)
        Price_container2_ = Main_container.ele('tag:span@@class=list-prices', timeout=0.1)
        Location_container = Main_container.ele('tag:section@@id=map-section', timeout=0.1)
        Property_container = Main_container.ele('tag:ul@@id=section-icon-features-property', timeout=0.1)
        Character_container = page.ele('tag:div@@id=cookies-policy', timeout=0.1)
        page.stop_loading()
    
    else:
        loading_flag = page.ele('tag:a@@aria-label=Logo de zonaprop', timeout=0.1)
        if loading_flag == None:
            raise Exception("Website page is not loaded!")

    print('===================================================')
    Property_type = property_type
    print("Property_type: ", Property_type)

    print('===================================================')
    Listing_price = Currency = Type_transaction = Monthly_fee = None
    if Price_container != None:
        
        basic_price_container = Price_container.ele('tag:div@@class=price-value', timeout=0.1)
        monthly_container =  Price_container.ele('tag:div@@class=price-extra', timeout=0.1)
        if basic_price_container != None:

            source_string = basic_price_container.text.strip()
            # print(source_string)

            if source_string is not None:

                if "USD" in source_string:
                    Currency = "USD"
                elif "$" in source_string:
                    Currency = "$"
                else:
                    Currency = None
                
                if Currency != None:
                    Type_transaction = source_string.split(Currency)[0]
                    # Listing_price_parts = source_string.split(Currency)[1]
                    Listing_price = Currency + " " + source_string.split(Currency)[1].strip()
                    # Listing_price = " ".join(Listing_price_parts).strip()

        if monthly_container != None:
            Monthly_fee_parts = monthly_container.text.strip().split(" ")[1:]
            Monthly_fee = " ".join(Monthly_fee_parts).strip()


        print("Type of transiction: ", Type_transaction)
        print("Listing price: ", Listing_price)
        print("Currency: ",Currency)
        print("Monthly fee: ", Monthly_fee)

    elif Price_container2_ != None:
        Type_transaction = Price_container2_.ele('tag:span@@class=operation-type').text.strip()
        Listing_price = Price_container2_.children('tag:span')[-1].text.strip()
        Currency = Listing_price.split(" ")[0]

        print("Type of transiction: ", Type_transaction)
        print("Listing price: ", Listing_price)
        print("Currency: ",Currency)

        
    print('===================================================')
    Location = Address = Neighborhood = None
    if Location_container != None:
        source_string = Location_container.text.strip()
        Address = source_string.split(",")[0]
        Location = source_string.split(",")[-1]
        Neighborhood_parts = source_string.split(",")[1:-1]
        Neighborhood = ",".join(Neighborhood_parts)

        print("Location: ", Location)
        print("Address: ", Address)
        print("Neighborhood: ",Neighborhood)
                    
    print('===================================================')
    Location_building = Cardinal_orientation = Covered_area = Total_area = Number_rooms = Bedrooms = Bathrooms = Garage = Age_property = Bright = None    

    if Property_container != None:
        # Get Pricing, Bedrooms, Residences, Estimated_completion_date
        itemname_list_1 = ["Location_building", "Cardinal_orientation", "Covered_area", "Total_area", "Number_rooms", "Bedrooms", "Bathrooms", "Garage", "Age_property", "Bright"]
        itemprop_list_1 = ["disposicion", "orientacion", "scubierta", "stotal", "ambiente", "dormitorio", "bano", "cochera", "antiguedad", "luminosidad"]

        for itemname, itemprop in zip(itemname_list_1, itemprop_list_1):
            temp_container = Property_container.ele(f'tag:i@@class:{itemprop}',timeout=0.1)

            if temp_container != None:
                origin_text = temp_container.parent('tag:li').text.strip()
                globals()[itemname] = ' '.join(origin_text.split())
                print(f"{itemname}:  ", globals()[itemname])
        
        #Garage State
        if Garage != None:
            Garage = "Yes"
        else:
            Garage = "No"

        #Bright State
        if Bright != None: 
            Bright = "Yes"
        else:
            Bright = "No"

    elif Character_container != None:
        itemname_list_1 = ["Location_building", "Cardinal_orientation", "Covered_area", "Total_area", "Number_rooms", "Bedrooms", "Bathrooms", "Garage", "Age_property", "Bright"]
        itemprop_list_1 = ["disposicion", "orientacion", "scubierta", "stotal", "ambiente", "dormitorio", "bano", "cochera", "antiguedad", "luminosidad"]

        String_container = Character_container.next('tag:script')
        
        if String_container != None:
            text_ = String_container.inner_html.strip()

            # Step 1: Extract the mainFeatures block
            main_features_block = extract_main_features(text_)
            
            if main_features_block:
                main_features_text = "{" + main_features_block + "}"  # Only the inside {...}
                
                # Step 2: Prepare text for JSON parsing
                cleaned_text = main_features_text.replace('null', 'null')  # To be safe (if needed)

                # Step 3: Load into a Python dict
                try:
                    main_features = json.loads(cleaned_text)
                    # print(main_features)
                except Exception as e:
                    print("Error parsing JSON:", e)
                    main_features = {}

                # Step 4: Extract value and measure for icons of interest
                for feature in main_features['mainFeatures'].values():
                    icon = feature.get('icon')
                    # print(icon)

                    for itemname, itemprop in zip(itemname_list_1, itemprop_list_1):

                        if icon == itemprop:
                            value = feature.get('value')
                            measure = feature.get('measure')
                            if measure is not None:  # Only if value is NOT null
                                value = str(value) + measure
                            
                            globals()[itemname] = value
                            print(f"{itemname}:  ", globals()[itemname])
                
                #Garage State
                if Garage != None:
                    Garage = "Yes"
                else:
                    Garage = "No"

                #Bright State
                if Bright != None: 
                    Bright = "Yes"
                else:
                    Bright = "No"

            else:
                print("mainFeatures not found.")


    print('===================================================')
    Amenities = []
    if Character_container != None:
        # print(Character_container)
        String_container = Character_container.next('tag:script')
        
        if String_container != None:
            text_ = String_container.inner_html.strip()
            # print(text_)

            # caracteristicas_section = re.search(r'"Características"\s*:\s*({.*?})\s*(,|})', text_, re.DOTALL)
            # caracteristicas_section = re.search(r'"Características":\s*{(.*?)}(?=,\s*")', text_, re.DOTALL)

            # Find the position where "Características" starts
            start = text_.find('"Características":')
            # print(start)

            if start != -1:
                # From there, find the opening '{'
                first_brace = text_.find('{', start)
                count = 0
                end = first_brace

                # Now, manually count braces to find where the object ends
                while end < len(text_):
                    if text_[end] == '{':
                        count += 1
                    elif text_[end] == '}':
                        count -= 1
                        if count == 0:
                            break
                    end += 1

                # Extract the substring
                caracteristicas_section = text_[start:end+1]
                # print(caracteristicas_section)

                # Step 2: Extract all labels inside the "Características" section
                Amenities = re.findall(r'"label":"([^"]+)"', caracteristicas_section)

                print(Amenities)
            else:
                print('"Características" not found.')
    print('===================================================')
    Url = url

    Extract_item_list = [Property_type, Location, Address, Neighborhood, Listing_price, Currency, 
                        Type_transaction, Monthly_fee, Location_building, Cardinal_orientation, 
                        Covered_area, Total_area, Number_rooms, Bedrooms, Bathrooms, Garage, 
                        Age_property, Bright, Amenities, Url]
    
    sleep(random.uniform(0.1,0.3))
    return Extract_item_list


def main():
    property_type = input("Enter property type(departamentos/casas/ph): ")
    # property_type = "ph"
    operation_type = input("Enter operation type(alquiler/venta/alquiler-temporal): ")
    Start_page = input("Enter the page number you want to start from (e.g. 5): ")
    # operation_type = "venta"

    url_source = basic_url + "/" + property_type + "-" + operation_type

    '-------------------------------------------------------------------Verify Excel file'
    #Create title
    title = datetime.now().date()

    # Define the file name
    file_name = f"zonaprop-{property_type}-{operation_type}-{title}.xlsx"

    # Check if the file exists and remove it
    if os.path.exists(file_name):
        os.remove(file_name)
        print(f"{file_name} already exists. Removing it.")
    else:
        print(f"{file_name} generated sucessfully.")

    df = pd.DataFrame(columns=["Property_type", "Location", "Address", "Neighborhood", "Listing_price", 
                        "Currency", "Type_transaction", "Monthly_fee", "Location_building", 
                        "Cardinal_orientation", "Covered_area", "Total_area", "Number_rooms", 
                        "Bedrooms", "Bathrooms", "Garage", "Age_property", "Bright", "Amenities", "Url"])

    df.to_excel(file_name, index=False)

    '----------------------------------------------------------------------------------------Launch Browser'    
    arguments = [
        "-no-first-run",
        "--disable-gpu"
    ]

    options = get_chromium_options(arguments).auto_port()
    page = ChromiumPage(addr_or_opts=options)
    page.set.load_mode.none()

    Extract_title_list = ["Property_type", "Location", "Address", "Neighborhood", "Listing_price", 
                        "Currency", "Type_transaction", "Monthly_fee", "Location_building", 
                        "Cardinal_orientation", "Covered_area", "Total_area", "Number_rooms", 
                        "Bedrooms", "Bathrooms", "Garage", "Age_property", "Bright", "Amenities", "Url"]
    
    '----------------------------------------------------------------------------------------Get page numbers'    
    #Get cookie
    page.get(basic_url)
    sleep(random.uniform(2,3))
    
    #Get Page numbers
    url = url_source + ".html"
    bypass_get(page,url)
    page.get(url)
    page.wait.ele_displayed('tag:div@@class=postingsList-module__postings-container')
    Card_container = page.ele('tag:div@@class=postingsList-module__postings-container')
    Total_container = page.ele('tag:h1@@class=postingsTitle-module__title')
    page.stop_loading()

    ## Text process and print total pages
    Card_numbers_ = len(Card_container.children('tag:div@@class:card-container'))

    Source_string = Total_container.text.strip()
    digits = re.findall(r'\d+', Source_string)
    Total_numbers = int(''.join(digits))

    if Total_numbers % Card_numbers_ == 0:
        Total_pages = int(Total_numbers / Card_numbers_)
    
    else:
        Total_pages = int(Total_numbers / Card_numbers_ ) + 1

    print("Total Pages: ", Total_pages)
    print('________________________________')    



    '-------------------------------------------------------------------Launch Scrap'    
    for i in range(int(Start_page), Total_pages + 1):
        print('----------------------------------')
        print(f'{i}page is loaded...')
        if i == 1:
            url = url_source + ".html"
            bypass_get(page,url)
        else:
            url = url_source + f"-pagina-{i}.html"

        page.get(url)
        page_data = []


        while True:
            try:
                page.wait.ele_displayed('tag:div@@class=postingsList-module__postings-container')
                Card_container = page.ele('tag:div@@class=postingsList-module__postings-container')
                # print(Card_container)

                Link_container_list = Card_container.children('tag:div@@class:card-container')
                page.stop_loading()

                url_list = []
                for link_container in Link_container_list:
                    url_container = link_container.ele('tag:div@@class:postingCardLayout')
                    url = url_container.attr('data-to-posting')
                    url = basic_url + url
                    print(url)
                    url_list.append(url)


                break
            except:
                print('----------------------------------')
                print('Page is restarted.......')
                page.quit()
                sleep(random.uniform(2,3))

                page = ChromiumPage(addr_or_opts=options)
                page.set.load_mode.none()

                #Get cookie and bypass
                page.get(basic_url)
                sleep(random.uniform(2,3))
                bypass_get(page,url)

                # Move to website
                page.get(url)



        
        for url in url_list:
            # Extract_item_list = scrap(page,url)
            # page_data.append({Extract_title_list[i]: Extract_item_list[i] for i in range(len(Extract_title_list))})

            while True:
                try:
                    Extract_item_list = scrap(page,url, property_type)
                    page_data.append({Extract_title_list[i]: Extract_item_list[i] for i in range(len(Extract_title_list))})

                    break
                except:
                    print('Page is restarted.......')
                    page.quit()
                    sleep(random.uniform(2,3))
                    page = ChromiumPage(addr_or_opts=options)
                    page.set.load_mode.none()

                    #Get cookie and bypass
                    page.get(basic_url)
                    sleep(random.uniform(2,3))
                    bypass_get(page,url)

            


        #Save into excel file
        if page_data:
            # Append the new data to the existing Excel file
            df = pd.DataFrame(page_data)
            with pd.ExcelWriter(file_name, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
                df.to_excel(writer, index=False, header=False, startrow=writer.sheets['Sheet1'].max_row)
            print(f'Appended data for page {i} to {file_name}')

    print('============================================================')
    print('Scraping is completed!')
    page.quit()

if __name__ == '__main__':
    main()
