import moviepy as mp

def create_test_video():
    # Use the test audio file we just created
    audio_path = "test_audio.wav"
    
    # Test monologue text
    monologue = "This is a test line. This is another test line. And this is the final test line."
    
    # Create a black background video
    audio_clip = mp.AudioFileClip(audio_path)
    video_duration = audio_clip.duration
    
    # Create a black background
    background = mp.ColorClip(size=(1920, 1080), color=(0, 0, 0), duration=video_duration)
    
    # Split monologue into lines for subtitles
    lines = monologue.split('. ')
    subtitle_clips = []
    
    # Calculate time per line
    time_per_line = video_duration / len(lines)
    
    # Create subtitle clips
    for i, line in enumerate(lines):
        if line.strip():  # Skip empty lines
            start_time = i * time_per_line
            end_time = (i + 1) * time_per_line
            
            try:
                # Create text clip with minimal parameters
                txt_clip = mp.TextClip(
                    line,
                    color='white'
                )
                
                # Set position and duration
                txt_clip = txt_clip.set_position('center').set_duration(end_time - start_time).set_start(start_time)
                subtitle_clips.append(txt_clip)
            except Exception as e:
                print(f"Error creating TextClip: {str(e)}")
                continue
    
    # Combine all clips
    final_video = mp.CompositeVideoClip([background] + subtitle_clips)
    final_video = final_video.set_audio(audio_clip)
    
    # Save the final video
    video_path = "test_video.mp4"
    final_video.write_videofile(video_path, fps=24, codec='libx264', audio_codec='aac')
    
    # Clean up
    audio_clip.close()
    final_video.close()
    
    print(f"Video created successfully at: {video_path}")

if __name__ == "__main__":
    create_test_video()
