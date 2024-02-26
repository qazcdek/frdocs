import os
import requests
import lxml.etree as et
import re
from tqdm import tqdm

from frdocs.config import data_dir


reginfo_url = 'https://www.reginfo.gov'
agenda_href = '/public/do/eAgendaXmlReport'


def get_agenda_urls():
    response = requests.get(reginfo_url + agenda_href)
    response.raise_for_status()
    html = response.content

    try:
        html = html.decode('utf8')
    except (UnicodeDecodeError,AttributeError):
        pass

    root = et.HTML(html)

    agenda_urls = [reginfo_url + href for href in root.xpath('.//a/@href') if href.endswith('.xml')]

    return agenda_urls


def main(args=None):
    start_agenda = "".join(args.start_agenda.split("."))
    end_agenda = "".join(args.end_agenda.split("."))
    print(f"start from {start_agenda} end to {end_agenda}")
    print('Downloading unified agenda files')
    download_dir = os.path.join(data_dir, 'raw')

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    if not os.path.exists(os.path.join(download_dir, 'agenda')):
        os.makedirs(os.path.join(download_dir, 'agenda'))

    agenda_urls = get_agenda_urls()
    for url in tqdm(agenda_urls):
        r = requests.get(url)
        r.raise_for_status()
        xml = r.content

        # Publication id provides a more consistent way of naming the file than the href
        m = re.search(rb'<PUBLICATION_ID>(\d{4})(\d{2})</PUBLICATION_ID>',xml)

        save_file = os.path.join(download_dir, 'agenda', f"{m.group(1).decode('utf8')}-{m.group(2).decode('utf8')}.xml")

        if int(m.group(1).decode('utf8') + m.group(2).decode('utf8')) >= int(start_agenda) and int(m.group(1).decode('utf8') + m.group(2).decode('utf8')) <= int(end_agenda):

            with open(save_file,'wb') as f:
                f.write(xml)
            print(f"{m.group(1).decode('utf8') + m.group(2).decode('utf8')} complete!")
        else:
            print(f"{m.group(1).decode('utf8') + m.group(2).decode('utf8')} is out of range!")

if __name__ == '__main__':
    main()