# TAKEDA SERVICE API
## Endpoints
### Upload Collection
* Description: Upload collection of PDFs to be processed, annotated, etc.
* Endpoint: <host>:<port>/upload
* Methods: POST
* Body:
    * files
    * collectionName

### List Collections
* Description: List available collections already uplaoded to be displayed.
* Endpoint: <host>:<port>/list
* Methods: GET
* Body:
    * None
