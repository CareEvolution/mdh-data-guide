import pandas as pd
import numpy as np  
import boto3
import time
import os
from datetime import datetime
import json

class MDHQuery:
    
    def __init__(
        self,
        project_schema_name: str, 
        athena_workgroup: str, 
        athena_output_bucket_location: str, 
        aws_profile_name: str = None, 
        query_result_temp_file_name: str = None
    ):

        self._project_schema_name = project_schema_name
        self._athena_workgroup = athena_workgroup
        self._athena_output_bucket_location = athena_output_bucket_location
        self._aws_profile_name = aws_profile_name
        self._query_result_temp_file_name = query_result_temp_file_name
        
        self.__aws_access_key_id = None
        self.__aws_secret_access_key = None
        self.__aws_session_token = None
      
    def get_query_result(self, query_string: str, _query_result_temp_file_name: str = None) -> pd.DataFrame:

        if self._aws_profile_name:
            session = boto3.session.Session(profile_name=self._aws_profile_name)

        else:    
            while not self.__aws_session_token:      
                self.__get_temporary_credentials_with_mfa()

            session = boto3.session.Session(
                aws_access_key_id=self.__aws_access_key_id,
                aws_secret_access_key=self.__aws_secret_access_key,
                aws_session_token=self.__aws_session_token
            )

        athena_client = session.client("athena", region_name="us-east-1")

        query_start = athena_client.start_query_execution(
            QueryString = query_string,
            QueryExecutionContext = {"Database": self._project_schema_name}, 
            WorkGroup = self._athena_workgroup,
            ResultConfiguration = {"OutputLocation": self._athena_output_bucket_location}
        )

        query_execution = athena_client.get_query_execution(QueryExecutionId=query_start["QueryExecutionId"])

        while query_execution["QueryExecution"]["Status"]["State"] in {"RUNNING", "QUEUED"}:
            print(time.strftime("%H:%M:%S", time.localtime()), f'query status: {query_execution["QueryExecution"]["Status"]["State"]}')
            time.sleep(5)
            query_execution = athena_client.get_query_execution(QueryExecutionId=query_start["QueryExecutionId"])

        print(time.strftime("%H:%M:%S", time.localtime()), f'query status: {query_execution["QueryExecution"]["Status"]["State"]}')

        if query_execution["QueryExecution"]["Status"]["State"] in {"FAILED"}:

            print(query_execution["QueryExecution"]["Status"]["StateChangeReason"] )

            return pd.DataFrame()

        else:
            result_uri = query_execution["QueryExecution"]["ResultConfiguration"]["OutputLocation"]
            bucket_name =  result_uri.split("/")[2]             

            s3_client = session.client("s3")

            file_location = (
                _query_result_temp_file_name if _query_result_temp_file_name 
                else self._query_result_temp_file_name if self._query_result_temp_file_name
                else "athena_query_results.csv"
            )

            s3_client.download_file(
                bucket_name,
                result_uri.replace(f"s3://{bucket_name}/", ""),
                file_location,
            )

            result_df = pd.read_csv(file_location)

            print(time.strftime("%H:%M:%S", time.localtime()), f"rows: {len(result_df.index)}", f"columns: {result_df.columns.to_list()}")

            return result_df

    def get_table(self, table_name: str, predicate: str = "") -> pd.DataFrame:

        return self.get_query_result(f"select * from {table_name} {predicate}")

    def __get_temporary_credentials_with_mfa(self) -> None:

        profile_name = input(f"Enter default profile name:")

        boto3.setup_default_session(profile_name=profile_name)

        sts_client = boto3.client("sts")
        user_name = sts_client.get_caller_identity()["Arn"].split("/")[1]

        iam_client = boto3.client("iam")
        mfa_device_serial_number = iam_client.list_mfa_devices(UserName=user_name)["MFADevices"][0]["SerialNumber"]

        token_code = input(f"Enter MFA code for {profile_name} device {mfa_device_serial_number}:")

        sts_client = boto3.client("sts")
        credentials = sts_client.get_session_token(SerialNumber=mfa_device_serial_number, TokenCode=token_code)["Credentials"]

        self.__aws_access_key_id = credentials["AccessKeyId"]
        self.__aws_secret_access_key = credentials["SecretAccessKey"]
        self.__aws_session_token = credentials["SessionToken"]
        
