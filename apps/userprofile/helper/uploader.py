import cloudinary.uploader

def uploader(image):
    """
    Upload image to cloudinary
    :param image: File from post request
    :return: uploaded image data if image was uploaded successfully else None
    """
    try:
        image_data = cloudinary.uploader.upload(
            image,
            public_id='smaple_id',
            crop='limiy',
            width=2000,
            height=2000,
            eager=[
                {'width': 200, 'height': 200,
                'crop': 'thumb', 'gravity': 'face',
                'radius': 20, 'effect': 'sepia'},
                {'width': 100, 'height': 150,
                 'crop': 'fit', 'format': 'png'}
            ]
        )
        return image_data
    except Exception as e:
        print(e)
        return None