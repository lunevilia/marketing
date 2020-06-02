from django.shortcuts import render
import requests
from django.conf import settings
from django.http import HttpResponse
import json
import numpy as np 

def extract_time(json): #딕셔너리 정렬
    try:
        return json["items"]["snippet"]["publishedAt"]
    except KeyError:
        return 0

# # lines.sort() is more efficient than lines = lines.sorted()
# lines.sort(key=extract_time, reverse=True)

# Create your views here.
def channel(request, token=None):
    params = {
        'key': settings.YOUTUBE_API_KEY,
        'part': 'snippet',
        'channelId': 'UCom6YhUY62jM52nIMjf5_dw',
        'type': 'video',
        'maxResults': '5',
        'order': 'date',
        'pageToken': token,
    }

    youtube_api_url = 'https://www.googleapis.com/youtube/v3/search'

    #session = requests.session()

    response = requests.get(youtube_api_url, params)
    response.raise_for_status() 
    response_dict = response.json()


    try:
        return render(request, 'youtube_detail.html', {'response_dict':response_dict['items'], 'pagetoken':response_dict['nextPageToken'], 'gettype':'video'})
    except:
        return render(request, 'youtube_detail.html', {'response_dict':response_dict['items'], 'pagetoken':'None', 'gettype':'video'})
    
# channeID를 바꾸면 플레이리스트가 channelID기준으로 된다
# ajax를 한꺼번에 playlist와 영상찾기를 2개 이용하고 있어서 같이 사용중
# youtubelayer.html에도 ajax를 if문으로 분기 시켰다!
def ajax(request, gettype, token):
    if request.is_ajax():
        params = {
            'key': settings.YOUTUBE_API_KEY,
            'part': 'snippet',
            'channelId': 'UCom6YhUY62jM52nIMjf5_dw',
            'type': gettype,
            'maxResults': '5',
            'order': 'date',
            'pageToken': token,
        }

        if gettype == "playlist": #플레이 리스트를 가져오는 ajax일 경우
            youtube_api_url = 'https://www.googleapis.com/youtube/v3/playlists'
        else: #그냥 동영상 가져오는 ajax일 경우
            youtube_api_url = 'https://www.googleapis.com/youtube/v3/search'

        response = requests.get(youtube_api_url, params)
        response.raise_for_status() 
        response_dict = response.json()
        
        if gettype == "playlist":
            youtube_api_url_playlist = 'https://www.googleapis.com/youtube/v3/playlistItems'

            gettitle = []

            for i in response_dict['items']:
                params2 = {
                    'key': settings.YOUTUBE_API_KEY,
                    'part': 'snippet',
                    'playlistId': i['id'],
                    'maxResults': '5',
                    'order': 'date', #안먹히고 쓸모 없지만 Ajax에서 2개를 가지고 있기 때문에 그냥 장식품으로 남겨놓음
                }

                response2 = requests.get(youtube_api_url_playlist, params2)
                response2.raise_for_status() 
                response_dict2 = response2.json()

                if(len(response_dict2["items"])>0): #플레이리스트에 비디오가 없을 경우
                    for j in response_dict2["items"]:
                        gettitle.append(j["snippet"]["title"])
                        gettitle.append(j["snippet"]["resourceId"]["videoId"])
                        try:
                            gettitle.append(j["snippet"]["thumbnails"]["high"])
                        except:
                            gettitle.append({"url":"https://www.blogcdn.com/wow.joystiq.com/media/2011/01/580nothing.jpg"})

                        i['added'] = np.array(gettitle).reshape(-1, 3).tolist()
                    
                    gettitle = []
                else:
                    continue
            
            #정렬하기 성공 (플레이리스트 순서 정렬) 문제 가져오는 처음 5개에서 정렬하는 것이기 때문에 전체가 아니다!! 전체 기준으로 정렬 하려면 maxResults를 늘려야 한다
            #예 ) 10 3 5 4 1 6 7 2 이런식인데 5개씩 가져와서 10 3 5 4 1 을 정렬하면 1 3 4 5 10이 되고 내보낸 다음에 남은 것 6 7 2를 가져와 정렬해서 2 6 7가 되서 결국 1 3 4 5 10 2 6 7 같이 된다
            response_dict["items"] = sorted(response_dict["items"], key=lambda x: (x["snippet"]["publishedAt"]), reverse=True)

    try:
        return HttpResponse(json.dumps({'response_dict':response_dict['items'], 'pagetoken':response_dict['nextPageToken']}), 'application/json')
    except:
        return HttpResponse(json.dumps({'response_dict':response_dict['items'], 'pagetoken':"None"}), 'application/json')

# channeID를 바꾸면 플레이리스트가 channelID기준으로 된다
def playlist(request, token=None):
    params = {
        'key': settings.YOUTUBE_API_KEY,
        'part': 'snippet',
        'channelId': 'UCom6YhUY62jM52nIMjf5_dw',
        'type': 'playlist',
        'maxResults': '5',
        'order': 'date',
        'pageToken': token,
    }

    youtube_api_url = 'https://www.googleapis.com/youtube/v3/playlists'

    response = requests.get(youtube_api_url, params)
    response.raise_for_status() 
    response_dict = response.json()

    youtube_api_url_playlist = 'https://www.googleapis.com/youtube/v3/playlistItems'

    gettitle = []

    for i in response_dict['items']: #플레이리스트 이름
        params2 = {
            'key': settings.YOUTUBE_API_KEY,
            'part': 'snippet',
            'playlistId': i['id'],
            'maxResults': '5',
            'order': 'date', #안먹히고 쓸모 없지만 Ajax에서 2개를 가지고 있기 때문에 그냥 장식품으로 남겨놓음
        }

        response2 = requests.get(youtube_api_url_playlist, params2)

        response2.raise_for_status() 
        response_dict2 = response2.json()

        if(len(response_dict2["items"])>0): #플레이리스트에 비디오가 없을 경우
            for j in response_dict2["items"]: #비디오
                gettitle.append(j["snippet"]["title"])
                gettitle.append(j["snippet"]["resourceId"]["videoId"])
                gettitle.append(j["snippet"]["thumbnails"]["high"])

                i['added'] = np.array(gettitle).reshape(-1, 3)
            
            gettitle = []
        else:
            continue
    
    #정렬하기 성공 (플레이리스트 순서 정렬) 문제 가져오는 처음 5개에서 정렬하는 것이기 때문에 전체가 아니다!! 전체 기준으로 정렬 하려면 maxResults를 늘려야 한다
    #예 ) 10 3 5 4 1 6 7 2 이런식인데 5개씩 가져와서 10 3 5 4 1 을 정렬하면 1 3 4 5 10이 되고 내보낸 다음에 남은 것 6 7 2를 가져와 정렬해서 2 6 7가 되서 결국 1 3 4 5 10 2 6 7 같이 된다
    response_dict["items"] = sorted(response_dict["items"], key=lambda x: (x["snippet"]["publishedAt"]), reverse=True)

    try:
        return render(request, 'youtube_information.html', {'response_dict':response_dict['items'], 'pagetoken':response_dict['nextPageToken'], 'gettype':'playlist',})
    except:
        return render(request, 'youtube_information.html', {'response_dict':response_dict['items'], 'pagetoken':'None', 'gettype':'playlist',})