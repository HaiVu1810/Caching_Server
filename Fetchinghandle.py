from fastapi import FastAPI,Response
import requests
import json
import os
app  = FastAPI()

@app.get("/{path:path}")
async def caching_proxy(path: str,response: Response):
# Lấy origin từ môi trường (ví dụ: https://dummyjson.com)
    origin_url = os.getenv("ORIGIN_URL")
    if path == "":
        full_url = origin_url
        sub_path=None
        cach__name="index"
    else:
        full_url = f"{origin_url}/{path}"
        path_split=path.strip("/").split("/")
        cach__name=path_split[0]
        if(len(path_split)>1):
            sub_path=path_split[1]
            print(sub_path)
        else:
            sub_path=None
        # print(cach__name)
    cache_path=f"cache/{cach__name.replace('/', '_')}.json"
    Get_url = requests.get(full_url)
    response={
        "content": Get_url.json() if 'application/json' in Get_url.headers.get('Content-Type', '') else Get_url.text,   
        "status_code": Get_url.status_code,
        "headers": {**dict(Get_url.headers),
                    "X-Cache": "Miss"
                    }
    }

    if not os.path.exists(cache_path) or os.path.getsize(cache_path) == 0:
        with open(cache_path, 'w') as f:
            print("Cache created successfully.")
            json.dump(response, f)
            # print(Get_url.json())
    elif os.path.exists(cache_path) and os.path.getsize(cache_path) > 0:
        with open(cache_path, 'r') as f:
            print("Cache hit, reading from cache.")
            cached_data = json.load(f)
            contetnt_fetch=cached_data["content"]
            if (cach__name in cached_data["content"]):
                contetnt_fetch=cached_data["content"][cach__name]
            if sub_path is not None:
                for item in contetnt_fetch:
                    if int(item["id"]) == int(sub_path):
                        response["content"] = item
                        break
            else:
                response["content"] = cached_data["content"]
            response["status_code"] = cached_data["status_code"]
            response["headers"] = cached_data["headers"]
            response["headers"]["X-Cache"] = "Hit"
    return response
