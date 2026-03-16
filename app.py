from flask import Flask, request, jsonify
from sample_data import sample_users
from recommendation_engine import (
    get_user_based_recommendations,
    get_item_based_recommendations,
    get_content_based_recommendations,
    get_hybrid_recommendations
)

app = Flask(__name__)

@app.route('/recommend')
def recommend():
    user_id = request.args.get('user_id')
    rec_type = request.args.get('type', 'hybrid')
    top_k = int(request.args.get('top_k', 5))
    user = next((u for u in sample_users if u.id == user_id), None)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    if rec_type == 'user':
        recs = get_user_based_recommendations(user, top_k)
        result = [r.__dict__ for r in recs]
    elif rec_type == 'item':
        recs = get_item_based_recommendations(user, top_k)
        result = [r.__dict__ for r in recs]
    elif rec_type == 'content':
        recs = get_content_based_recommendations(user, top_k)
        result = [r.__dict__ for r in recs]
    elif rec_type == 'hybrid':
        recs = get_hybrid_recommendations(user, top_k=top_k)
        result = [{**{'score': r['score'], 'sources': r['sources']}, **r['product'].__dict__} for r in recs]
    else:
        return jsonify({'error': 'Invalid recommendation type'}), 400
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True) 