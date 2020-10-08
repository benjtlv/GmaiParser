from gmail_user_shopping_parser import GmailUserShoppingParser

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
MARKETPLACES = ['LinkedIn']
PAGE_LIMIT = 4

if __name__ == "__main__":

    shopping_parser = GmailUserShoppingParser('credentials.json', SCOPES, MARKETPLACES)
    shopping_emails = shopping_parser.parse_shopping_mails_content(PAGE_LIMIT)

    print(shopping_emails)
