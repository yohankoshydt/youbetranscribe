import openai
import streamlit as st
import whisper
from io import BytesIO

# Initialize Whisper model (small model for faster processing; you can use 'base' or 'large' for higher accuracy)
model = whisper.load_model("small")

# Set your OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]
# Function to transcribe audio or video using Whisper
def transcribe_audio(file_bytes):
    # Save the uploaded file temporarily
    with open("temp_file", "wb") as f:
        f.write(file_bytes)
    
    # Transcribe the audio using Whisper
    result = model.transcribe("temp_file")
    return result['text']

# Function to send transcript to GPT and generate questions
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
        print(f"Error communicating with OpenAI: {e}")
        return None

# Main function to handle file input and generate questions
def main():
    st.title("Audio/Video Transcription and Question Generator")

    # Upload audio or video file
    uploaded_file = st.file_uploader("Upload an audio or video file", type=["wav", "mp4", "mp3"])

    if uploaded_file is not None:
        st.write("Processing file...")

        # Read the file as bytes
        file_bytes = uploaded_file.read()

        # Transcribe the audio using Whisper
        transcript = transcribe_audio(file_bytes)
        st.write("Transcript:")
        st.write(transcript)

        # Generate questions from the transcript
        generate = st.button("Generate Questions")
        if generate:
            st.write("Generating questions from the transcript...")
            generated_questions = generate_questions_from_transcript(transcript)
            if generated_questions:
                st.write("Generated Questions:")
                st.write(generated_questions)
            else:
                st.write("No questions were generated.")
    else:
        st.write("Please upload an audio or video file.")

if __name__ == "__main__":
    main()
