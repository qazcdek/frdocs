import urllib
import urllib.parse
import urllib.error
from urllib.request import Request, urlopen
import time
import json

baseURL = 'https://www.federalregister.gov/api/v1'
searchURL = baseURL + '/documents.json?'
articleURL = baseURL + '/documents/'

allFields = ['abstract', 'action', 'agencies',
             'agency_names', 'body_html_url', 'cfr_references',
             'citation', 'comments_close_on', 'correction_of',
             'corrections', 'dates', 'docket_id', 'docket_ids',
             'document_number', 'effective_on', 'end_page',
             'excerpts', 'executive_order_notes',
             'executive_order_number', 'full_text_xml_url',
             'html_url', 'images', 'json_url', 'mods_url', 'page_length',
             'page_views', 'pdf_url', 'president',
             'presidential_document_number', 'proclamation_number',
             'public_inspection_pdf_url', 'publication_date', 'raw_text_url',
             'regulation_id_number_info', 'regulation_id_numbers',
             'regulations_dot_gov_info', 'regulations_dot_gov_url',
             'significant', 'signing_date', 'start_page', 'subtype',
             'title', 'toc_doc', 'toc_subject', 'topics', 'type', 'volume']


def search(searchParams):
    response = get_with_retry(searchURL, searchParams,
                              retry_intervals=[1, 10, 100], timeout=100)
    try:
        results = json.loads(str(response))
        print(results)
    except:
        print(f"에러? {str(response)}")
    
    if results['count'] > 10000:
        print('Warning: Results will be truncated at 10,000 entries')

    if results['count'] > 0:
        for result in results['results']:
            yield result

        while 'next_page_url' in results:
            nextPage = get_with_retry(results['next_page_url'],
                                      retry_intervals=[1, 10, 100], timeout=100)
            results = nextPage.json()

            for result in results['results']:
                yield result


def get_all_agencies(retry_intervals=[1, 10]):
    response = get_with_retry(baseURL + '/agencies',
                              retry_intervals=retry_intervals)
    response = response.read()
    return json.loads(response.decode(encoding='utf-8'))





def get_with_retry(url, params={}, retry_intervals=[1., 10., 60.],
                   wait_interval=60, timeout=10, check_json=False):
    '''
    A wrapper for requests.get that tries to handle most of the common reasons
    to retry including:
        -Miscellaneous timeouts and connection errors other than bad-request
        -Rate limits (via wait_interval)
        -corrupted json (optional)
    '''
    url = url + "?" + urllib.parse.urlencode(params)

    if retry_intervals:
        for retry_interval in retry_intervals:
            try:
                r = urlopen(url, timeout=timeout)
            except urllib.error.HTTPError as e:
                print(f"after {retry_interval} sec, retry get metadata, error code: {e}")
                time.sleep(retry_interval)
                continue
            if r.status >= 200 and r.status < 400:
                if check_json:
                    # Optional: retry if json content is corrupted
                    try:
                        string = r.read().decode('utf-8')
                        json_obj = json.loads(string)
                    except Exception:
                        continue

                # Return successful request
                return r

            elif r.status == 429 and wait_interval > 0:
                # If rate-limit reached, wait and then use recursion to
                # restart retry intervals
                # (Never gives up unless a different error occurs)
                print('Rate limit reached. Waiting {:.1f} min to retry'
                      .format(wait_interval / 60.0))
                time.sleep(wait_interval)
                return get_with_retry(url, params=params,
                                      retry_intervals=retry_intervals,
                                      wait_interval=wait_interval,
                                      timeout=timeout,
                                      check_json=check_json)

            elif 400 <= r.status <= 500:
                # Don't bother to retry if the request is bad
                #r.raise_for_status()
                print(f"protocol error: {r.status}")

            else:
                # Retry if any other error occurs
                time.sleep(retry_interval)
    else:
        r = urlopen(url, timeout=timeout)

        # Still want to handle rate limits without other retries.
        if r.status == 429 and wait_interval > 0:
            # If rate-limit reached, wait and then use recursion to
            # restart retry intervals
            # (Never gives up unless a different error occurs)
            print('Rate limit reached. Waiting {:.1f} min to retry'
                    .format(wait_interval / 60.0))

            time.sleep(wait_interval)
            return get_with_retry(url, params=params,
                                    retry_intervals=retry_intervals,
                                    wait_interval=wait_interval,
                                    timeout=timeout,
                                    check_json=check_json)

        else:
            print("error occured!")
            return r


def get(url, params={}, timeout=10, ignore_codes=[], check_json=False):
    print('Warning: requestsUtilities.get is depreciated. Use get_with_retry.')
    return get_with_retry(url, params=params, retry_intervals=[],
                          timeout=timeout, check_json=check_json)
