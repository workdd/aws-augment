import boto3
from PIL import Image, ImageFilter

return_bucket_name = 'aug-module'

TMP = "/tmp/"


def rotate90(image, file_name):
    path = TMP + "rotate-90-" + file_name
    img = image.transpose(Image.ROTATE_90)
    img.save(path)
    return path


def augmentation(file_name, image_path):
    image = Image.open(image_path)
    ret = rotate90(image, file_name)
    return ret


def handler(event, context):
    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        object_path = record['s3']['object']['key']
        tmp = '/tmp/' + object_path
        s3 = boto3.client('s3')
        s3.download_file(bucket_name, object_path, tmp)
        ret = augmentation(object_path, tmp)
        s3.upload_file(ret, return_bucket_name, ret.split('/')[2])
    print('rotate90')
    return 'rotate90'
