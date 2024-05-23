import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random

# Load data
user_df = pd.read_csv('users_large.csv')
post_df = pd.read_csv('posts_large_updated.csv')
interaction_df = pd.read_csv('interactions_large_updated.csv')
semantic_map_df = pd.read_csv('somatic_map.csv', delimiter=';', header=None)

# Process semantic map
tags = semantic_map_df.iloc[0, 1:].values
semantic_map_df = semantic_map_df[1:]
semantic_map_df.columns = ['Tag'] + list(tags)
semantic_map_df.set_index('Tag', inplace=True)

# Merge data for simplicity
data = pd.merge(interaction_df, post_df, on='Post')

# Check for NaN values in the Tags column and replace them with an empty string
post_df['Tags'] = post_df['Tags'].fillna('')

# TF-IDF Vectorizer
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(post_df['Tags'])

# Similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)


def get_semantic_similarity(tag1, tag2, semantic_map):
    if tag1 in semantic_map.index and tag2 in semantic_map.columns:
        return semantic_map.at[tag1, tag2]
    else:
        return 0


def get_recommendations(user_id, interaction_df, post_df, similarity_matrix, semantic_map, top_n=5):
    # Indices of interacted posts
    user_interactions = interaction_df[interaction_df['User'] == user_id]
    interacted_posts = user_interactions['Post'].tolist()
    interacted_indices = post_df[post_df['Post'].isin(interacted_posts)].index.tolist()

    # Sum of similarity scores
    sim_scores = np.sum(similarity_matrix[interacted_indices], axis=0)

    # Directly emphasize user's main interest
    user_tags = []
    for interacted_post in interacted_posts:
        user_tags.extend(post_df.loc[post_df['Post'] == interacted_post, 'Tags'].values[0].split(', '))

    main_interest = max(set(user_tags), key=user_tags.count)

    # Debugging: print user's main interest
    print(f"User {user_id}'s main interest: {main_interest}")

    # Adjust similarity scores with semantic map
    for idx, post in enumerate(post_df['Post']):
        if idx not in interacted_indices:
            tags = post_df.loc[idx, 'Tags'].split(', ')
            for tag in tags:
                if tag == main_interest:
                    sim_scores[idx] += 20  # Directly boost score for main interest tag
                for interacted_post in interacted_posts:
                    interacted_tags = post_df.loc[post_df['Post'] == interacted_post, 'Tags'].values[0].split(', ')
                    for interacted_tag in interacted_tags:
                        sim_scores[idx] += get_semantic_similarity(tag, interacted_tag, semantic_map)

    # Sort the scores
    sim_scores_indices = np.argsort(-sim_scores)

    # Avoid already interacted posts
    uninteracted_indices = [i for i in sim_scores_indices if post_df.iloc[i]['Post'] not in interacted_posts]

    # Directly add posts with the user's main interest
    main_interest_posts = post_df[post_df['Tags'].str.contains(main_interest, na=False)]
    main_interest_posts = main_interest_posts[~main_interest_posts['Post'].isin(interacted_posts)]
    main_interest_indices = main_interest_posts.index.tolist()

    # Combine the main interest posts with the other recommendations
    recommended_indices = main_interest_indices[:top_n] + [i for i in uninteracted_indices if
                                                           i not in main_interest_indices][
                                                          :top_n - len(main_interest_indices)]

    # Debugging: print tags of recommended posts
    recommended_posts = post_df.iloc[recommended_indices]
    print("Recommended posts and their tags:")
    print(recommended_posts[['Post', 'Tags']])

    return recommended_posts['Post'].tolist()


# Example usage
user_to_test = 'user2'
recommended_posts = get_recommendations(user_to_test, interaction_df, post_df, cosine_sim, semantic_map_df)
print(recommended_posts)