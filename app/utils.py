# app/utils.py

import cv2
import os



ALLOWED_EXTENSIONS = {'webp', 'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'uploads'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processImage(filename, format_conversion=None, image_processing=None):
    print(f"Format Conversion: {format_conversion}, Image Processing: {image_processing}, Filename: {filename}")
    img = cv2.imread(f"uploads/{filename}")

    if img is None:
        print(f"Failed to load image: uploads/{filename}")
        return None

    output_dir = "static/uploads"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    base = filename.rsplit('.', 1)[0]
    ext = filename.rsplit('.', 1)[1]

    # 1. Apply image processing if selected
    if image_processing:
        match image_processing:
            case "cgray":
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                base += "_gray"
            case "histeq":
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                img = cv2.equalizeHist(img)
                base += "_histeq"
            case "blur":
                img = cv2.GaussianBlur(img, (5, 5), 0)
                base += "_blurred"
            case "canny":
                img = cv2.Canny(img, 100, 200)
                base += "_edges"
            case "rotate":
                img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
                base += "_rotated"
            case "sharpen":
                kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
                img = cv2.filter2D(img, -1, kernel)

    file_format = filename.rsplit('.', 1)[1].lower()
    new_format = file_format

    # Handle Format Conversions Simultaneously also if required by user
    if format_conversion:
        if format_conversion == "cwebp":
            new_format= "webp"
        elif format_conversion == "cpng":
            new_format = "png"
        elif format_conversion == "cjpg":
            new_format = "jpg"
        elif format_conversion == "cjpeg":
            new_format = "jpeg"

    # --- Final output filename ---
    newFilename = f"static/{base}_processed.{new_format}"
    cv2.imwrite(newFilename, img)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),"..",newFilename)