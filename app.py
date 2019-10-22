from flask import Flask, request, jsonify
from flask_restplus import Api, Resource, fields, marshal_with
import single_listing

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
                listing_data = single_listing.crawl(request.json['url'])
                return jsonify(listing_data)
            elif request.json['type'] == 'fsbo':
                return 'FSBO result'

        return {'message': 'Wrong parameters provided'}, 500


if __name__ == '__main__':
    app.run(debug=True)
