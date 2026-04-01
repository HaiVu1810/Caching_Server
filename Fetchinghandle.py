from fastapi import FastAPI,Response
import requests
import json
import os
app  = FastAPI()
def normalize_to_list(data):
    # Trường hợp 1: Dữ liệu đã là list (như JSONPlaceholder)
    if isinstance(data, list):
        return data
    
    # Trường hợp 2: Dữ liệu là dict (như DummyJSON)
    if isinstance(data, dict):
        # Tìm xem có key nào chứa list không (ví dụ: 'posts', 'carts', 'products')
        for value in data.values():
            if isinstance(value, list):
                return value
        # Nếu là dict nhưng không chứa list, bọc nó lại thành list 1 phần tử
        return [data]
    
    return []

@app.get("/{path:path}")
async def caching_proxy(path: str,response: Response):
    sub_path=None
    origin_url = os.getenv("ORIGIN_URL")
    site_name=origin_url.split("//")[-1].split("/")[0]
    print("origin_url:",origin_url)
    if path == "":
        full_url = origin_url
        cach__name="index"
    else:
        full_url = f"{origin_url}/{path}"
        path_split=path.strip("/").split("/")
        cach__name=path_split[0]
        if(len(path_split)>1):
            sub_path=path_split[1]
            # cache_path=f"cache/{cach__name+'_'+sub_path.replace('/', '_')}.json"
    cache_path=f"cache/{site_name+'_'+cach__name.replace('/', '_')}.json"
    try:
        print(f"Fetching URL: {full_url}")
        Get_url = requests.get(full_url)
        if(Get_url.status_code != 200):
            return {"error": f"Failed to fetch URL: {full_url}, status code: {Get_url.status_code}"}
        response={
        "content": Get_url.json() if 'application/json' in Get_url.headers.get('Content-Type', '') else Get_url.text,   
        "status_code": Get_url.status_code,
        "headers": {**dict(Get_url.headers),
                    "X-Cache": "Miss"
                    }
        }
        if not os.path.exists(cache_path) or os.path.getsize(cache_path) == 0:
            Temp_get_url = requests.get(f"{origin_url}/{cach__name}")
            Temp_response={
                "content": Temp_get_url.json() if 'application/json' in Temp_get_url.headers.get('Content-Type', '') else Temp_get_url.text,   
                "status_code": Temp_get_url.status_code,
                "headers": {**dict(Temp_get_url.headers),
                            "X-Cache": "Miss"
                            }
            }
            with open(cache_path, 'x') as f:
                print("Cache created successfully.")
                json.dump(Temp_response, f)
                # print(Get_url.json())
        elif os.path.exists(cache_path) and os.path.getsize(cache_path) > 0:
            with open(cache_path, 'r') as f:
                print("Cache hit, reading from cache.")
                cached_data = json.load(f)
                contetnt_fetch=normalize_to_list(cached_data["content"])
                if sub_path is not None:
                    target_item = next((item for item in contetnt_fetch if str(item.get("id")) == str(sub_path)), None)
                    response["content"] = target_item or {"message": "Not found"}
                else:
                    response["content"] = contetnt_fetch
                response["status_code"] = cached_data["status_code"]
                response["headers"] = cached_data["headers"]
                response["headers"]["X-Cache"] = "Hit"
        return response
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return {"error": str(e)}
