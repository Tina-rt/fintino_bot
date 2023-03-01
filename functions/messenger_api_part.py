from functions.string_res import *
from functions.algo import *

import requests, json, re

ACCESS_TOKEN = 'EAAzGFZBO1c4YBADFcXsHB66bZCzBolDAQwlk1G4Y0gY7U8xNhG8NbiDmMi3HJumFEpypGKgqABhWAsfuSqx6INlEfPBIsmGyp5DZB7gNZASISNjrXGeTdimN2H8ERUgEN2QNQYyR7NcZBZBFIIWkB2FNivmTPTdSsThXYBmktM3ZBG00zw5gRD4'
# ACCESS_TOKEN = 'EAA1wRuSPHuIBADjv4nmhWBWzFn78QFffqXZAyf5Sy0oxfH8F21Pqc3IRyURuHmADUNBJ5WqaJsoEelSFyzaLZAIZBuZAYHwaDZBNnAwRp7OFmkEYZCM7Yq9iYLXhKZANFtS5rEiySIeCZCIZAF6xZCaGDcGYnOxj1klR49VY861VS38wNl27LMromP'
URL = 'https://graph.facebook.com/v2.6/me/messages?access_token='+ACCESS_TOKEN

myUrl = 'https://6d44-197-159-148-241.eu.ngrok.io'
# myUrl = 'https://htbot2001.herokuapp.com'

def seen(dest_id):
    # print('typing_on')
    obj = {
      "recipient": {
        "id": dest_id
      },
      "sender_action": "mark_seen"
    }
    headers = {"Content-Type": "application/json"}
    r = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" +
                      ACCESS_TOKEN, data=json.dumps(obj), headers=headers)

def typing_on(dest_id):
	# print('typing_on')
	obj = {
	  "recipient": {
	    "id": dest_id
	  },
	  "sender_action": "typing_on"
	}
	headers = {"Content-Type": "application/json"}
	r = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" +
	                  ACCESS_TOKEN, data=json.dumps(obj), headers=headers)


def typing_off(dest_id):
	# print('typing_on')
	obj = {
	  "recipient": {
	    "id": dest_id
	  },
	  "sender_action": "typing_off"
	}
	headers = {"Content-Type": "application/json"}
	r = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" +
	                  ACCESS_TOKEN, data=json.dumps(obj), headers=headers)


def main_menu(dest_id):
    send_response_quickreply(dest_id, 'Que voulez vous faire ?', [
        {
            'content_type': 'text',
            'title': 'Google search',
            "payload": json.dumps({
                'menu': 'google',
                
            })
        },
        {
            'content_type': 'text',
            'title': 'Video',
            "payload": json.dumps({
                'menu': 'video',
                
            })
        },
        {
            'content_type': 'text',
            'title': 'Image',
            "payload": json.dumps({
                'menu': 'image',
                
            })
        },
        {
            'content_type': 'text',
            'title': 'Traduction',
            "payload": json.dumps({
                'menu': 'translate',
                
            })
        }


        ])

def send_translate_suggestion(dest_id, page=1):
    list_lang_n = show(list_lang, page, 5)
    pprint(list_lang_n)
    # payload = []
    # for lang in list_lang_n:
    # 	code = list_lang_dict[lang] == 'en'? 'gb':list_lang_dict[lang]
    # 	payload.append({
    #         'content_type': 'text',
    #         'title': f'{lang.capitalize()}',
    #         'image_url': f'https://www.countryflags.io/{code}/flat/16.png',	
    #         'payload': json.dumps({
    #             'query_lang': list_lang_dict[lang]
    #         	})
    #         })
    # send_response_quickreply(dest_id, 'Traduire en')
    code_gb = 'gb'
    send_response_quickreply(dest_id, 'Traduire en', [{
            'content_type': 'text',
            'title': f'{lang.capitalize()}',
            'image_url': f'https://www.countryflags.io/{code_gb if (list_lang_dict[lang] == "en") else list_lang_dict[lang]}/flat/16.png',	
            'payload': json.dumps({
                'query_lang': list_lang_dict[lang]
            })
        } for lang in list_lang_n
        
    ])

def send_img(dest_id, image_url):
    print('sending..')
    
    data = {
        "recipient": {
            "id": f"{dest_id}"
        },
        "message": {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": f"{image_url}",
                    "is_reusable": 'true'
                }
            }
        }
    }
    headers = {"Content-Type": "application/json"}
    r = requests.post("https://graph.facebook.com/v10.0/me/messages?access_token=" +
                      ACCESS_TOKEN, data=json.dumps(data), headers=headers)
    print(r.content)




def send_google_suggestion(dest_id, query, page=1):
    data = get_json_fb(dest_id, query, page=page)

    headers = {"Content-Type": "application/json"}
    r = requests.post(URL, data=json.dumps(data), headers=headers)
    typing_off(dest_id)
    print(r.content)

def send_video_suggestion(dest_id, query, page=1):
    list_video = getListVideo(query, page)
    typing_on(dest_id)
    current_list_video = list_video[:8]
    print(current_list_video)
    data = {
        "recipient": {
            "id": f'{dest_id}'
        },
        "messaging_type": "response",
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": f"{video['title']}",
                            "image_url": f"{video['thumbnail']}",
                            "subtitle": f"{video['duration']} - {video['viewCount']['short']}",

                            "buttons": [
                                {
                                    "type": "postback",
                                    "title": "Regarder",
                                    "payload": json.dumps({
                                        'watch': video['url']
                                    })
                                }, {
                                    "type": "postback",
                                    "title": "Ecouter",
                                    "payload": json.dumps({
                                        'listen': video['url']
                                    })
                                }
                            ]
                        } for video in current_list_video
                    ]
                },
                
            },
            "quick_replies": [
                {	
	                'content_type': 'text',
		    		'title': 'Page suivante',
		    		'payload': json.dumps({
		    			'page': page+1,
		    			'query': query
		    			})
    			}
            ]
            
        }
    }

    # send_response_quickreply(dest_id, '', [
    # 	{	'content_type': 'text',
    # 		'title': 'Page suivante',
    # 		'payload': json.dumps({'page': page+1})
    # 	}
    # ])

    # data['message']['quick_reply'] = [
    # 	{	'content_type': 'text',
    # 		'title': 'Page suivante',
    # 		'payload': {'page': page+1}
    # 	}
    # ]

    headers = {"Content-Type": "application/json"}
    r = requests.post(URL, data=json.dumps(data), headers=headers)
    typing_off(dest_id)
    print(r.content)
def send_response_quickreply(dest_id, reply, payloads):
	# print(reply)
	data = {
	  "recipient":{
	    "id":f"{dest_id}"
	  },
	  "messaging_type": "RESPONSE",
	  "message":{
	    "text": f"{reply}",
	    "quick_replies": payloads
	    
	  }
	}
	headers = {"Content-Type": "application/json"}
	r = requests.post(URL, data=json.dumps(data), headers=headers)
	print(r.content)

def sendText(dest_id, text):
    # typing_on(dest_id)
    data = {
        "recipient": {
            "id": f"{dest_id}"
        },
        "messaging_type": "RESPONSE",
        "message": {
            "text": f"{text}",

        }
    }
    headers = {"Content-Type": "application/json"}
    r = requests.post(URL, data=json.dumps(data), headers=headers)
    print(r.text)

    # typing_off(dest_id)
