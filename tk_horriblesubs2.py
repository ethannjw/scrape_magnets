import tkinter
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidArgumentException
import requests
from lxml import html


request_session = requests.session()
response = request_session.get("https://jespa.megahtex.com/web/login")

# Tkinter init
root = tkinter.Tk("test")
root.title("Scrape Horriblesubs")
root.geometry("700x500+2+400")

# Instruction label at top
url_label = tkinter.Label(root, text="Enter the url")
url_label.pack(side='top', fill=tkinter.X)

# Entry field at top
entry1 = tkinter.Entry(root, width=60)
entry1.pack(side='top')

# Instance of bottom label
label_var = tkinter.StringVar()

# Instance of status label
status_label = tkinter.Label(root, textvariable=label_var)
status_label.pack(side='bottom')

# Button instance
button1 = tkinter.Button(text='Get the Links',
                         command=lambda: GetMagnets(entry1.get()))
button1.pack(side='top')

# Instance of text box
textbox = tkinter.Text(root, height=25, width=80)
textbox.pack(side="top")


def set_label(name):
    """Dynamically sets name of the botton label"""
    label_var.set(name)


def GetMagnets(url):
    """Main Function runs when button is clicked"""

    set_label(url)  # text variable for label

    from selenium.webdriver.chrome.options import Options
    option = Options()
    option.headless = True

    with webdriver.Chrome() as driver:

        try:
            driver.get(url)

            sleep(3)
            set_label("Sleeping for 3 Sec")

            try:
                show_more = driver.find_element_by_class_name('more-button')
                show_more.click()

            except Exception:
                print('did not click show more button')
                pass

            sleep(3)
            # magnet_links = driver.find_elements_by_xpath('//*[@title="Magnet Link"]')
            magnet_links = driver.find_elements_by_xpath(
                '//*[@class="rls-link link-720p"]/span[2]/a')

            magnets = ""
            count = 0
            for link in magnet_links:
                magnets += link.get_attribute("href")
                count += 1
                magnets += "\n"

            output = "Total: {} links scraped".format(str(count))
            print(output)

            textbox.insert(tkinter.END, magnets)

            set_label(output)

        except InvalidArgumentException:
            set_label("Invalid URL!")


root.mainloop()
