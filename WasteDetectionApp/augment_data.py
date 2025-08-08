import os
import random
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array, save_img

# Augmentation configuration
datagen = ImageDataGenerator(
    rotation_range=25,
    width_shift_range=0.15,
    height_shift_range=0.15,
    shear_range=0.15,
    zoom_range=0.15,
    horizontal_flip=True,
    fill_mode='nearest'
)

# Base dataset directory
base_dir = 'newdataset'
target_total = 403  # Target number of images per class
image_format = 'jpg'  # Save format: 'jpg' or 'png'

# Function to augment images in one class folder
def augment_class_images(class_dir):
    images = [img for img in os.listdir(class_dir) if img.lower().endswith(('.jpg', '.jpeg', '.png'))]
    current_count = len(images)

    if current_count >= target_total:
        print(f"✅ '{class_dir}' already has {current_count} images. Skipping.")
        return

    needed = target_total - current_count
    print(f"🔄 Augmenting {needed} images in '{class_dir}'...")

    generated = 0
    while generated < needed:
        img_name = random.choice(images)
        img_path = os.path.join(class_dir, img_name)

        try:
            img = load_img(img_path)
            x = img_to_array(img)
            x = np.expand_dims(x, axis=0)

            # Generate one image at a time
            for batch in datagen.flow(x, batch_size=1):
                new_name = f"aug_{generated}_{random.randint(1000, 9999)}.{image_format}"
                save_path = os.path.join(class_dir, new_name)
                save_img(save_path, batch[0])
                generated += 1
                if generated >= needed:
                    break
        except Exception as e:
            print(f"❌ Error with {img_path}: {e}")

    print(f"✅ Done. Now '{class_dir}' has {current_count + generated} images.")

# Process both 'train' and 'val' folders
for subset in ['train', 'val']:
    subset_path = os.path.join(base_dir, subset)
    print(f"\n📁 Processing '{subset_path}'...")
    if not os.path.exists(subset_path):
        print(f"❌ Folder '{subset_path}' not found. Skipping.")
        continue

    for class_name in os.listdir(subset_path):
        class_dir = os.path.join(subset_path, class_name)
        if os.path.isdir(class_dir):
            augment_class_images(class_dir)

print("\n🎉 Augmentation complete for all datasets. Each class now has 403 images.")
