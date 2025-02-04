import argparse
import os
import shutil
import time

import requests
import urllib.request
from tqdm import tqdm


def download_with_progress(url, download_path, original_file_name):
    # Get the total file size
    with urllib.request.urlopen(url) as response:
        total_size = int(response.info().get("Content-Length", 0))

    # Open the file and start downloading with progress tracking
    with open(download_path, "wb") as file, tqdm(
            desc=f"Downloading {original_file_name}",
            total=total_size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
    ) as bar:
        def show_progress(block_num, block_size, total_size):
            bar.update(block_size)  # Update the progress bar

        urllib.request.urlretrieve(url, download_path, show_progress)

    print(f"Downloaded {original_file_name}!")


failed_titles = []
def search_and_download_songs():
    user_profile_url = f"https://api.myanimelist.net/v2/users/{args.username}/animelist?limit=1000&status=completed"

    my_anime_list_response = requests.get(user_profile_url,
                                          headers={'X-MAL-CLIENT-ID': f'{args.client_id}'})

    delete_and_create_songs_directory()

    if my_anime_list_response.status_code == 200:
        my_anime_list_data = my_anime_list_response.json()
        user_animes = my_anime_list_data['data']
        # print("Response Data:", user_animes)
        for anime in user_animes:
            anime_url = f"https://api.myanimelist.net/v2/anime/{anime['node']['id']}?fields=id,title,alternative_titles,start_season"
            my_anime_list_detailed_response = requests.get(anime_url,
                                                           headers={
                                                               'X-MAL-CLIENT-ID': f'{args.client_id}'})
            if my_anime_list_detailed_response.status_code == 200:
                my_anime_list_detailed_data = my_anime_list_detailed_response.json()
                original_title = my_anime_list_detailed_data['title']
                original_season = my_anime_list_detailed_data['start_season']['season']
                original_year = my_anime_list_detailed_data['start_season']['year']
                # print(my_anime_list_detailed_data)

                anime_theme_url = f"https://api.animethemes.moe/search?page[limit]=1&fields[search]=anime&q={original_title}&include[anime]=animethemes.animethemeentries.videos"
                anime_theme_search_response = requests.get(anime_theme_url)
                anime_theme_search_data = anime_theme_search_response.json()
                anime_themes_first_result = anime_theme_search_data['search']['anime'][0]
                # print(anime_themes_first_result)

                if original_season.lower() == anime_themes_first_result['season'].lower() and original_year == \
                        anime_themes_first_result['year']:
                    # print(anime_theme_search_data)
                    print(f"Found {anime_theme_search_data['search']['anime'][0]['name']}!")
                    for anime_theme in anime_theme_search_data['search']['anime'][0]['animethemes']:
                        anime_theme_link = anime_theme['animethemeentries'][0]['videos'][0]['link']
                        file_name = anime_theme_link.split("/")[-1]

                        download_with_progress(anime_theme_link, "songs/" + file_name, file_name)
                else:
                    print("Initial search didn't work.")
                    print("Checking alternate title...")
                    anime_theme_url = f"https://api.animethemes.moe/search?page[limit]=1&fields[search]=anime&q={my_anime_list_detailed_data['alternative_titles']['en']}&include[anime]=animethemes.animethemeentries.videos"
                    anime_theme_search_response = requests.get(anime_theme_url)
                    anime_theme_search_data = anime_theme_search_response.json()
                    # print(anime_theme_search_data)
                    if "errors" in anime_theme_search_data:
                        print("Something went wrong with the search.")
                        failed_titles.append(original_title)
                        continue
                    anime_themes_first_result = anime_theme_search_data['search']['anime'][0]
                    if original_season.lower() == anime_themes_first_result['season'].lower() and original_year == \
                            anime_themes_first_result['year']:
                        # print(anime_theme_search_data)
                        print(f"Found {anime_theme_search_data['search']['anime'][0]['name']}!")
                        for anime_theme in anime_theme_search_data['search']['anime'][0]['animethemes']:
                            anime_theme_link = anime_theme['animethemeentries'][0]['videos'][0]['link']
                            file_name = anime_theme_link.split("/")[-1]

                            download_with_progress(anime_theme_link, "songs/" + file_name, file_name)
                    else:
                        print(f"Couldn't find {original_title}!")
                        failed_titles.append(original_title)
                        # print(original_title + " != " + anime_theme_search_data['search']['anime'][0]['name'])
            else:
                print("Failed to retrieve data:", my_anime_list_detailed_response.status_code)
            time.sleep(1)
    else:
        print("Failed to retrieve data:", my_anime_list_response.status_code)

    print("Sorry these titles couldn't be downloaded (maybe try and find them manually?): ")
    for failed_title in failed_titles:
        print(failed_title)


def delete_and_create_songs_directory():
    dir_path = f"{args.username}-songs"
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.makedirs(dir_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download all the anime themes off a profile from MAL!")
    parser.add_argument("username", help="The username of the profile you want to download songs from.")
    parser.add_argument("client_id", help="The client ID from your MAL (MyAnimeList).")

    args = parser.parse_args()

    search_and_download_songs()
