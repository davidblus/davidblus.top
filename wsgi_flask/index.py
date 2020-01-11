# -*- coding:utf-8 -*-

# python3 index.py
# curl http://0.0.0.0:5000/

from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from api_classes.hello_world import HelloWorld
from api_classes.invest_interest import AbchinaRmbGoldInterest
from api_classes.invest_interest import FundInterest

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://davidblus.top"}})
api = Api(app)

api.add_resource(HelloWorld, '/')
api.add_resource(AbchinaRmbGoldInterest, '/invest_interest/abchina_rmb_gold')
api.add_resource(FundInterest, '/invest_interest/fund')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
