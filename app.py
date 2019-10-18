from flask import Flask, request
from flask_restplus import Api, Resource, fields, marshal_with

app = Flask(__name__)
api = Api(app)


model = api.model('Model', {
    'type': fields.String(required=True,
                          description="zillow type",
                          help="type parameter cannot be blank."),
    'url': fields.Url(required=True,
                      description="zillow url",
                      help="url parameter cannot be blank.")
})


@api.route('/zillow')
class Zillow(Resource):
    @api.expect(model)
    def post(self):
        if 'url' not in request.json or not request.json['url'].startswith('https://www.zillow.com'):
            return {'message': 'Wrong URL provided'}, 500

        if 'type' in request.json:
            if request.json['type'] == 'single-listing':
                return 'Single Listing Result'
            elif request.json['type'] == 'fsbo':
                return 'FSBO result'

        return {'message': 'Wrong parameters provided'}, 500


if __name__ == '__main__':
    app.run(debug=True)
