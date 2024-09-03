import retrieve_html
from bs4 import BeautifulSoup

url = f"https://www.worldometers.info/gdp/gdp-by-country/"

def all_letters(the_string : str) -> bool:
    
    for c in the_string:
        # print(f"Checking {c} in the_string")
        if ord(c) >= ord('A') and ord(c) <= ord('Z') or ord(c) >= ord('a') and ord(c) <= ord('z'):
            continue
        # print(f"Returning False")
        return False
    
    return True


def all_numbers(the_string : str) -> bool:
    
    for c in the_string:
        # print(f"Checking {c} in the_string")
        if ord(c) >= ord('0') and ord(c) <= ord('9'):
            continue
        # print(f"Returning False")
        return False
    
    return True



def get_country_GDPs() ->dict[str : dict[str : float]]:
    """
        Summary:
            Get the GDPs of each country along with the nominal GDP,
            growth rate, population, GDP per capital, and share of world GDP.
            
        Arguments:
            None
            
        Return:
            A dict of dicts with the following structure:
            
            {
                f"COUNTRY" : {
                    f"GDP" : float (max in trillions)
                    f"GROWTH" : float (greater than 1 number percentage 0-100)
                    f"POPULATION" : int (max billions)
                    f"GDP_PER_CAPITA" : int (This will be in dollars)
                    f"SHARE_OF_WORLD_GDP" : float (greater than 1 number percentage 0-100)
                    f"GLOBAL_RANK" : int (the ranking globally based on GDP)
                }
            }
            
            **NOTE**
            * These names are not the actual dictionary inputs. They are just used here for example references.
    """
    
    the_answer = {}
    the_html = retrieve_html.retrieve_raw_html(url)
    
    if the_html.status_code != 200:
        
        print(f"Failed to retrieve the url. HTTP Request status code {the_html.status_code}")
        return the_answer
    
    # print("\n\n", f"Retrieved html code successfully")
    complete_soup = BeautifulSoup(the_html.text, "html.parser")
    gdp_table = complete_soup.find(f"table", {f"id" : "example2"})
    
    column_titles, rank, rank_index, country = [], "Rank", -1, -1
    columns_html = gdp_table.find(f"thead").find("tr").find_all(f"th")
    for index in range(len(columns_html)):
        this_data = columns_html[index].text
        this_data.split(" ")
        if this_data == '#':
            column_titles.append(rank)
            rank_index = index
            continue
        
        if this_data.lower() == 'country':
            country = index
            column_titles.append(this_data)
            continue
        
        column_titles.append(this_data)
        
    column_body = gdp_table.find("tbody")
    
    countries = column_body.find_all("tr")
    
    for country_index in range(len(countries)):
        
        country_data = countries[country_index].find_all("td")
        country_name = country_data[country].text
        the_answer[country_name] = {}
        for data_index in range(len(country_data)):
            
            if data_index == country:
                continue
            else:
                this_data = country_data[data_index].text
                this_data = this_data.replace('$', '')
                this_data = this_data.replace('%', '')
                this_data = this_data.replace(',', '')
                # this_data = this_data.replace('trillion', '')
                # this_data = this_data.replace('million', '')
                # this_data = this_data.replace('billion', '')
                the_answer[country_name][column_titles[data_index]] = this_data if this_data[-1].isalpha() else int(this_data) if this_data.find('.') == -1 else float(this_data) if this_data[-1].isdigit() else this_data
        # print(the_answer)
        # break
    
    return the_answer


if __name__ == f"__main__":
    
    national_gdps = get_country_GDPs()
    for country in national_gdps:
        print(f"{country}'s Economic infomation:")
        for aspect in national_gdps[country]:
            print("\t", f"{aspect}: {national_gdps[country][aspect]}")