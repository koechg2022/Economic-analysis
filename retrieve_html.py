


import sys, os
import datetime
import requests
from bs4 import BeautifulSoup

sys_slash = '\\' if sys.platform == f"win32" else '/'

http_requests = {
    f"GET" : requests.get,
    f"POST" : requests.post,
    f"PUT" : requests.put,
    f"HEAD" : requests.head,
    f"OPTIONS" : requests.options
}
write_to_directory = f"./html_retrieved"
default_file = f"retrieved_file"

def index_of(to_find : str, the_list : list[str], ignore_case = True) -> int:
    
    for index in range(len(the_list)):
        
        if ignore_case:
            
            if to_find.lower() == the_list[index].lower():
                return index
            continue
        
        if to_find == the_list[index]:
            return index
    
    return -1

def retrieve_html(the_url : str = "https://www.goodreads.com/book/show/33571713-a-column-of-fire", http_request = f"GET") -> str:
    """
        Retrieve the html content of a website passed in.

        Args:
            the_url (str, optional): The url to the website whose html is to be retrieved. 
                Defaults to "https://www.goodreads.com/book/show/33571713-a-column-of-fire".

        Returns:
            bytes: The text of the html that is returned directly from the requests.get function
    """
    
    if http_request not in http_requests:
        return f"UnRecognized HTTP Request f{http_request}"
    
    return http_requests[http_request](the_url).text

def write_to_file(file_name : str, data_to_write : str | bytes, directory_to_write_to : str = write_to_directory) -> bool:
    """
        Write data to the file and directory specified

        Args:
            file_name (str): The name of the file to write the data to
            data_to_write (str): The data to write to `file_name`

        Returns:
            bool: `True` if the data is successfully written in, `False` otherwise.
    """
    the_answer = False
    with open(f"{directory_to_write_to}{sys_slash}{file_name}", f"w", encoding =  "utf-8") as open_file:
        try:
            open_file.write(data_to_write)
            the_answer = True
        except Exception:
            
            print(f"Failed writing data... ")
        
    return the_answer
            
def contains_file(file_name : str, directory : str = write_to_directory) -> bool:
    
    for this in os.listdir(directory):
        
        if this == file_name:
            return True
    return False

if __name__ == f"__main__":
    
    # print(retrieve_html() if len(sys.argv) == 1 else retrieve_html(sys.argv[1]))
    if len(sys.argv) == 1:
        soup = BeautifulSoup(retrieve_html(), 'html.parser')
        write_to_file("A Column of Fire.html", soup.prettify())
    else:
        the_html = retrieve_html(sys.argv[-1])
        soup = BeautifulSoup(the_html, 'html.parser')
        if contains_file(default_file, write_to_directory) != -1:
            write_to_file(f"{default_file}--{datetime.datetime.now()}.html", soup.prettify())
        else:
            write_to_file(f"{default_file}.html", soup.prettify())