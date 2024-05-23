from collections import OrderedDict

actual = [
    {
        'user_id': 2332,
        'email': 'test1@gmail.com',
        'folder_id': 2332429292,
    },
    {
        'user_id': 7436,
        'email': 'test2@gmail.com',
        'folder_id': 3299329,
    },
]

email_list = [
    {
        'user_id': 2332,
        'email': 'test1@gmail.com',
        'folder_id': 2332429292,
    },
    {
        'user_id': 7436,
        'email': 'test2@gmail.com',
        'folder_id': 3299329,
    },
    {
        'user_id': 93293,
        'email': 'test3@gmail.com',
        'folder_id': 844382,
    },
    {
        'user_id': 12203023,
        'email': 'test4@gmail.com',
        'folder_id': 433482,
    },
        {
        'user_id': 7436,
        'email': 'test2@gmail.com',
        'folder_id': 3299329,
    },
    {
        'user_id': 93293,
        'email': 'test3@gmail.com',
        'folder_id': 844382,
    },
    {
        'user_id': 3281,
        'email': 'test3@gmail.com',
        'folder_id': 92392,
    },
].extend(actual)
print(email_list.count(email['email']) > 1)
email_list = list(filter(lambda email: email_list.count(email['email']) > 1, email_list ))

# email_list = list(OrderedDict(('email', True)).keys())
print(email_list)
# filtered_list = tuple(OrderedDict((email['email'], True) for email in email_list).keys())
# print(filtered_list)