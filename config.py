# Label ids of the dataset
category_ids = {
    "rain": 0,
    "umbrella": 1,
    "person": 2,
    "lightning": 3,
    "cloud": 4,
    "pool": 5,
}

category_keys = {
    0: "rain",
    1: "umbrella",
    2: "person",
    3: "lightning",
    4: "cloud",
    5: "pool",
}


dataset_paths = {
    "quickdraw": "/your-path-to/quickdraw_dataset/format_ndjson/",
    "tu-berlin": "/your-path-to/tu_berlin/png/",
    "kaggle": "/your-path-to/dip_dataset/",
}


category_sample_paths = {
    "rain": [
        {"format": "ndjson", "dataset": "quickdraw",
            "path": dataset_paths["quickdraw"] + "rain.ndjson"}
    ],
    "umbrella": [
        {"format": "ndjson", "dataset": "quickdraw",
            "path": dataset_paths["quickdraw"] + "umbrella.ndjson"},
        {"format": "png", "dataset": "quickdraw",
            "path": dataset_paths["tu-berlin"] + "umbrella"}
    ],
    "person": [
        {"format": "png", "dataset": "tu-berlin",
         "path": dataset_paths["tu-berlin"]+"person walking"},
    ],
    "lightning": [
        {"format": "ndjson", "dataset": "quickdraw",
            "path": dataset_paths["quickdraw"] + "lightning.ndjson"}
    ],
    "cloud": [
        {"format": "ndjson", "dataset": "quickdraw",
            "path": dataset_paths["quickdraw"] + "cloud.ndjson"},
        {"format": "png", "dataset": "tu-berlin",
            "path": dataset_paths["tu-berlin"]+"cloud"}
    ],
    "pool": [
        {"format": "ndjson", "dataset": "quickdraw",
            "path": dataset_paths["quickdraw"] + "pool.ndjson"}
    ],
}

# Define which colors match which categories in the images
num_category = [1, 4, 9, 9, 9, 6]

category_colors = {}
category_colors['(255, 0, 0)'] = 0  # rain
for i in range(num_category[1]):  # num_umbrella
    p = (0 + i*10, 255, 0)
    category_colors[str(p)] = 1
for i in range(num_category[2]):  # num_person
    p = (0 + i*10, 0, 255)
    category_colors[str(p)] = 2
for i in range(num_category[3]):  # num_lightning
    p = (128 + i*10, 128, 255)
    category_colors[str(p)] = 3
for i in range(num_category[4]):  # num_cloud
    p = (255, 255, 0 + i*10)
    category_colors[str(p)] = 4
for i in range(num_category[5]):  # num_pool
    p = (255, 127, 39 + i*10)
    category_colors[str(p)] = 5
