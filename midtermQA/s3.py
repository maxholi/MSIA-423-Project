import boto3
import config



def transfer_s3():
    
    s3 = boto3.resource('s3',
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key= config.AWS_SECRET_ACCESS_KEY)

    copy_source = {
       'Bucket': 'maxh-msia423-project',
       'Key': 'raw/Seasons_Stats.csv'}

    s3.meta.client.copy(copy_source, config.DEST_BUCKET, config.DEST_KEY)



if __name__ == "__main__":

    transfer_s3()


