from aiohttp import web
import json
from PIL import Image
import io
import numpy as np
import cv2


i = 0
async def apitest(request):
    print("request")
    result ={"status":"200"}
    return web.Response(text=json.dumps(result), status=200)

async def savePhoto(request):
    global i
    try:
        j = await request.json()
        dicts = [{k:v} for k,v in j.items()]
        name = dicts[0]
        photo = dicts[1]
        print(name['name'])
        npa= np.fromstring(bytes(photo['photo']),np.uint8)
        img = cv2.imdecode(npa,cv2.IMREAD_COLOR)
        cv2.imshow("caca",img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        # im2 = Image.new('RGB', (128,128))
        # im2.putdata(photo['photo'])
        # # Save the image.
        # image_name = r"fotosESP-" + str(i) + r".jpeg"
        # print('2')
        # im2.save(image_name, "JPEG") # Stored in images folder in the pwd, if not present then create one
        # print('3')
        # i+=1
        # print('4')
        # im2.show()
        print('5')
        #im = Image.open(StringIO(photo['photo']))
        #im.save(r'C:\Users\auror\OneDrive\Escritorio\fotosESP')
        return web.Response(text=json.dumps({'status': 'success'}), status=200)
    except Exception as e:
        print (e)
        response_obj = {'status': 'failed', 'reason': str(e)}
        web.Response(text=json.dumps(response_obj), status=500)

async def show(request):
    try:
        print("request")
        return web.Response(text=json.dumps({'data': 'success'}), status=200)
    except Exception as e:
        response_obj = {'status': 'failed', 'reason': str(e)}
        web.Response(text=json.dumps(response_obj), status=500)
app = web.Application()
app.router.add_get('/',apitest)
app.router.add_post('/save',savePhoto)
if __name__ == '__main__':
    web.run_app(app)