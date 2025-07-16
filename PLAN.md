# 🎬 OCT AI: Organic Chemistry Tutor Style Educational Video Generator

## 🎯 Vision

Create an AI system that generates educational videos in the style of "The Organic Chemistry Tutor" from any uploaded documents using RAG (Retrieval Augmented Generation). The system will produce step-by-step explanations with realistic handwriting animations and OCT-style narration.

## 🏗️ System Architecture

### Current Infrastructure ✅

- **Backend**: FastAPI with Google Gemini LLM
- **RAG System**: Vector retrieval with ChromaDB
- **Document Processing**: PDF text extraction
- **Frontend**: Next.js application
- **Database**: Vector database for document embeddings

### New Components to Add 🔨

#### 1. Animation Engine

- **Primary**: Manim Community Edition
- **Alternative**: Still-Manim (browser-based)
- **Backup**: Remotion (React-based)

#### 2. Voice Generation

- **Primary**: ElevenLabs (premium quality)
- **Alternative**: Murf AI or VocalCopyCat (cost-effective)
- **Style**: OCT's calm, methodical teaching voice

#### 3. Handwriting Simulation

- **Technique**: SVG path animation with stroke-dasharray
- **Implementation**: Manim's Write() animation
- **Enhancement**: AI-generated realistic handwriting paths

## 📋 Implementation Plan

### Phase 1: Basic Video Generation (Week 1-2)ene):

    def construct(self):
        # Title
        title = Text("{script['title']}", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Step-by-step content
        for step in script['steps']:
            text = Text(step['content'])
            self.play(Write(text))
            self.wait(step['pause_duration'])

            if step['type'] == 'equation':
                equation = MathTex(step['equation'])
                self.play(Write(equation))
                self.wait(1)
    """
    return manim_code

@app.post("/generate-animated-lesson")
async def generate_animated_lesson(request: LessonRequest):
content = retriever.invoke(request.topic)
script = generate_oct_script(content, request.topic)
visuals = generate_oct_visuals(script)
audio = generate_oct_voice(script)

    # Render video
    video_url = render_manim_video(visuals, audio)

    return {
        "script": script,
        "video_url": video_url,
        "manim_code": visuals
    }

````

### Phase 4: Advanced Features (Week 6-8)
- Realistic handwriting with pressure simulation
- Dynamic diagram generation
- Multi-step problem solving animations
- Interactive elements

## 🎨 OCT Style Guidelines

### Content Structure
```python
oct_prompt_template = """
You are The Organic Chemistry Tutor. Create a lesson on: {topic}
Based on this content: {content}

Use OCT's signature style:
- Start with "In this video, we're going to learn about..."
- Break into clear, numbered steps
- Use simple, methodical explanations
- Include example problems with step-by-step solutions
- End each section with "Let's move on to the next concept"
- Keep tone calm, patient, and encouraging
- Use phrases like "So we have..." and "Now let's..."
- Always show the work step by step
"""
````

### Visual Style

```python
oct_visual_style = {
    "background_color": "WHITE",
    "text_color": "BLACK",
    "handwriting_color": "BLUE",
    "emphasis_color": "RED",
    "font_family": "Arial", # Clean, readable font
    "equation_style": "handwritten",
    "animation_speed": "moderate", # Not too fast, not too slow
    "pause_between_steps": 1.5 # seconds
}
```

## 🛠️ Technical Stack

### Animation Libraries Comparison

| Library         | Pros                                            | Cons             | Best For                        |
| --------------- | ----------------------------------------------- | ---------------- | ------------------------------- |
| **Manim**       | Perfect for educational content, huge community | Complex setup    | Mathematical/scientific content |
| **Still-Manim** | Browser-based, outputs SVG                      | Static only      | Quick diagrams                  |
| **Remotion**    | React-based, modern                             | More web-focused | Dynamic content                 |
| **Monocurl**    | STEM-specific                                   | Beta software    | Mathematical presentations      |

### Voice Cloning Options

| Service          | Quality | Cost        | Features                      |
| ---------------- | ------- | ----------- | ----------------------------- |
| **ElevenLabs**   | Premium | $22/month   | Best quality, emotional range |
| **Murf AI**      | Good    | $29/month   | Educational presets           |
| **VocalCopyCat** | Good    | 90% cheaper | Budget alternative            |

## 📝 New API Endpoints

### 1. Lesson Generation

```python
class LessonRequest(BaseModel):
    topic: str
    difficulty_level: str = "beginner"  # beginner, intermediate, advanced
    duration_minutes: int = 10
    include_examples: bool = True
    style: str = "oct"  # organic_chemistry_tutor

@app.post("/api/lessons/generate")
async def generate_lesson(request: LessonRequest)
```

### 2. Video Creation

```python
class VideoRequest(BaseModel):
    lesson_id: str
    voice_enabled: bool = True
    animations_enabled: bool = True
    handwriting_style: str = "realistic"  # basic, realistic, calligraphy

@app.post("/api/videos/create")
async def create_video(request: VideoRequest)
```

### 3. Voice Customization

```python
class VoiceRequest(BaseModel):
    text: str
    voice_style: str = "oct"  # oct, professional, casual
    speed: float = 0.9
    clarity: float = 0.9

@app.post("/api/voice/generate")
async def generate_voice(request: VoiceRequest)
```

## 🎯 File Structure Updates

# Voice integration

def generate_oct_voice(script: str):
voice_settings = {
"voice_id": "oct_clone",
"stability": 0.8, # Consistent delivery
"clarity": 0.9, # Very clear pronunciation  
 "speed": 0.9 # Slightly slower for understanding
}
return text_to_speech(script, voice_settings)

@app.post("/generate-voiced-lesson")
async def generate_voiced_lesson(request: LessonRequest):
content = retriever.invoke(request.topic)
script = generate_oct_script(content, request.topic)
audio = generate_oct_voice(script)
return {"script": script, "audio_url": audio}
