import json
import sys
import requests
from aiohttp_sse_client import client as sse_client
import asyncio

API_BASE_URL = "CHATCAT_API_ENDPOINT"

common_headers = {
    'Authorization': 'Bearer YOUR_TOKEN',
    'Content-type': 'application/json',
    'Accept': 'application/json'
}


async def event_listener():
    url = '{}/chats/messages/events'.format(API_BASE_URL)
    sse_headers = {**common_headers,
                   'Accept': 'text/event-stream',
                   'Content-Type': 'text/event-stream'
                   }
    async with sse_client.EventSource(url, headers=sse_headers) as event_source:
        try:
            async for event in event_source:
                data = json.loads(event.data)
                if data['finished'] == False:
                    sys.stdout.write(data['message']['content'])
                    sys.stdout.flush()
                else:
                    print()
        except ConnectionError:
            print("Connection error")


async def add_message():
    url = "{}/chats/messages".format(API_BASE_URL)
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": "你是谁"
            }
        ]
    })
    response = requests.post(url, headers=common_headers, data=payload)
    print(response.text)


async def main():
    try:
        await asyncio.gather(event_listener(), add_message())
    except Exception as e:
        print(f"Exception occurred: {e}")

if __name__ == '__main__':
    asyncio.run(main())
