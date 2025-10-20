### This should be in any files within this folder!! ###
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from imports import *
########################################################

if __name__ == "__main__":

    ## change this depending on your data
    df_cleaned = pd.read_csv(clean_curated_file)


    # ### IF YOU DON'T ALREADY HAVE THE MODEL (NO STOPWORDS)- use this
    # ### for model saving
    # os.makedirs("models", exist_ok=True)
    # ### load data
    # #### want to keep stopwords
    # # see https://maartengr.github.io/BERTopic/index.html#fine-tune-topic-representations 
    # topic_model = BERTopic(
    #     min_topic_size=10,
    #     calculate_probabilities=True
    # )
    # topics, probs = topic_model.fit_transform(df_cleaned['text'].tolist())
    # topic_model.save("models/bertopic_guyana_conversations_min10")

    # ## IF YOU DON'T ALREADY HAVE THE MODEL (WITH STOPWORDS)- use this
    # ### for model saving
    # os.makedirs("models", exist_ok=True)
    # ### load data
    # vectorizer_model = CountVectorizer(stop_words="english", min_df=2)
    # topic_model = BERTopic(
    #     vectorizer_model=vectorizer_model,
    #     min_topic_size=30,
    #     calculate_probabilities=True
    # )
    # topics, probs = topic_model.fit_transform(df_cleaned['text'].tolist())
    # topic_model.save("models/bertopic_CURATED_guyana_min30_with_stopwords")

    ## IF YOU ALREADY HAVE THE MODEL - use this
    # model_name = "models/bertopic_CURATED_guyana_min30_with_stopwords"
    # topic_model = BERTopic.load(model_name)
    # topic_info = topic_model.get_topic_info()
    # print(topic_info)

    # for topic_id in topic_info['Topic'][:10]:  # First 10 topics
    #     if topic_id != -1:  # Skip outlier topic
    #         words = topic_model.get_topic(topic_id)
    #         print(f"\nTopic {topic_id}: {words[:10]}")  # Top 10 words

    # print(f"\nNumber of documents per topic:")
    # print(topic_info[['Topic', 'Count', 'Name']])

    ##### if interested at looking at what documents are used for certain topics
    # topics = topic_model.topics_
    # df_with_topics = df_cleaned.copy()
    # df_with_topics['topic'] = topics
    # specific_topic = 12  ## change this based on list from display
    # topic_posts = df_with_topics[df_with_topics['topic'] == specific_topic]['text']

    # print(f"Posts in Topic {specific_topic}:")
    # for i, post in enumerate(topic_posts.head(10)):
    #     print(f"{i+1}: {post}")
    #     print("-" * 50)