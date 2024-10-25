
import os
import json



assembled_pages_dir = "./"

page_parts_dir = "./pageParts/"

snippets_dir = "./pageParts/snippets/"

actions_dir = "./pageParts/actions/"

music_json = "music.json"

music_section_template = ""

insert_code = [ "<!-- ##",  "## -->" ]


page_html: dict = dict()
snippet_code_html: dict = dict()



def assemble_pages():

    get_pages()

    make_action_snippets()

    get_snippets()

    insert_snippets_into_pages()



def get_pages():
    global page_html

    for file in filter(lambda file: file.endswith('.html'), os.listdir(page_parts_dir)):
        with open(f"{page_parts_dir}{file}", 'r') as f:
            page_html[file] = f.read()

    



def make_action_snippets():
    global music_section_template

    with open(f"{actions_dir}musicSectionTemplate.html") as m_s_t_f:

        music_section_template = m_s_t_f.read()

    make_navigation_snippet()

    make_music_snippet()



def make_music_snippet():
    global snippet_code_html
    
    with open(f"{actions_dir}{music_json}", 'r') as file:
        music_list = json.load(file)["songs"]

    music_snippet = ""

    for song in music_list:
        template = music_section_template

        template = template.replace("<!-- $$songTitle$$ -->", song["title"])
        template = template.replace("<!-- $$soundCloudEmbed$$ -->", build_embed(song["title"], song["embed_url"], song["song_url"]))
        template = template.replace("<!-- $$shortDescription$$ -->", song["short_description"])

        music_snippet += template

    snippet_code_html[snippet_name_to_code("musicSection")] = music_snippet




def build_embed(title: str, embed_url: str, song_url: str) -> str:

    embed = "<iframe width=\"100%\" height=\"166\" scrolling=\"no\" frameborder=\"no\" allow=\"autoplay\" src=\""

    embed += embed_url

    embed += "\"></iframe><div style=\"font-size: 10px; color: #cccccc;line-break: anywhere;word-break: normal;overflow: hidden;white-space: nowrap;text-overflow: ellipsis; font-family: Interstate,Lucida Grande,Lucida Sans Unicode,Lucida Sans,Garuda,Verdana,Tahoma,sans-serif;font-weight: 100;\"><a href=\"https://soundcloud.com/matangi-priya-522922640\" title=\"Matangi Priya\" target=\"_blank\" style=\"color: #cccccc; text-decoration: none;\">Matangi Priya</a> · <a href=\""

    embed += song_url

    embed += "\" title=\""

    embed += title

    embed += "\" target=\"_blank\" style=\"color: #cccccc; text-decoration: none;\">"

    embed += title
    
    embed += "</a></div>"

    return embed




def make_navigation_snippet():
    global snippet_code_html
    
    navigation_snippet = "<div class=\"navigation\">\n"

    for page in page_html.keys():
        navigation_snippet += f"<a href=\"./{page}\">{page.removesuffix(".html").title()}</a>\n"

    navigation_snippet += "</div>\n"

    snippet_code_html[snippet_name_to_code("navigation")] = navigation_snippet





def get_snippets():
    global snippet_code_html

    for file in filter(lambda file: file.endswith('.html'), os.listdir(snippets_dir)):
        with open(f"{snippets_dir}{file}", 'r') as f:
            snippet_code_html[snippet_name_to_code(file.removesuffix(".html"))] = f.read()



def snippet_name_to_code(snippet: str) -> str:
    return f"{insert_code[0]}{snippet}{insert_code[1]}"




def insert_snippets_into_pages():

    for page in page_html.keys():
        with open(f"{assembled_pages_dir}{page[:-5]}.html", 'w') as f:
            f.write(insert_snippets(page_html[page]))




def insert_snippets(template: str) -> str:

    inserted_snippet = False    
    
    assembled_page = template

    for snippet_code in snippet_code_html.keys():
        inserted_snippet = True if assembled_page.find(snippet_code) >= 0 else inserted_snippet
        
        assembled_page = assembled_page.replace(snippet_code, snippet_code_html[snippet_code])

    return insert_snippets(assembled_page) if inserted_snippet else assembled_page





if __name__ == "__main__":

    assemble_pages()
