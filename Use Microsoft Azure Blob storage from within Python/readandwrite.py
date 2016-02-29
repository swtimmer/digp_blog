#connect to your storage account
from azure.storage import BlobService
blob_service = BlobService(account_name='YourAccountName', account_key='YourKey')

#list all CSV files in your storage account

blobs = []
marker = None
while True:
    batch = blob_service.list_blobs('YourContainer', marker=marker, prefix='input_')
    blobs.extend(batch)
    if not batch.next_marker:
        break
    marker = batch.next_marker
for blob in blobs:
    print(blob.name)

#read the blob file as a text file
#I just read in the first from the pervious list

data = blob_service.get_blob_to_text('rockt', blobs[0].name).split("\n")
print("Number of lines in CSV " + str(len(data)))

#do your stuff
#I want to filter out some lines of my CSV and only keep those having ABC or DEF in them

matchers = ['abc', 'def']
matching = [s for s in data if any(xs in s for xs in matchers)]
print("Number of lines in CSV " + str(len(matching)))

#write your text directly back to blob storage

blob_service.put_block_blob_from_text(
    'YourContainer',
    'YourOutputFile.csv',
    ''.join(matching),
    x_ms_blob_content_type='text'
)
