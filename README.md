# TAKEDA SERVICE API
## Endpoints
### Upload Collection
* Description: Upload collection of PDFs to be processed, annotated, etc.
* Endpoint: '<host>:<port>/upload/<string:collection_id>'
* Body:
    * files

Example:
```bash
curl localhost:5000/upload/pubmed_34 -d "dummyData= This is some dummy data."
```
