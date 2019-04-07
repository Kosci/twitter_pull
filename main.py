import json
import twython as twy
import datetime


def main():
    with open('credentials.json', 'r') as file:
        auth = json.load(file)

    twitter = twy.Twython(auth.get('CONSUMER_KEY'),
                          auth.get('CONSUMER_SECRET'),
                          auth.get('ACCESS_TOKEN'),
                          auth.get('ACCESS_SECRET'))


    username = ''
    cur_date = get_date()
    write_to_file('followers.txt', cur_date,
                  get_followers(twitter, username))

    write_to_file('following.txt', cur_date,
                  get_following(twitter, username))


def get_followers(twitter, username):
    followers = list()
    followers_json = twitter.get_followers_list(screen_name=username,
                                                count=200)

    for k in followers_json.get('users'):
        followers.append(get_user_info(k))

    cursor = followers_json.get('next_cursor')
    while cursor != 0:
        followers_json = twitter.get_followers_list(screen_name=username,
                                                    count=200,
                                                    cursor=cursor)

        for k in followers_json.get('users'):
            followers.append(get_user_info(k))

    return followers


def get_following(twitter, username):
    following = list()
    following_json = twitter.get_friends_list(screen_name=username,
                                              count=200)

    for k in following_json.get('users'):
        following.append(get_user_info(k))

    cursor = following_json.get('next_cursor')
    while cursor != 0:
        following_json = twitter.get_followers_list(screen_name=username,
                                                    count=200,
                                                    cursor=cursor)

        for k in following_json.get('users'):
            following.append(get_user_info(k))

    return following


def get_user_info(user):
    user_info = {
        'id': user.get('id'),
        'display_name': user.get('name'),
        'username': user.get('screen_name')
    }

    return user_info


def get_date():
    now = datetime.datetime.now()
    date = '{month}/{day}/{year} {hour}:{minute}'.format(
        month=now.month, day=now.day, year=now.year,
        hour=now.hour, minute=now.minute
    )

    return date


def write_to_file(filename, date, users):
    f = open(filename, "a")

    f.write('--------------' + date + '--------------')
    for user in users:
        f.write(user.get('id'))
        f.write(user.get('display_name'))
        f.write('@' + user.get('username'))
        f.write('\n')
    f.close()


if __name__ == "__main__":
    main()
