import tkinter
import requests
from lxml import html

# url = "https://horriblesubs.info/shows/maou-gakuin-no-futekigousha"

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

def get_links(url):
    """Gets the first batch from the url given"""
    response = requests.get(url)
    tree = html.fromstring(response.text)
    show_id_link = tree.xpath('//*[@class="post-inner-content"]/article/div/script')
    # get the show id
    show_id = show_id_link[0].text.split()[3][:-1]
    magnet_link_list = []
    page_no=0

    show_request_URL = f"https://horriblesubs.info/api.php?method=getshows&type=show&showid={show_id}nextid={page_no}"
    show_response = requests.get(show_request_URL)
    show_request_tree = html.fromstring(show_response.text)
    magnet_link_list = show_request_tree.xpath('//*[@class="rls-link link-720p"]/span[2]/a')
    # while True:
    #     try:
    #         show_request_URL = f"https://horriblesubs.info/api.php?method=getshows&type=show&showid={show_id}nextid={page_no}"
    #         show_response = requests.get(show_request_URL)
    #         show_request_tree = html.fromstring(show_response.text)
    #         magnet_link_list = show_request_tree.xpath('//*[@class="rls-link link-720p"]/span[2]/a')
    #         page_no = page_no + 1
    #     except:
    #         break

    return [a.get('href') for a in magnet_link_list]


def set_label(name):
    """Dynamically sets name of the botton label"""
    label_var.set(name)


def GetMagnets(url):
    """Main Function runs when button is clicked"""

    set_label(url)  # text variable for label

    try:
        magnet_links = get_links(url)

    except InvalidArgumentException:
        set_label("Invalid URL!")

    magnets = ""
    count = 0
    for link in magnet_links:
        magnets += link
        count += 1
        magnets += "\n"

    output = "Total: {} links scraped".format(str(count))
    print(output)

    textbox.insert(tkinter.END, magnets)

    set_label(output)

root.mainloop()
