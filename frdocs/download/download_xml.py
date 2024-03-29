import os
from argparse import ArgumentParser
import gzip
from requests import HTTPError
from tqdm import tqdm

from frdocs.download.api import get_with_retry
from frdocs.config import data_dir
from frdocs import load_info_df


def main(args):
    if args.using_frapi:
        download_dir = os.path.join(data_dir, 'raw')

        print('Loading document info')

        info_df = load_info_df(fields=['document_number','full_text_xml_url'])

        info_df = info_df[info_df['full_text_xml_url'].notnull()]

        print(f'Found {len(info_df)} documents with XML urls')

        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        if not args.force_update:

            existing = {f.split('.',1)[0] for f in os.listdir(download_dir)}

            info_df = info_df[~info_df['document_number'].isin(existing)]
            print(f'Found {len(existing)} existing files ({len(info_df)} remain to download)')


        print('Downloading')
        downloaded = 0
        failed = []
        for d,url in tqdm(info_df.values):

            save_file = os.path.join(download_dir, f'{d}.xml.gz')

            try:
                r = get_with_retry(url)

                with gzip.open(save_file,'wb') as f:
                    f.write(r.content)
                downloaded += 1
            except:
                failed.append(d)
        print(f'\nDownloaded XML for {downloaded} documents')
        print(f'Downloading XML failed for {len(failed)} documents')

    else:
        download_dir = os.path.join(data_dir, 'raw')

        info_df = load_info_df(fields=['document_number', 'publication_date', 'full_text_xml_url'])

        #fr_dates_df = info_df[info_df['full_text_xml_url'].notnull()]
        dates_df = info_df \
                            .groupby('publication_date')[['document_number']].count() \
                            .reset_index() \
                            .rename(columns={'document_number': 'documents'})

        dates = sorted(list(dates_df['publication_date']))
        #document_list = sorted(list(dates_df['documents']))

        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        if not os.path.exists(os.path.join(download_dir, 'xml')):
            os.makedirs(os.path.join(download_dir, 'xml'))

        # Search for existing files\
        if args.force_update:
            print(f'Downloading XML for {len(dates)} dates')
        else:
            existing = {f.split('.', 1)[0] for f in os.listdir(os.path.join(download_dir, 'xml'))}
            print(f'Found {len(existing)} existing daily XML files')

            dates = [d for d in dates if d not in existing]
            print(f'Downloading XML for {len(dates)} remaining dates')

        failed = []
        downloaded = 0
        for d in tqdm(dates):

            save_file = os.path.join(download_dir, 'xml', f'{d}.xml.gz')
            url = f'https://www.govinfo.gov/content/pkg/FR-{d}/xml/FR-{d}.xml'

            try:
                r = get_with_retry(url)

                # Check that we haven't been redirected to a no results found page
                if b'xml' in r.content[:20].lower():

                    # Save content
                    with gzip.open(save_file, 'wb') as f:
                        f.write(r.content)
                        downloaded += 1
                else:
                    failed.append(d)

            except HTTPError as e:
                if e.response.status_code == 404:
                    failed.append(d)        

        print(f'\nDownloaded XML for {downloaded} dates')
        print(f'Downloading XML failed for {len(failed)} dates')
        if failed:
            print(dates_df[dates_df['publication_date'].isin(failed)])


if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument('--force_update', dest='force_update', action='store_true')
    parser.add_argument('--using_frapi', dest='using_frapi', action='store_true')

    args = parser.parse_args()

    main(args)


# """
# The following code is an experiment with downloading the XML from federalregister.gov
#
# The advantage is that it can rely on the website's parsing of the frdoc
#
# The problem is that it is *super* slow.
# """
#
#
#
# def main(args):
#
#     download_dir = Path(args.download_dir)
#
#     print('Loading document info')
#
#     info_df = load_info_df(fields=['document_number','full_text_xml_url'])
#
#     info_df = info_df[info_df['full_text_xml_url'].notnull()]
#
#     print(f'Found {len(info_df)} documents with XML urls')
#
#     if not os.path.exists(download_dir):
#         os.makedirs(download_dir)
#
#     if not args.force_update:
#
#         existing = {f.split('.',1)[0] for f in os.listdir(download_dir)}
#
#         info_df = info_df[~info_df['document_number'].isin(existing)]
#         print(f'Found {len(existing)} existing files ({len(info_df)} remain to download)')
#
#
#     print('Downloading')
#     for d,url in tqdm(info_df.values):
#
#         save_file = download_dir/f'{d}.xml.gz'
#
#         r = get_with_retry(url)
#
#         with gzip.open(save_file,'wb') as f:
#             f.write(r.content)
