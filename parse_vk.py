import sys
import vk_api
import pprint

from config import VK_API_VERSION, MIPT_UNIVERSITY_ID


def count_mipt_friends(girl, api):
    girl_user = api.users.get(user_ids=girl, v=VK_API_VERSION)
    pprint.pprint(girl_user)
    friends = api.friends.get(user_id=girl_user[0]['id'], order='random', fields='universities')
    count = 0
    #pprint.pprint(friends)
    for friend in friends['items']:
        try:
            for university in friend['universities']:
                if university['id'] == MIPT_UNIVERSITY_ID:
                    count += 1
                    break
        except:
            continue
    return count


def main():
    girl = sys.argv[1]
    vk_api_key = sys.argv[2]

    api = vk_api.VkApi(token=vk_api_key).get_api()

    print(count_mipt_friends(girl, api))


main()
