from convokit import Corpus, download

if __name__ == "__main__":
    corpus = Corpus(download('subreddit-Guyana'))
    corpus.print_summary_stats()

    utt = corpus.random_utterance()

    print(utt)
