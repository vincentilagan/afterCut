import os
from tkinter import Tk, filedialog, Button, Label, Frame
from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector

# Sensitivity for scene detection
THRESHOLD = 30.0

def process_video():
    video_file = filedialog.askopenfilename(
        title="Select your video",
        filetypes=[("MP4 files", "*.mp4")]
    )
    if not video_file:
        return

    status_label.config(text="⏳ Processing... Please wait.")
    root.update_idletasks()

    folder = os.path.dirname(video_file)
    base_name = os.path.splitext(os.path.basename(video_file))[0]
    jsx_file = os.path.join(folder, base_name + ".jsx")  # Save in same folder

    # Scene detection
    video_manager = VideoManager([video_file])
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=THRESHOLD))
    video_manager.start()
    scene_manager.detect_scenes(frame_source=video_manager)
    scenes = scene_manager.get_scene_list()
    video_manager.release()

    print(f"Detected {len(scenes)} cuts in {video_file}")

    # --- JSX script ---
    jsx_header = """
var comp = app.project.activeItem;
if (comp == null || !(comp instanceof CompItem)) {
    alert("Please select a composition with your video layer.");
} else {
    var layer = comp.layer(1);
    var markerProp = layer.property("Marker");
    var w = comp.width;
    var h = comp.height;
    var pa = comp.pixelAspect;
    var fr = comp.frameRate;
"""

    jsx_body = ""

    # Place markers at scene change points
    for i, scene in enumerate(scenes[:-1]):
        seconds = scene[1].get_seconds()
        jsx_body += f"    markerProp.setValueAtTime({seconds}, new MarkerValue('Cut {i+1}'));\n"

    # Create precomps from markers
    jsx_body += """
    // Create precomps for each cut and place them in timeline
    for (var i = 1; i <= markerProp.numKeys; i++) {
        var startTime = (i === 1) ? 0 : markerProp.keyTime(i - 1);
        var endTime = markerProp.keyTime(i);
        var duration = endTime - startTime;

        var cutComp = app.project.items.addComp('Cut_' + i, w, h, pa, duration, fr);
        var newLayer = cutComp.layers.add(layer.source);
        newLayer.startTime = -startTime;

        var precompLayer = comp.layers.add(cutComp);
        precompLayer.startTime = startTime;
    }

    // Handle last segment after last marker
    if (markerProp.numKeys > 0) {
        var lastStart = markerProp.keyTime(markerProp.numKeys);
        var lastDur = comp.duration - lastStart;
        if (lastDur > 0.01) {
            var cutCompLast = app.project.items.addComp('Cut_' + (markerProp.numKeys + 1), w, h, pa, lastDur, fr);
            var newLayerLast = cutCompLast.layers.add(layer.source);
            newLayerLast.startTime = -lastStart;

            var precompLayerLast = comp.layers.add(cutCompLast);
            precompLayerLast.startTime = lastStart;
        }
    }
"""

    jsx_footer = "\n}"

    with open(jsx_file, "w", encoding="utf-8") as f:
        f.write(jsx_header + jsx_body + jsx_footer)

    print(f"✅ JSX script created: {jsx_file}")
    status_label.config(text=f"✅ Done! JSX created: {jsx_file}")

# --- GUI ---
root = Tk()
root.title("AfterCut - AE Auto-Cut Generator")
root.geometry("500x250")
root.resizable(False, False)
root.configure(bg="black")

frame = Frame(root, bg="black", padx=20, pady=20)
frame.pack(expand=True, fill="both")

ae_blue = "#00ADEF"
ae_orange = "#FF6A00"
status_green = "#00FF7F"
footer_gray = "#AAAAAA"

header_label = Label(
    frame, text="AfterCut - AE Auto-Cut Generator",
    font=("Helvetica", 18, "bold"), fg=ae_blue, bg="black"
)
header_label.pack(pady=(0, 20))

upload_button = Button(
    frame, text="Upload Your Video", command=process_video,
    width=30, height=2, bg=ae_orange, fg="white", activebackground=ae_blue, activeforeground="white"
)
upload_button.pack(pady=10)

status_label = Label(frame, text="", font=("Helvetica", 10), fg=status_green, bg="black")
status_label.pack(pady=10)

footer_label = Label(frame, text="Created by Vincent Ilagan", font=("Helvetica", 10, "italic"), fg=footer_gray, bg="black")
footer_label.pack(side="bottom", pady=(15,0))

root.mainloop()
