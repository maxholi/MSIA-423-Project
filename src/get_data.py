import boto3
import yaml
import argparse

import logging

logger = logging.getLogger(__name__)



def get_destination_s3(dest_bucket):

    """ return configuration for S3 bucket to store the raw data
    Args:
        dest_bucket (dict): dictionary containing bucket name and path to raw data file
    Returns:
        dest (dict): dicitonary contianing the bucket name and path to raw data file
    """

    logger.info("get the configuration paramters of the destination bucket in S3")
    dest = dest_bucket


    return dest


def transfer_s3(source, **kwargs):

    """ function to transfer data from the raw source (s3) to another predconfigured s3 bucket
    Args:
        source( dictionary): dictionary containing the bucket name and path for the raw data in S3
        **kwargs: calls get_destination_s3 function to return the parameters of the destination bucket
    Returns:
        None
    """
    s3 = boto3.resource('s3')

    dest = get_destination_s3(**kwargs['get_destination_s3'])

    dest_bucket = dest['Bucket']
    dest_key = dest['Key']

    # transfer data from one S3 bucket to another
    try:
        s3.meta.client.copy(source, dest_bucket, dest_key)
    except:
        logger.error("unable to download the file, check to make file path is correct in the bucket and/or download path exists in your file system")



def get_s3(download_path,**kwargs):

    """
    Download data from an S3 bucket into local

    Args:
        download_path (str): path to downloaded file on local
        **kwargs: calls get_destination_s3 function to return the parameters of the destination bucket
    Returns:
        None

    """

    # configure s3
    s3 = boto3.resource('s3')

    dest = get_destination_s3(**kwargs['get_destination_s3'])

    bucket = dest['Bucket']
    file_path = dest['Key']

    # assign bucket to variable
    bucket = s3.Bucket(bucket)
    try:
        # download data from s3 into specified download_path on local
        bucket.download_file(file_path, download_path)
    except:
        logger.error("unable to download the file, check to make file path is correct in the bucket and/or download path exists in your file system")

def run_get_s3(args):

    """ runs the data download from s3 via args in the command line"""

    ## open YAML file containing parameters to run download from s3
    with open(args.config, "r") as f:
        config = yaml.load(f)

    ## download data from s3 via parameters in the YAML file
    config_s3 = config['get_data']

    # transfer and then download
    transfer_s3(**config_s3['transfer_s3'])
    get_s3(**config_s3['get_s3'])


if __name__ == "__main__":

    ## configure command line syntax to be used in running the data download from s3 process

    parser = argparse.ArgumentParser(description="get raw data from s3")
    parser.add_argument('--config', help='path to yaml file with configurations', default="config/config.yml")

    args = parser.parse_args()

    run_get_s3(args)



