# lofty-django-app

## Running a Development Copy

1. Clone this repo
2. Navigate to .devcontainer/ from project root
3. Execute "docker-compose up"
4. Application is served at host 127.0.0.1, port 8000

## API Reference

### KeyValue

* Create KeyValue With Key, Initialize Value at 0
  * POST /api/keys/
  * Expects: JSON {"key": key}
  * Returns: Created key and value, 201 on success

* Increment Value of Given Key
    * POST /api/keys/:key/increment
    * Expects: key as path parameter
    * Returns: Resulting key and value, 200 on success

* List All Keys and Values
    * GET /api/keys/list/
    * Expects:
    * Returns: All keys and values, 200 on success

### DogImage

* Generate Dog Images
    * POST /api/dogs/generate/
    * Expects: JSON {"key": key}
    * Returns: 200 on success

* Get Modified Dog Image
    * GET /api/dog/
    * Expects: 
    * Returns: Modified image url, original image url, original image metadata, 200 on success
