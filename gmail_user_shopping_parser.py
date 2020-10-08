"""This class allows to parse the shopping-related emails from
from a certain gmail accounts identified by its associated credentials.
One can create as much instances as there are Gmail users / credentials"""

from utils import build_gmail_user_service, fetch_inbox_data


class GmailUserShoppingParser:

    def __init__(self, credentials_path, scopes, marketplaces):
        self.gmail_user_service = build_gmail_user_service(credentials_path, scopes)
        self.marketplaces = marketplaces

    def parse_shopping_mails_content(self, page_limit):
        """Fetches the inbox, keeps only the emails related to shopping orders,
        and shows the actual content"""

        # SELECT / FETCH the inbox content
        inbox_data = fetch_inbox_data(page_limit, self.gmail_user_service)

        # FILTER all the inbox data related to an order from a marketplace
        inbox_data_filtered_by_order_from_marketplace = filter(self._is_mail_order_confirmation, inbox_data)

        # MAP the inbox data to the actual mail content / snippet
        order_confirmation_mails_content = map(self._map_mail_content,
                                               inbox_data_filtered_by_order_from_marketplace)

        return list(order_confirmation_mails_content)

    def _is_mail_order_confirmation(self, mail):
        metadata = mail['payload']['headers']
        sender = [meta['value'] for meta in metadata if meta['name'] == 'From'][0]
        subject = [meta['value'] for meta in metadata if meta['name'] == 'Subject'][0]

        return any([sender.find(marketplace) != -1
                    for marketplace in self.marketplaces])

    @staticmethod
    def _map_mail_content(mail):
        return mail['snippet']
