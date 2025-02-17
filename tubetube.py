import streamlit as st
import re
import openai
from youtube_transcript_api import YouTubeTranscriptApi

# Set up OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Function to get video ID from YouTube URL
def get_video_id(youtube_url):
    pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, youtube_url)
    return match.group(1) if match else None

# Fetch available languages for transcripts
def get_available_languages(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        available_languages = {t.language_code: t.language for t in transcript_list}
        return available_languages
    except Exception as e:
        st.error(f"Error fetching languages: {e}")
        return {}

# Fetch transcript in the selected language
def get_transcript(video_id, selected_language):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[selected_language])
        return transcript
    except Exception as e:
        st.error(f"Error fetching transcript: {e}")
        return []

# Function to send transcript to ChatGPT and generate questions
def generate_questions_from_transcript(transcript_text):
    prompt = f"Create fill-in-the-blank and match-the-following type questions from this transcript: \n\n{transcript_text}\n"

    try:
        # Call OpenAI API 
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant and question creator for students."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except openai.error.OpenAIError as e:
        st.error(f"Error communicating with OpenAI: {e}")
        return None

# Main function
def main():
    st.title("YouTube Transcript to Questions Generator")

    # Input YouTube URL
    youtube_url = st.text_input("Enter the YouTube video link:")

    if youtube_url:
        video_id = get_video_id(youtube_url)
        if video_id:
            # Get available languages for the transcript
            available_languages = get_available_languages(video_id)
            
            if available_languages:
                st.write("Available languages:")
                for lang_code, lang_name in available_languages.items():
                    st.write(f"{lang_code}: {lang_name}")
                
                # Select the language
                selected_language = st.selectbox("Select the language code for the transcript:", list(available_languages.keys()))
                
                # Fetch and display the transcript
                if st.button("Fetch Transcript"):
                    transcript_data = get_transcript(video_id, selected_language)
                    if transcript_data:
                        transcript_text = " ".join([entry['text'] for entry in transcript_data])
                        st.write("\nTranscript:")
                        st.write(transcript_text)
                        
                        # Generate questions from transcript
                        if st.button("Generate Questions"):
                            st.write("\nGenerating questions...")
                            generated_questions = generate_questions_from_transcript(transcript_text)
                            if generated_questions:
                                st.write("\nGenerated Questions:")
                                st.write(generated_questions)
                            else:
                                st.write("No questions were generated.")
                    else:
                        st.write("No transcript found.")
            else:
                st.write("No available languages found.")
        else:
            st.write("Invalid YouTube URL.")

if __name__ == "__main__":
    main()
