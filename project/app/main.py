from PIL import Image
import numpy as np

def convert_to_grayscale(input_image_path, output_image_path):
    image = Image.open(input_image_path)
    grayscale_image = image.convert("L")
    grayscale_image.save(output_image_path)
    image.close()
    
def bradley_roth_thresholding(image_array, window_size=15, threshold=0.15):
    height, width = image_array.shape
    
    output_image = np.zeros((height, width), dtype=np.uint8)
    
    for i in range(height):
        for j in range(width):
            x_start = max(0, i - window_size // 2)
            x_end = min(height, i + window_size // 2 + 1)
            y_start = max(0, j - window_size // 2)
            y_end = min(width, j + window_size // 2 + 1)
            
            window = image_array[x_start:x_end, y_start:y_end]
            
            mean = np.mean(window)
            
            if image_array[i, j] < mean * (1 - threshold):
                output_image[i, j] = 0
            else:
                output_image[i, j] = 255
    return output_image

if __name__ == "__main__":
    input_path = "app\\models\\imageTest.jpeg"  
    output_path = "app\\models\\imageRes.jpg"
    
    convert_to_grayscale(input_path, output_path)

    image = Image.open(output_path)
    image_array = np.array(image)
    binary_image = bradley_roth_thresholding(image_array, window_size=35)
    result_image = Image.fromarray(binary_image)
    result_image.save("app\\models\\binary_image.jpg")
    image.close()
