import boto3
import config



def transfer_s3():
    
    s3 = boto3.resource('s3')

    copy_source = {
       'Bucket': 'maxh-msia423-project',
       'Key': 'raw/Seasons_Stats.csv'}

    s3.meta.client.copy(copy_source, config.DEST_BUCKET, config.DEST_KEY)



if __name__ == "__main__":

    transfer_s3()


