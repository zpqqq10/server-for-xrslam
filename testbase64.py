import base64, json
strs=None
# with open('luxun.png','rb') as f:
#     strs=base64.b64encode(f.read()).decode()
with open('frames/12-22 18-23-03.json', 'r') as f:
    strs = json.load(f)['image']

with open('test.png','wb') as f:
        f.write(base64.b64decode(strs))