import sys
import subprocess

# Install fpdf2 if not installed
try:
    import fpdf
except ImportError:
    print("Installing fpdf2 library...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "fpdf2"])

from fpdf import FPDF

class PresentationPDF(FPDF):
    def __init__(self):
        # 16:9 Aspect Ratio: custom page size width=297mm, height=167.06mm
        super().__init__(orientation="L", unit="mm", format=(167.06, 297))
        self.set_margin(0)
        self.set_auto_page_break(False)

    def draw_slide_background(self, title):
        # Draw background color (sleek dark mode)
        self.set_fill_color(22, 24, 30) # Dark Charcoal
        self.rect(0, 0, 297, 167.06, "F")
        
        # Draw tech accents/side border (AMD theme color)
        self.set_fill_color(237, 85, 59) # Coral Orange Accent
        self.rect(0, 0, 8, 167.06, "F")
        
        # Draw Header
        self.set_font("helvetica", "B", 18)
        self.set_text_color(255, 255, 255)
        self.set_xy(20, 15)
        self.cell(0, 10, title, ln=True)
        
        # Draw footer
        self.set_font("helvetica", "I", 9)
        self.set_text_color(120, 125, 140)
        self.set_xy(20, 153)
        self.cell(0, 5, "AMD Developer Hackathon 2026 | Track 2: Video Captioning Agent", ln=False)
        self.set_xy(260, 153)
        self.cell(20, 5, f"Slide {self.page_no()}", align="R")

# Create presentation
pdf = PresentationPDF()

# --- Slide 1: Title ---
pdf.add_page()
# Override background for title slide to make it look special
pdf.set_fill_color(22, 24, 30)
pdf.rect(0, 0, 297, 167.06, "F")
# Top border accent
pdf.set_fill_color(237, 85, 59)
pdf.rect(0, 0, 297, 8, "F")

pdf.set_font("helvetica", "B", 36)
pdf.set_text_color(255, 255, 255)
pdf.set_xy(20, 45)
pdf.cell(0, 15, "AMD Captivate AI", ln=True)

pdf.set_font("helvetica", "B", 20)
pdf.set_text_color(237, 85, 59) # Orange Accent
pdf.set_xy(20, 62)
pdf.cell(0, 10, "Intelligent Video Understanding & Multi-Style Captioning", ln=True)

pdf.set_font("helvetica", "", 12)
pdf.set_text_color(180, 185, 200)
pdf.set_xy(20, 80)
pdf.multi_cell(240, 7, "A fully containerized batch video analysis platform built for Track 2 of the AMD Developer Hackathon 2026. Powered by Fireworks AI Qwen 3.7 Plus Vision models for high-efficiency, multi-style scene captioning.")

pdf.set_font("helvetica", "B", 12)
pdf.set_text_color(255, 255, 255)
pdf.set_xy(20, 112)
pdf.cell(0, 7, "Developer: Rishant (rishant78)", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("helvetica", "", 11)
pdf.set_text_color(150, 155, 170)
pdf.set_xy(20, 119)
pdf.cell(0, 7, "Docker Image Tag: rishant78/amd-captivate-ai:latest", new_x="LMARGIN", new_y="NEXT")
pdf.set_xy(20, 126)
pdf.cell(0, 7, "Docker Hub Link: https://hub.docker.com/r/rishant78/amd-captivate-ai", new_x="LMARGIN", new_y="NEXT", link="https://hub.docker.com/r/rishant78/amd-captivate-ai")


# --- Slide 2: Key Features ---
pdf.add_page()
pdf.draw_slide_background("Key Capabilities & Innovations")

# Feature 1
pdf.set_font("helvetica", "B", 13)
pdf.set_text_color(237, 85, 59)
pdf.set_xy(20, 32)
pdf.cell(0, 7, "1. Intelligent Keyframe Extraction", ln=True)
pdf.set_font("helvetica", "", 10.5)
pdf.set_text_color(200, 205, 220)
pdf.set_xy(20, 40)
pdf.multi_cell(250, 5.5, "- Duration-based adaptive sampling (e.g. extracts 15 frames for 30s - 2min videos).\n- Grayscale absolute pixel difference detection (dup removal) to prevent redundant API calls.\n- Drastically reduces Fireworks AI token consumption while maintaining coverage of unique visual events.")

# Feature 2
pdf.set_font("helvetica", "B", 13)
pdf.set_text_color(237, 85, 59)
pdf.set_xy(20, 70)
pdf.cell(0, 7, "2. Multi-Style Caption Generation", ln=True)
pdf.set_font("helvetica", "", 10.5)
pdf.set_text_color(200, 205, 220)
pdf.set_xy(20, 78)
pdf.multi_cell(250, 5.5, "- Produces one cohesive consolidated summary representing the video sequence.\n- Translates summary into 4 distinct styles: Formal, Sarcastic, Humorous-Tech, and Humorous-NonTech.\n- Exact JSON compliance for all requested styles ensures zero penalty scores.")

# Feature 3
pdf.set_font("helvetica", "B", 13)
pdf.set_text_color(237, 85, 59)
pdf.set_xy(20, 108)
pdf.cell(0, 7, "3. Complete Local Development Environment", ln=True)
pdf.set_font("helvetica", "", 10.5)
pdf.set_text_color(200, 205, 220)
pdf.set_xy(20, 116)
pdf.multi_cell(250, 5.5, "- Beautiful React 19 Frontend Web dashboard for interactive uploading, playing, and timeline scrubbing.\n- Real-time stepper updates with subtitle downloading options (SRT/TXT).\n- FastAPI backend serving responsive REST endpoints alongside the batch pipeline.")


# --- Slide 3: Architecture & Workflow ---
pdf.add_page()
pdf.draw_slide_background("System Architecture & Workflow")

# Draw flowchart boxes
pdf.set_fill_color(35, 38, 48)
pdf.set_draw_color(60, 64, 80)
pdf.set_text_color(255, 255, 255)
pdf.set_font("helvetica", "B", 11)

# Box 1: Input
pdf.rect(20, 42, 50, 22, "DF")
pdf.set_xy(20, 48)
pdf.cell(50, 10, "1. Input JSON", align="C")

# Box 2: OpenCV
pdf.rect(85, 42, 50, 22, "DF")
pdf.set_xy(85, 48)
pdf.cell(50, 10, "2. CV Keyframes", align="C")

# Box 3: Fireworks AI
pdf.rect(150, 42, 53, 22, "DF")
pdf.set_xy(150, 48)
pdf.cell(53, 10, "3. Vision AI Model", align="C")

# Box 4: Output
pdf.rect(220, 42, 50, 22, "DF")
pdf.set_xy(220, 48)
pdf.cell(50, 10, "4. Output JSON", align="C")

# Draw connection arrows
pdf.set_line_width(1)
pdf.set_draw_color(237, 85, 59)
pdf.line(70, 53, 85, 53)
pdf.line(135, 53, 150, 53)
pdf.line(203, 53, 220, 53)

# Description text below boxes
pdf.set_font("helvetica", "", 10.5)
pdf.set_text_color(180, 185, 200)
pdf.set_xy(20, 78)
pdf.multi_cell(250, 6, "- Step 1: Reads task parameters (video_url and styles) dynamically from mounted volume /input/tasks.json.\n- Step 2: Downloads video, runs OpenCV adaptive sampling, removes near-duplicate frames via grayscale pixel difference.\n- Step 3: Passes base64 images to Fireworks AI Qwen 3.7 VL, generates overall summary, and splits into 4 stylistic tones.\n- Step 4: Formats dictionary and writes results to /output/results.json before exiting cleanly.")


# --- Slide 4: Track 2 Batch Processing ---
pdf.add_page()
pdf.draw_slide_background("Track 2 Batch Processing & Compliance")

pdf.set_font("helvetica", "B", 13)
pdf.set_text_color(255, 255, 255)
pdf.set_xy(20, 32)
pdf.cell(0, 7, "Containerization & Evaluation Standards", ln=True)

pdf.set_font("helvetica", "", 10.5)
pdf.set_text_color(200, 205, 220)
pdf.set_xy(20, 42)
pdf.multi_cell(250, 6, "- Volume Mounting: Input tasks are parsed dynamically from /input/tasks.json and output is cleanly exported to /output/results.json.\n- Model Configuration: Powered by serverless Qwen 3.7 Plus Vision through Fireworks API, supporting robust scaling.\n- Strict Compliance: Exit code 0 signals flawless execution, and a non-zero code signals task-level pipeline errors.\n- Image Architecture: Compiled for linux/amd64 platforms to align with judging host requirements.")

pdf.set_fill_color(35, 38, 48)
pdf.rect(20, 95, 250, 42, "F")
pdf.set_font("helvetica", "B", 11)
pdf.set_text_color(237, 85, 59)
pdf.set_xy(25, 98)
pdf.cell(0, 5, "Verification Status:", ln=True)
pdf.set_font("helvetica", "", 10.5)
pdf.set_text_color(255, 255, 255)
pdf.set_xy(25, 106)
pdf.cell(0, 5, "- Built and pushed successfully to Docker Hub (rishant78/amd-captivate-ai:latest)", ln=True)
pdf.set_xy(25, 114)
pdf.cell(0, 5, "- Verified locally with Docker Desktop using official video clips", ln=True)
pdf.set_xy(25, 122)
pdf.cell(0, 5, "- Outputs matched schema for all 4 requested styles with zero errors", ln=True)

pdf.output("presentation.pdf")
print("Presentation PDF generated successfully at E:\\AMD Developer hakathon\\presentation.pdf!")
