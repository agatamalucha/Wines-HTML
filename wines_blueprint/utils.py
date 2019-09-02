#######    UPLOADING FILE PROCESS    ######

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])  # 1. the only file extensions (images) allowed into bucket of files on AWS


# 2. Function below is checking if file extensions for files we want to upload belongs to the allowed extensions in the list above
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS  # converting capital letters into lower key an checking if extension is allowed


# 3.
def upload_file_to_s3(file, bucket_name, acl="public-read"):
    try:  # Use "try" function otherwise if sth goes wrong , user won't know if there is any error

        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:  # Use "except" to print error on the screen and prevent app from crashing
        print("Something Happened: ", e)
        return e

    return "{}{}".format(app.config["S3_LOCATION"], file.filename)
