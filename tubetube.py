import re
import openai
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi

# Set up OpenAI API key (replace with your actual key)
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

# Streamlit app
def main():
    st.title("YouTube Transcript to Questions Generator")
    
    # Input for YouTube URL
    youtube_url = st.text_input("Enter the YouTube video link:", "")
    
    # Use session_state to preserve state after button clicks
    if 'transcript_text' not in st.session_state:
        st.session_state.transcript_text = None
    if 'generated_questions' not in st.session_state:
        st.session_state.generated_questions = None
    
    if youtube_url:
        video_id = get_video_id(youtube_url)
        
        if video_id:
            # Fetch available languages
            available_languages = get_available_languages(video_id)
            
            if available_languages:
                selected_language = st.selectbox("Select language for transcript:", options=list(available_languages.keys()), format_func=lambda x: available_languages[x])
                
                # Fetch transcript when button is clicked
                if st.button("Fetch Transcript"):
                    transcript_data = get_transcript(video_id, selected_language)
                    
                    if transcript_data:
                        st.session_state.transcript_text = " ".join([entry['text'] for entry in transcript_data])
                
                # Show transcript if available
                if st.session_state.transcript_text:
                    st.subheader("Transcript:")
                    st.text_area("Transcript Text", st.session_state.transcript_text, height=200)
                    
                    # Generate questions button
                    if st.button("Generate Questions"):
                        st.write("Generating questions, please wait...")
                        st.session_state.generated_questions = generate_questions_from_transcript(st.session_state.transcript_text)
                
                # Display generated questions if available
                if st.session_state.generated_questions:
                    st.subheader("Generated Questions:")
                    st.write(st.session_state.generated_questions)
                    
            else:
                st.error("No available languages found.")
        else:
            st.error("Invalid YouTube URL.")

if __name__ == "__main__":
    main()
