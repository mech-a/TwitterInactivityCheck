from googleapiclient.discovery import build
from pprint import pprint

# ---
# TODO use service accts
google_key = ''
# ---


def fetch_cell_hyperlinks(service, spreadsheet_id, ranges):
    # TODO cite stackoverflow
    result = service.spreadsheets().get(
        spreadsheetId=spreadsheet_id,
        ranges=ranges,
        fields="sheets/data/rowData/values/hyperlink"
    ).execute()
    return result


def get_twitter_usernames_from_sheet(spreadsheet_id, ranges, key=google_key):
    service = build('sheets', 'v4', developerKey=key)
    hyperlinks = fetch_cell_hyperlinks(service, spreadsheet_id, ranges)
    urls = extract_url_from_hyperlinks(hyperlinks)
    usernames = []
    for url in urls:
        # TODO see if twitter api can handle username from url
        # TODO understand why this didn't work in a function
        # from last occurence of slash
        raw_username = url[url.rfind('/')+1:]
        # remove queries
        if '?' in raw_username:
            username = raw_username[:raw_username.find('?')]
            usernames.append(username)
        else:
            usernames.append(raw_username)
    return usernames


def extract_url_from_hyperlinks(hyperlinks):
    urls = []
    # TODO switch to while loop and return dictionary such that we can track urls to their sheet position
    #  (or, perhaps use nested lists)
    for sheet in hyperlinks['sheets']:
        for e in sheet['data'][0]['rowData']:
            # filters for {}, represents any non-hyperlinked line
            if e:
                urls.append(e['values'][0]['hyperlink'])
    return urls


#pprint(get_twitter_usernames_from_sheet(rv_spreadsheet_id, fansite_ranges))