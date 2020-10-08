from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


def build_gmail_user_service(credentials_path, google_api_scopes):
    """Builds a service that allows the programmer to access all
    the available Gmail data of a specific Gmail account associated
    with the given credentials"""

    print("Loading Gmail Service...")

    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(credentials_path, google_api_scopes)
        creds = tools.run_flow(flow, store)
    gmail_user_service = build('gmail', 'v1', http=creds.authorize(Http()))

    print("Service Loaded")

    return gmail_user_service


def fetch_inbox_data(page_limit, gmail_user_service):
    """Does the actual fetching and returns a list containing all the data for each mail"""

    fetchable_data = _get_fetchable_inbox_data(page_limit, gmail_user_service)

    # can take time
    print("Fetching inbox...")

    inbox_data = [gmail_user_service.users().messages().get(userId='me', id=message['id']).execute()
                  for message in fetchable_data]

    print("Fetching inbox...")

    return inbox_data


def _get_fetchable_inbox_data(page_limit, gmail_user_service):
    """Returns the total list of fetchable objects that corresponds to all the
     emails of the first <page_limit> pages of the inbox"""

    page_data_request, page_data_response = None, None
    fetchable_inbox_data = []

    for idx_page in range(page_limit):

        page_data_request, page_data_response, current_page_data = _get_next_page_data(gmail_user_service,
                                                                                       page_data_request,
                                                                                       page_data_response)

        # if the current_page_data is an empty list
        if not current_page_data:
            break

        fetchable_inbox_data.extend(current_page_data)

    return fetchable_inbox_data


def _get_next_page_data(gmail_user_service, previous_request, previous_response):
    """Returns a list of fetchable emails instances for the next page
    or the first page if called for the first time"""

    # When the method is called for the first time
    if previous_request is None:
        previous_request = (gmail_user_service
                            .users()
                            .messages()
                            .list(userId='me', labelIds=['INBOX']))

    else:
        previous_request = (gmail_user_service
                            .users()
                            .messages()
                            .list_next(previous_request, previous_response)
                            )
        if previous_request is None:
            return []

    previous_response = previous_request.execute()
    current_page_data = previous_response.get('messages', [])
    return previous_request, previous_response, current_page_data
