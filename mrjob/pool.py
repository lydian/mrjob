# Copyright 2012 Yelp and Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Utilities related to job-flow-pooling. This code used to be in mrjob.emr.
"""
from datetime import datetime
from datetime import timedelta

try:
    import boto.utils
except ImportError:
    # don't require boto; MRJobs don't actually need it when running
    # inside hadoop streaming
    boto = None


def est_time_to_hour(job_flow, now=None):
    """How long before job reaches the end of the next full hour since it
    began. This is important for billing purposes.

    If it happens to be exactly a whole number of hours, we return
    one hour, not zero.
    """
    if now is None:
        now = datetime.utcnow()

    creationdatetime = getattr(job_flow, 'creationdatetime', None)
    startdatetime = getattr(job_flow, 'startdatetime', None)

    if creationdatetime:
        if startdatetime:
            start = datetime.strptime(startdatetime, boto.utils.ISO8601)
        else:
            start = datetime.strptime(job_flow.creationdatetime,
                                  boto.utils.ISO8601)
    else:
        # do something reasonable if creationdatetime isn't set
        return timedelta(minutes=60)
        
    run_time = now - start
    return timedelta(seconds=((-run_time).seconds % 3600.0 or 3600.0))
