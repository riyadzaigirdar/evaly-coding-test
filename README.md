# evaly-coding-test

#### get excel download link
    
    curl --location --request GET 'http://127.0.0.1:8000/loans/get-excel-for-loans'
    
#### Response
    
    {
        "download_link": "http://127.0.0.1:8000/media/loans.csv"
    }

#### Browse books

    curl --location --request GET 'http://127.0.0.1:8000/browse/books' \
    --data-raw ''

#### Response
    [
      {
          "id": 1,
          "name": "Harry Potter",
          "description": "And that's it. DRF will call this method to get queryset, filter it as configured, and serialize the data with your serializer automatically. No need to manually implement what's already provided.",
          "author": {
              "id": 1,
              "name": "John Doe",
              "location": "Chittagong",
              "publised_books": [
                  {
                      "book_id": 1,
                      "book_name": "Harry Potter"
                  },
                  {
                      "book_id": 2,
                      "book_name": "Social Science"
                  }
              ]
          },
          "created_at": "2021-03-06T08:23:59.182842Z",
          "last_update": "2021-03-06T08:33:06.181384Z",
          "is_publised": true
      },
      {
          "id": 2,
          "name": "Social Science",
          "description": "search specifies the pattern that needs to be matched. search_fields specify the database ... This will come in handy in a scenario where your front end lists all the ... When we send a pattern in a GET query parameter, we want the term to be",
          "author": {
              "id": 1,
              "name": "John Doe",
              "location": "Chittagong",
              "publised_books": [
                  {
                      "book_id": 1,
                      "book_name": "Harry Potter"
                  },
                  {
                      "book_id": 2,
                      "book_name": "Social Science"
                  }
              ]
          },
          "created_at": "2021-03-06T08:33:37.590310Z",
          "last_update": "2021-03-06T08:33:37.590372Z",
          "is_publised": true
      }
    ]
    
#### search books using ?search query 

    curl --location --request GET 'http://127.0.0.1:8000/browse/books?search=Harry' \
    --data-raw ''
    
#### response
    [
      {
          "id": 1,
          "name": "Harry Potter",
          "description": "And that's it. DRF will call this method to get queryset, filter it as configured, and serialize the data with your serializer automatically. No need to manually implement what's already provided.",
          "author": {
              "id": 1,
              "name": "John Doe",
              "location": "Chittagong",
              "publised_books": [
                  {
                      "book_id": 1,
                      "book_name": "Harry Potter"
                  },
                  {
                      "book_id": 2,
                      "book_name": "Social Science"
                  }
              ]
          },
          "created_at": "2021-03-06T08:23:59.182842Z",
          "last_update": "2021-03-06T08:33:06.181384Z",
          "is_publised": true
      }
    ]
    
#### browse authors

    curl --location --request GET 'http://127.0.0.1:8000/browse/author'

#### response
    [
      {
          "id": 1,
          "name": "John Doe",
          "location": "Chittagong",
          "publised_books": [
              {
                  "book_id": 1,
                  "book_name": "Harry Potter"
              },
              {
                  "book_id": 2,
                  "book_name": "Social Science"
              }
          ]
      },
      {
          "id": 2,
          "name": "foo bar",
          "location": "khulna",
          "publised_books": [
              {
                  "book_id": 4,
                  "book_name": "Bangla Grammer"
              }
          ]
      },
      {
          "id": 3,
          "name": "ramen hasar",
          "location": "borishal",
          "publised_books": [
              {
                  "book_id": 5,
                  "book_name": "English For Today"
              }
          ]
      }
    ]
 
#### search using search keyword

    curl --location --request GET 'http://127.0.0.1:8000/browse/author?search=john'
    
#### Response
    
    [
      {
          "id": 1,
          "name": "John Doe",
          "location": "Chittagong",
          "publised_books": [
              {
                  "book_id": 1,
                  "book_name": "Harry Potter"
              },
              {
                  "book_id": 2,
                  "book_name": "Social Science"
              }
          ]
      }
    ]
    
    
    
    
