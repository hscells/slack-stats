#!/usr/bin/python3

import json, sys, os

def main(argv, argc):

    # check to see if there was at least one argument
    if argc != 2:
        print('Wrong number of arguments, expected slackstats.py <exported folder name>')
        sys.exit(1)

    # get out folder name
    folder = argv[1]

    # open the needed files, also kinda tests if it's a real exported slack folder
    try:
        channels_json = open(folder + '/channels.json', 'r').read()
        users_json = open(folder + '/users.json', 'r').read()
    except:
        print('Could not detect correct files in the folder entered.')
        raise

    # sweet, now we have the channel and users json data structures in memory!
    channels = json.loads(channels_json)
    users = json.loads(users_json)

    usernames = {}
    for user in users:
        usernames[user['id']] = user['name']
    print('found {} users'.format(len(usernames)))

    channel_names = [channel['name'] for channel in channels]
    print('found {} channels'.format(len(channels)))

    # now we get to do the complicated stuff...
    for channel_name in channel_names:
        print('stats for {}'.format(channel_name))
        # this will store our stats
        stats = {}
        # walk the tree for each of the channels we found
        for root, dirs, files in os.walk(folder + '/' + channel_name):
            for file in files:
                with open(root + '/' + file) as logs:
                    # the log is the individual json log file
                    log = json.loads(logs.read())
                    for post in log:
                        # we need to filter out erroneous posts
                        if post['type'] == 'message' and 'user' in post.keys():
                            # finally, tally up the count of posts
                            if post['user'] not in stats.keys():
                                stats[post['user']] = 0
                            else:
                                stats[post['user']] += 1
        # we can now print our stats out!
        for key, value in stats.items():
            print('\t{} has {} posts'.format(usernames[key], value))


if __name__ == '__main__':
    main(sys.argv, len(sys.argv))