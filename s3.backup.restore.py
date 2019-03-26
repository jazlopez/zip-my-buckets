import argparse
import subprocess
import tempfile
import logging
from utilsaws import aws_exec_endpoint
from utilsnapshot import compress, extract, get_snapshot_filename

logging.basicConfig(format="%(asctime)s [%(module)s - %(funcName)s:%(lineno)s] %(levelname)s: %(message)s", level=logging.INFO)


def archive(bucket=None,  **opts):
    """
    Backup: compress archived content from s3 bucket
    :param bucket
    :param **opts
    :return:
    """

    if not bucket:
        raise ValueError("required bucket name could not be found")

    if not bucket.startswith("s3://"):
        bucket = "s3://{0}".format(bucket)

    profile = opts.get('profile')
    timeout = int(opts.get('timeout'))

    if not profile:
        raise ValueError("required AWS profile name could not be found")

    logging.info("starting snapshot process for bucket: %s", bucket)

    try:

        with tempfile.TemporaryDirectory() as temp_s3_backup_space:

            logging.info("snapshot disk allocation: %s", temp_s3_backup_space)

            aws_exec = ['aws']
            aws_exec_opts = ['s3', 'cp', '--profile', profile, '--recursive', bucket, temp_s3_backup_space]
            aws_exec_endpoint_url = aws_exec_endpoint(opts)

            if aws_exec_endpoint_url:
                aws_exec.append(aws_exec_endpoint_url)

            for aws_exec_opt in aws_exec_opts:
                aws_exec.append(aws_exec_opt)

            spawn = subprocess.run(aws_exec, timeout=timeout, stdout=subprocess.DEVNULL)

            bucket_no_prefix = bucket.replace("://", "_")

            compress(get_snapshot_filename(resource=bucket_no_prefix), temp_s3_backup_space)

            logging.info("snapshot copy task return code %d", spawn.returncode)

    except Exception as e:
        raise RuntimeError(e)


def restore(from_archive=None, to_bucket=None, **opts):

    """
    Restore S3 files from archive snapshot
    :param from_archive:
    :param to_bucket:
    :param opts:
    :return:
    """

    profile = opts.get('profile')
    timeout = int(opts.get('timeout'))

    if not from_archive:
        raise ValueError("required zip filename could not be found")

    if not to_bucket:
        raise ValueError("required bucket name could not be found")

    if not profile:
        raise ValueError("required AWS profile name could not be found")

    if not to_bucket.startswith("s3://"):
        to_bucket = "s3://{0}".format(to_bucket)

    logging.info("starting restoring snapshot task")
    logging.info("from source file: %s", from_archive)
    logging.info("into bucket name: %s", to_bucket)

    try:

        with tempfile.TemporaryDirectory() as temp_s3_restore_space:

            logging.info("snapshot disk allocation: %s", temp_s3_restore_space)

            extract(zipname=from_archive, directory=temp_s3_restore_space)

            aws_exec = ['aws']
            aws_exec_opts = ['s3', 'cp', '--profile', profile,  '--recursive', temp_s3_restore_space, to_bucket]

            aws_exec_endpoint_url = aws_exec_endpoint(opts)

            if aws_exec_endpoint_url:
                aws_exec.append(aws_exec_endpoint_url)

            for aws_exec_opt in aws_exec_opts:
                aws_exec.append(aws_exec_opt)

            spawn = subprocess.run(aws_exec, stdout=subprocess.DEVNULL, timeout=timeout)

            if not spawn.returncode == 0:

                logging.warning("restoring snapshot task encountered an error with code :%d",
                                spawn.returncode)

                return

            logging.info("restoring snapshot task completed with code %d", spawn.returncode)

    except Exception as e:
        raise RuntimeError(e)


__version__ = "1.0.0"
__contrib__ = "Jaziel Lopez, jaziel.lopez@thermofisher"
__author__ = "TFC_Nutrias@thermofisher.com"

parser = argparse.ArgumentParser(description="s3 Backup Restore Tool")
parser.add_argument("--run", choices=["backup", "restore"],  required=True, help="Specify the operation to perform")
parser.add_argument("--bucket-name", help="Provide bucket name to backup/restore\n", required=True)
parser.add_argument("--archive", help="When operating in restore mode: absolute path to zip file to restore")
parser.add_argument("--profile", help="AWS profile authorization", required=True, default="default")
parser.add_argument("--timeout", help="Timeout", default=3600)
parser.add_argument("--with-endpoint", help="Optional: S3 URL endpoint", default="")
args = parser.parse_args()

try:
    if args.run == "backup":

        archive(bucket=args.bucket_name, timeout=args.timeout, profile=args.profile,
                with_endpoint=args.with_endpoint)

    if args.run == "restore":

        restore(from_archive=args.archive, to_bucket=args.bucket_name,
                profile=args.profile, timeout=args.timeout,  with_endpoint=args.with_endpoint)

except Exception as e:
    logging.error("Error %s", e)
    exit(1)

exit(0)
