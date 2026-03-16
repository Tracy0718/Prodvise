from typing import List, Dict, Optional
from sample_data import User, Product, sample_users, sample_products
import math

def cosine_similarity(user_a: User, user_b: User) -> float:
    ratings_a = user_a.ratings
    ratings_b = user_b.ratings
    common_items = [item for item in ratings_a if item in ratings_b]
    if not common_items:
        return 0.0
    dot_product = sum(ratings_a[item] * ratings_b[item] for item in common_items)
    magnitude_a = math.sqrt(sum(ratings_a[item] ** 2 for item in common_items))
    magnitude_b = math.sqrt(sum(ratings_b[item] ** 2 for item in common_items))
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    return dot_product / (magnitude_a * magnitude_b)

def calculate_tfidf_similarity(product_a: Product, product_b: Product) -> float:
    features_a = set(product_a.features + product_a.category.split())
    features_b = set(product_b.features + product_b.category.split())
    intersection = features_a & features_b
    union = features_a | features_b
    return len(intersection) / len(union) if union else 0.0

def matches_user_interest(product: Product, user: User) -> bool:
    if not user.preferences:
        return True
    lower_prefs = [p.lower() for p in user.preferences]
    in_category = product.category.lower() in lower_prefs
    in_features = any(f.lower() in lower_prefs for f in product.features)
    in_tags = any(t.lower() in lower_prefs for t in (product.tags or []))
    return in_category or in_features or in_tags

def get_interest_fallback_products(user: User, top_k: int = 5) -> List[Product]:
    filtered = [p for p in sample_products if matches_user_interest(p, user)]
    filtered.sort(key=lambda p: p.average_rating, reverse=True)
    return filtered[:top_k]

def get_user_based_recommendations(target_user: User, top_k: int = 5) -> List[Product]:
    similarities = [
        (user, cosine_similarity(target_user, user))
        for user in sample_users if user.id != target_user.id
    ]
    similarities.sort(key=lambda x: x[1], reverse=True)
    top_similar = similarities[:3]
    recommended = {}
    for user, sim in top_similar:
        for product_id, rating in user.ratings.items():
            if product_id not in target_user.ratings:
                product = next((p for p in sample_products if p.id == product_id), None)
                if product:
                    if product_id not in recommended:
                        recommended[product_id] = {'score': 0, 'product': product}
                    recommended[product_id]['score'] += sim * rating
    recs = [v['product'] for v in sorted(recommended.values(), key=lambda x: x['score'], reverse=True)
            if matches_user_interest(v['product'], target_user)]
    if not recs:
        return get_interest_fallback_products(target_user, top_k)
    return recs[:top_k]

def get_item_based_recommendations(target_user: User, top_k: int = 5) -> List[Product]:
    user_rated = [p for p in sample_products if p.id in target_user.ratings]
    recommendations = {}
    for rated_product in user_rated:
        user_rating = target_user.ratings[rated_product.id]
        for product in sample_products:
            if product.id not in target_user.ratings:
                similarity = 0
                common_users = 0
                for user in sample_users:
                    if rated_product.id in user.ratings and product.id in user.ratings:
                        similarity += abs(user.ratings[rated_product.id] - user.ratings[product.id])
                        common_users += 1
                if common_users > 0:
                    sim_score = 1 / (1 + similarity / common_users)
                    if product.id not in recommendations:
                        recommendations[product.id] = {'score': 0, 'product': product}
                    recommendations[product.id]['score'] += sim_score * user_rating
    recs = [v['product'] for v in sorted(recommendations.values(), key=lambda x: x['score'], reverse=True)
            if matches_user_interest(v['product'], target_user)]
    if not recs:
        return get_interest_fallback_products(target_user, top_k)
    return recs[:top_k]

def get_content_based_recommendations(target_user: User, top_k: int = 5) -> List[Product]:
    user_rated = [p for p in sample_products if p.id in target_user.ratings]
    recommendations = {}
    for product in sample_products:
        if product.id not in target_user.ratings:
            total_similarity = 0
            weighted_rating = 0
            for rated_product in user_rated:
                similarity = calculate_tfidf_similarity(product, rated_product)
                user_rating = target_user.ratings[rated_product.id]
                total_similarity += similarity
                weighted_rating += similarity * user_rating
            if total_similarity > 0:
                score = weighted_rating / total_similarity
                recommendations[product.id] = {'score': score, 'product': product}
    recs = [v['product'] for v in sorted(recommendations.values(), key=lambda x: x['score'], reverse=True)
            if matches_user_interest(v['product'], target_user)]
    if not recs:
        return get_interest_fallback_products(target_user, top_k)
    return recs[:top_k]

def get_hybrid_recommendations(
    target_user: User,
    weights: Dict[str, float] = {'collaborative': 0.4, 'itemBased': 0.3, 'contentBased': 0.3},
    top_k: int = 10
) -> List[Dict]:
    user_based = get_user_based_recommendations(target_user, top_k)
    item_based = get_item_based_recommendations(target_user, top_k)
    content_based = get_content_based_recommendations(target_user, top_k)
    hybrid_scores = {}
    def add_to_hybrid(products, source, weight):
        for idx, product in enumerate(products):
            score = ((len(products) - idx) / len(products)) * weight
            if product.id not in hybrid_scores:
                hybrid_scores[product.id] = {'product': product, 'score': 0, 'sources': []}
            hybrid_scores[product.id]['score'] += score
            if source not in hybrid_scores[product.id]['sources']:
                hybrid_scores[product.id]['sources'].append(source)
    add_to_hybrid(user_based, 'User-Based CF', weights['collaborative'])
    add_to_hybrid(item_based, 'Item-Based CF', weights['itemBased'])
    add_to_hybrid(content_based, 'Content-Based', weights['contentBased'])
    hybrid = [v for v in hybrid_scores.values() if matches_user_interest(v['product'], target_user)]
    hybrid.sort(key=lambda x: x['score'], reverse=True)
    if not hybrid:
        return [{
            'product': p,
            'score': p.average_rating,
            'sources': ['Interest Fallback']
        } for p in get_interest_fallback_products(target_user, top_k)]
    return hybrid[:top_k]

def calculate_precision_at_k(predicted: List[Product], actual: List[Product], k: int) -> float:
    predicted_k = predicted[:k]
    actual_ids = {p.id for p in actual}
    relevant_retrieved = sum(1 for p in predicted_k if p.id in actual_ids)
    return relevant_retrieved / min(k, len(predicted_k)) if predicted_k else 0.0

def calculate_recall_at_k(predicted: List[Product], actual: List[Product], k: int) -> float:
    predicted_k = predicted[:k]
    actual_ids = {p.id for p in actual}
    relevant_retrieved = sum(1 for p in predicted_k if p.id in actual_ids)
    return relevant_retrieved / len(actual) if actual else 0.0

def calculate_ndcg(predicted: List[Product], actual: List[Product], k: int) -> float:
    predicted_k = predicted[:k]
    actual_ids = {p.id for p in actual}
    dcg = 0.0
    idcg = 0.0
    for idx, product in enumerate(predicted_k):
        relevance = 1 if product.id in actual_ids else 0
        dcg += relevance / math.log2(idx + 2)
    for i in range(min(k, len(actual))):
        idcg += 1 / math.log2(i + 2)
    return dcg / idcg if idcg > 0 else 0.0 