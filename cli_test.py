from sample_data import sample_users
from recommendation_engine import (
    get_user_based_recommendations,
    get_item_based_recommendations,
    get_content_based_recommendations,
    get_hybrid_recommendations
)

def main():
    print("Available users:")
    for user in sample_users:
        print(f"{user.id}: {user.name} (preferences: {', '.join(user.preferences)})")
    user_id = input("Enter user ID: ").strip()
    user = next((u for u in sample_users if u.id == user_id), None)
    if not user:
        print("User not found.")
        return
    print("Recommendation types: user, item, content, hybrid")
    rec_type = input("Enter recommendation type: ").strip().lower()
    top_k = int(input("How many recommendations? (default 5): ") or "5")
    if rec_type == 'user':
        recs = get_user_based_recommendations(user, top_k)
    elif rec_type == 'item':
        recs = get_item_based_recommendations(user, top_k)
    elif rec_type == 'content':
        recs = get_content_based_recommendations(user, top_k)
    elif rec_type == 'hybrid':
        recs = get_hybrid_recommendations(user, top_k=top_k)
        recs = [r['product'] for r in recs]
    else:
        print("Invalid recommendation type.")
        return
    print(f"\nTop {top_k} recommendations for {user.name}:")
    for i, product in enumerate(recs, 1):
        print(f"{i}. {product.title} (Category: {product.category}, Avg Rating: {product.average_rating})")

if __name__ == "__main__":
    main() 