import numpy as np
from PIL import Image
import os

def adjust_brightness(image, value):
    image_array = np.array(image)
    original_mode = image.mode
    if original_mode != "RGB":
        image = image.convert("RGB")
        image_array = np.array(image)
    image_array = image_array + value
    image_array = np.clip(image_array, 0, 255)
    image_array = image_array.astype(np.uint8)
    image = Image.fromarray(image_array)
    image = image.convert(original_mode)
    return image

def crop(image, left, top, right, bottom):
    image = image.crop((left, top, right, bottom))
    return image

def blur(image, radius, selection_area = None):
    image_array = np.array(image)
    if selection_area:
        left, top, right, bottom = selection_area
        sub_image_array = image_array[top:bottom, left:right]
        sub_height, sub_width = sub_image_array.shape[:2]
        blurred_sub_image_array = np.zeros_like(sub_image_array)
        print("Blurring the selected area...")
        for y in range(sub_height):
            for x in range(sub_width):
                x1 = max(0, x - radius)
                y1 = max(0, y - radius)
                x2 = min(sub_width - 1, x + radius)
                y2 = min(sub_height - 1, y + radius)
                neighbors = sub_image_array[y1:y2+1, x1:x2+1]
                average = np.mean(neighbors, axis=(0, 1))
                blurred_sub_image_array[y, x] = average
            
        image_array[top:bottom, left:right] = blurred_sub_image_array
    else:
        height, width = image_array.shape[:2]
        blurred_image_array = np.zeros_like(image_array)
        print("Blurring the whole image...")
        for y in range(height):
            for x in range(width):
                x1 = max(0, x - radius)
                y1 = max(0, y - radius)
                x2 = min(width - 1, x + radius)
                y2 = min(height - 1, y + radius)
                neighbors = image_array[y1:y2+1, x1:x2+1]
                average = np.mean(neighbors, axis=(0, 1))
                blurred_image_array[y, x] = average
        image_array = blurred_image_array
    print("Blurring done.")
    image = Image.fromarray(image_array)
    return image

def save_image(image, path = None, file_name = None):
    safe_path = "."
    safe_name = "modified_image"
    if path != None:
        safe_path = path
    if file_name != None:
        safe_name = file_name
    try:
        image.save(f"{safe_path}/{safe_name}")
        print(f"Image saved to {safe_path}/{safe_name}")
    except:
        print("An error occurred while saving the image. Please check the path and file name and try again.")



def main():
    valid_extensions = [".bmp", ".jpg", ".jpeg"]
    input_path = input("Enter the path of the input image (bmp/jpg/jpeg): ")
    _, extension = os.path.splitext(input_path)
    if extension.lower() not in valid_extensions:
        print("Invalid image format. Please enter a bmp, jpg, or jpeg image.")
        return
    try:
        image = Image.open(input_path)
    except:
        print("Invalid image path or format.")
        return
    print(f"Image opened from {input_path}")
    image.show()
    while True:
        print("---------------------------------")
        print("|    Welcome to Photo Editor    |")
        print("|   Fung Chun Wang  23019717D   |  ")
        print("|     Lo Ka Lam     23084548d   |  ")
        print("|    Yu Cheuk Bun   23093953d   |  ")
        print("--------------------------------- ")
        print("What function do you want to perform?")
        print("1. Adjust brightness")
        print("2. Crop")
        print("3. Blur")
        print("4. Save modified image")
        print("5. Exit")
        choice = input("Enter your choice (1/2/3/4/5): ")
        if choice == "1":
            while True:
                try:
                     value = int(input("Enter the brightness value to add or subtract (+/-): "))
                     break
                except ValueError:
                    print("Invalid brightness value. Please enter an integer.")
            image = adjust_brightness(image, value)
            image.show()

        elif choice == "2":
            while True:
                try:
                    left, top, right, bottom = map(int, input("Enter the left, top, right, and bottom coordinates(four integers separated by spaces): ").split())
                    break
                except ValueError:
                    print("Invalid crop coordinates. Please enter four integers separated by spaces.")
            image = crop(image, left, top, right, bottom)
            image.show()

        elif choice == "3":
            while True:
                try:
                    radius = int(input("Enter the blur radius: "))
                    break
                except ValueError:
                    print("Invalid blur radius. Please enter an integer.")
            selection = input("Do you want to blur a selected area? (y/n): ")
            if selection == "y":
                while True:
                    try:
                        left, top, right, bottom = map(int, input("Enter the left, top, right, and bottom coordinates of the selection area(four integers separated by spaces): ").split())
                        break
                    except ValueError:
                        print("Invalid selection area coordinates. Please enter four integers separated by spaces.")
                image = blur(image, radius, (left, top, right, bottom))
            elif selection == "n":
                image = blur(image, radius)
            else:
                print("Invalid choice. Please enter y or n.")
                continue
            image.show()
                
        elif choice == "4":
            output_path = input("Enter the path to save the modified image: ")
            output_name = input("Enter the file name to save the modified image: ")
            save_image(image, output_path, output_name)
        elif choice == "5":
            print("Thanks for using!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
