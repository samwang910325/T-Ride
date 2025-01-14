from quart import Quart, send_from_directory
from quart_cors import cors
import subprocess
from controller.matchController import match
from controller.orderController import order
from controller.userController import user
from controller.internalController import internal
from utils.config import Config

app = Quart(__name__)
app = cors(app, allow_origin='*')

@app.route('/health')
def health_check():
    # 在這裡可以加上一些檢查邏輯，確保應用程式的正常運作
    # 例如：檢查資料庫連線、外部服務是否可訪問等
    return 'OK'

@app.route('/Swagger/')
@app.route('/Swagger/<path:path>')
async def swagger(path=None):
    folder_path = 'Swagger'
    file_name = 'index.html'

    if path is None:
        response = await send_from_directory(folder_path, file_name)
    else:
        response = await send_from_directory(folder_path, path)

    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response
    

if __name__ == '__main__':
    app.register_blueprint(match, url_prefix='/match')
    app.register_blueprint(order, url_prefix='/order')
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(internal, url_prefix='/internal')
    app.run(host='0.0.0.0', port=int(Config.get('server').get('port')), debug=True)
