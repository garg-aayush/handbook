# YouTube Video Summarizer

```
You are tasked with summarizing a YouTube video based on its transcript and chapter timestamps. Your goal is to provide concise summaries and key points for each chapter, as well as an overall summary of the entire video.

<video_title>
{{VIDEO_TITLE}}
</video_title>

<video_transcript>
{{VIDEO_TRANSCRIPT}}
</video_transcript>

<chapter_timestamps>
{{CHAPTER_TIMESTAMPS}}
</chapter_timestamps>

<instructions>
Analyze the transcript and timestamps carefully. For each chapter:
1. Identify the main topics discussed.
2. Summarize the key points and ideas presented.
3. Note any important facts, figures, or examples mentioned.

Then, create an overall summary of the entire video, highlighting the main themes and most significant points.
</instructions>

<output_format>
<chapter_summaries>
<chapter>
<title>[Chapter title]</title>
<summary>[2-3 sentence summary of the chapter]</summary>
<key_points>
- [Key point 1]
- [Key point 2]
- [Key point 3]
</key_points>
</chapter>
[Repeat for each chapter]
</chapter_summaries>

<overall_summary>
[Provide a 5-7 sentence summary of the entire video, highlighting the main themes and most significant points]
</overall_summary>

<key_takeaways>
- [Overall key takeaway 1]
- [Overall key takeaway 2]
- [Overall key takeaway 3]
[Up to a maximum of 5]
</key_takeaways>
</output_format>

Ensure that your summaries and key points are concise, informative and accurately reflect the content of the video. Focus on the most important information and avoid unnecessary details.
```
