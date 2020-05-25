### IMPORTANT: 
- Make sure **word-counter** OpenFaaS function is deployed before deploying this application.
- Follow the steps on **README.md** file under **WORDS_COUNTER** folder

### Needed Helm Chart Values
| Parameter | Description | Default
| --- | --- | ---
| `config.logger.level` | application logger level | `INFO`
| `config.aws.bucketName` | AWS S3 bucket name | `None`
| `config.aws.regionName` | AWS region name | `None`
| `config.mysql.dbHost` | AWS RDS MySQL endpoint | `None`
| `config.mysql.dbDatabaseName` | AWS RDS MySQL database name | `None`
| `config.openFaas.wordsCounterUrl` | OpenFaaS word-counter function url | `http://gateway.openfaas:8080/function/word-counter`

### Needed Secrets
Add to **secrets.yaml** file inside **words-counter** helm application the following secrets encoded to base64:

| Parameter | Value
| --- | ---
| `AWS_ACCESS_KEY_ID` | `Your AWS Access Key ID`
| `AWS_SECRET_ACCESS_KEY` | `Your AWS Secret Access Key`
| `DB_USERNAME` | `AWS RDS MySQL username`
| `DB_PASSWORD` | `AWS RDS MySQL password`

### Build and Push the image
- ```docker build -t khjomaa/words-counter:1.0.0 .```
- ```docker push khjomaa/words-counter:1.0.0``` 

### Deploy the application
- ```helm upgrade --install <RELEASE NAME> ./helm/words-counter```

### Clean
- ```helm delete <RELEASE NAME>```