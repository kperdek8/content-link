import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Load semantic map from CSV file and ensure unique column names
def load_semantic_map(file_path):
    semantic_map_df = pd.read_csv(file_path, delimiter=';', header=0, index_col=0)
    return semantic_map_df.to_dict()


# Function to prepare TF-IDF matrix from a list of tags
def prepare_tfidf_matrix(tags_list):
    tags_series = pd.Series(tags_list).fillna('')
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(tags_series)
    return tfidf_matrix


# Function to get semantic similarity between two tags
def get_semantic_similarity(tag1, tag2, semantic_map):
    if tag1 in semantic_map and tag2 in semantic_map[tag1]:
        return semantic_map[tag1][tag2]
    else:
        return 0


# Function to get recommendations
def get_recommendations(user_id, posts, interactions, semantic_map, top_n=5):
    # Convert posts to DataFrame
    post_df = pd.DataFrame(list(posts.items()), columns=['Post', 'Tags'])
    post_df['Tags'] = post_df['Tags'].apply(lambda tags: ', '.join(tags))

    # Prepare the TF-IDF matrix from the tags list
    tags_list = post_df['Tags'].tolist()
    tfidf_matrix = prepare_tfidf_matrix(tags_list)

    # Similarity matrix
    similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Indices of interacted posts
    interacted_posts = [post.rstrip('/') for post in interactions[user_id]]
    interacted_indices = post_df[post_df['Post'].isin(interacted_posts)].index.tolist()

    # Sum of similarity scores
    sim_scores = np.sum(similarity_matrix[interacted_indices], axis=0)

    # Directly emphasize user's main interest
    user_tags = []
    for interacted_post in interacted_posts:
        user_tags.extend(posts[interacted_post])

    main_interest = max(set(user_tags), key=user_tags.count)

    # Debugging: print user's main interest
    print(f"User {user_id}'s main interest: {main_interest}", flush=True)

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
    recommended_indices = main_interest_indices + [i for i in uninteracted_indices if i not in main_interest_indices]

    # Limit the number of recommendations to top N
    recommended_indices = recommended_indices[:top_n]

    # Debugging: print tags of recommended posts
    recommended_posts = post_df.iloc[recommended_indices]
    print("Recommended posts and their tags:", flush=True)
    print(recommended_posts[['Post', 'Tags']], flush=True)

    return recommended_posts['Post'].tolist()
