# Change working directory to main directory
import os
os.chdir('../../../')

from cortex.publisher_consumer.message_queue.message_queue_runner import run_message_queue

if "__main__" == __name__:
    run_message_queue()
