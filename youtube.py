# -*- coding: utf-8 -*-
"""youtube.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1syqZVdJnj5jmGkzAcewf_GtiHrW6Vakd
"""

import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import BartTokenizer, BartForConditionalGeneration
def summarize_transcript(transcript):
    tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
    model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

    input_tensor = tokenizer.encode(transcript, return_tensors="pt", max_length=512, truncation=True)
    outputs_tensor = model.generate(input_tensor, max_length=160, min_length=120, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(outputs_tensor[0], skip_special_tokens=True)
    return summary

def main():
    st.title("YouTube Video Summarizer")
    video_url = st.text_input("Enter YouTube Video URL:", "")

    if st.button("Summarize"):
        if video_url:
            unique_id = video_url.split("=")[-1]
            try:
                transcript = YouTubeTranscriptApi.get_transcript(unique_id, proxies={"http": "http://mcjiohud:7xpdqm0wfvh8@206.41.172.74:6634"})
                subtitle = " ".join([x['text'] for x in transcript])
                summary = summarize_transcript(subtitle)
                st.write("**Summary:**")
                st.write(summary)
            except Exception as e:
                st.error(f"Error fetching transcript: {e}")
        else:
            st.error("Please enter a valid YouTube URL.")

if __name__ == "__main__":
    main()

