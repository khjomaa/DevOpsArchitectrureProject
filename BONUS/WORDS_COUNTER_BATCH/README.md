### Task:
Change code to limit all files to 3KB

**NOTES:** 
- Follow first same instructions in the basic solution to install OpenFaas and word-counter function
- Added to file **words_counter.py** a check that file size less or equal to 3KB by modifying the function **download_s3_bucket** as below:
```python
...
content_length = int(s3_obj['ResponseMetadata']['HTTPHeaders']['content-length'])
logger.info(f'Content-Length: {content_length}')
if content_length <= 3000:
...
```
- Built and pushed a new version **1.1.0**

### Build and Push the image
- ```docker build -t khjomaa/words-counter:1.1.0 .```
- ```docker push khjomaa/words-counter:1.1.0``` 

### Deploy the application
- ```helm upgrade --install <RELEASE NAME> ./helm/words-counter```

### Clean
- ```helm delete <RELEASE NAME>```