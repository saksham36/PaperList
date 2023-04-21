#!/usr/bin/env python3.8
'''
Written by: Saksham Consul 04/05/2023
Script to run GPT on scraped data
'''

import os
import argparse
import tiktoken
import pandas as pd
import openai
import numpy as np
from openai.embeddings_utils import distances_from_embeddings, cosine_similarity
import matplotlib.pyplot as plt
from utils.data_handling import read_config


def main():
    config = read_config()
    openai.organization = config['openai']['organization']

    openai.api_key = config['openai']['api_key']
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--new', type=bool,
                        help='Create new embeddings', default=False)
    parser.add_argument('-q', '--question', help='Question to ask the model',
                        default='What is the latest methods for LLMs')
    args = parser.parse_args()

    if args.new:
        print("Creating Embeddings...")
        df = create_embeddings()
        print("Embeddings created")
    else:
        df = pd.read_csv('processed/embeddings.csv', index_col=0)
        df.columns = ['text', 'n_tokens', 'embeddings']
        df['embeddings'] = df.embeddings.apply(
            lambda x: np.array(x[1:-1].split(', ')).astype(float))

    print(answer_question(df, question=args.question, debug=False))


def create_embeddings(max_tokens=500):
    '''Creates embeddings for each chunk of text'''
    df = pd.read_csv('processed/scraped.csv')

    # Load the cl100k_base tokenizer which is designed to work with the ada-002 model
    tokenizer = tiktoken.get_encoding("cl100k_base")

    df = pd.read_csv('processed/scraped.csv', index_col=0)
    df.columns = ['title', 'text']

    # Tokenize the text and save the number of tokens to a new column
    df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))

    # Visualize the distribution of the number of tokens per row using a histogram
    fig = plt.figure()
    ax = df.n_tokens.hist()
    ax.set_xlabel('Number of tokens')
    ax.set_ylabel('Number of rows')
    try:
        os.mkdir('plots')
    except:
        pass
    fig.savefig('plots/n_tokens.png')

    # Split the text into chunks of a maximum number of tokens
    shortened = []

    # Loop through the dataframe
    for row in df.iterrows():

        # If the text is None, go to the next row
        if row[1]['text'] is None:
            continue

        # If the number of tokens is greater than the max number of tokens, split the text into chunks
        if row[1]['n_tokens'] > max_tokens:
            shortened += split_into_many(row[1]['text'], tokenizer, max_tokens)

        # Otherwise, add the text to the list of shortened texts
        else:
            shortened.append(row[1]['text'])

    df = pd.DataFrame(shortened, columns=['text'])
    df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))
    df.n_tokens.hist()

    # Get embeddings for each chunk of text
    df['embeddings'] = df.text.apply(lambda x: openai.Embedding.create(
        input=x, engine='text-embedding-ada-002')['data'][0]['embedding'])
    df.to_csv('processed/embeddings.csv')

    # Load the embeddings into a dataframe
    df = pd.read_csv('processed/embeddings.csv', index_col=0)
    df['embeddings'] = df['embeddings'].apply(eval).apply(np.array)
    print(df.head())
    return df


def split_into_many(text, tokenizer, max_tokens=500,):
    '''Function to split the text into chunks of a maximum number of tokens '''
    # Split the text into sentences
    sentences = text.split('. ')

    # Get the number of tokens for each sentence
    n_tokens = [len(tokenizer.encode(" " + sentence))
                for sentence in sentences]

    chunks = []
    tokens_so_far = 0
    chunk = []

    # Loop through the sentences and tokens joined together in a tuple
    for sentence, token in zip(sentences, n_tokens):

        # If the number of tokens so far plus the number of tokens in the current sentence is greater
        # than the max number of tokens, then add the chunk to the list of chunks and reset
        # the chunk and tokens so far
        if tokens_so_far + token > max_tokens:
            chunks.append(". ".join(chunk) + ".")
            chunk = []
            tokens_so_far = 0

        # If the number of tokens in the current sentence is greater than the max number of
        # tokens, go to the next sentence
        if token > max_tokens:
            continue

        # Otherwise, add the sentence to the chunk and add the number of tokens to the total
        chunk.append(sentence)
        tokens_so_far += token + 1

    # Add the last chunk to the list of chunks
    if chunk:
        chunks.append(". ".join(chunk) + ".")

    return chunks


def create_context(
    question, df, max_len=1800, size="ada"
):
    """
    Create a context for a question by finding the most similar context from the dataframe
    """

    # Get the embeddings for the question
    q_embeddings = openai.Embedding.create(
        input=question, engine='text-embedding-ada-002')['data'][0]['embedding']

    # Get the distances from the embeddings
    df['distances'] = distances_from_embeddings(
        q_embeddings, df['embeddings'].values, distance_metric='cosine')

    returns = []
    cur_len = 0

    # Sort by distance and add the text to the context until the context is too long
    for i, row in df.sort_values('distances', ascending=True).iterrows():

        # Add the length of the text to the current length
        cur_len += row['n_tokens'] + 4

        # If the context is too long, break
        if cur_len > max_len:
            break

        # Else add it to the text that is being returned
        returns.append(row["text"])

    # Return the context
    return "\n\n###\n\n".join(returns)


def answer_question(
    df,
    model="text-davinci-003",
    question="Am I allowed to publish model outputs to Twitter, without a human review?",
    max_len=1800,
    size="ada",
    debug=False,
    max_tokens=150,
    stop_sequence=None
):
    """
    Answer a question based on the most similar context from the dataframe texts
    """
    context = create_context(
        question,
        df,
        max_len=max_len,
        size=size,
    )
    # If debug, print the raw model response
    if debug:
        print("Context:\n" + context)
        print("\n\n")

    try:
        # Create a completions using the questin and context
        response = openai.Completion.create(
            prompt=f"Answer the question based on the context below, and if the question can't be answered based on the context, say \"I don't know\"\n\nContext: {context}\n\n---\n\nQuestion: {question}\nAnswer:",
            temperature=0,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=stop_sequence,
            model=model,
        )
        return response["choices"][0]["text"].strip()
    except Exception as e:
        print(e)
        return ""


if __name__ == "__main__":
    main()
