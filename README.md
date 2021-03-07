# evaly-coding-test

#### 1. get excel download link
    
    curl --location --request GET 'http://127.0.0.1:8000/loans/get-excel-for-loans'
    
#### Response
    
    {
        "download_link": "http://127.0.0.1:8000/media/loans.csv"
    }

#### 2. Browse books

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
    
#### 3. Search books using ?search query 

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
    
#### 4. Browse authors

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
 
#### 5. Search using search keyword

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

#### 6. List Loan Requests(member)(gets his own request)
     curl --location --request GET 'http://127.0.0.1:8000/loans/loan' \
     --header 'Authorization: Token d9a59df3ebf8ec04145d1cf47c0c5c9874a4f8bf'
     
#### Respone
    
    [
    {
        "id": 2,
        "member": {
            "id": 3,
            "name": "onni",
            "email": "onni@gmail.com"
        },
        "book": 1,
        "is_accepted": false,
        "is_rejected": false,
        "is_returned": false
    },
    {
        "id": 3,
        "member": {
            "id": 3,
            "name": "onni",
            "email": "onni@gmail.com"
        },
        "book": 2,
        "is_accepted": true,
        "is_rejected": false,
        "is_returned": true
    },    
    ]

#### 7. List Loan Request(admin)(gets all request)

    curl --location --request GET 'http://127.0.0.1:8000/loans/loan' \
    --header 'Authorization: Token fe46efb60cc0656528c7cbb7812d14ffac33742c'

#### Response
    [
    {
        "id": 2,
        "member": {
            "id": 3,
            "name": "onni",
            "email": "onni@gmail.com"
        },
        "book": 1,
        "is_accepted": false,
        "is_rejected": false,
        "is_returned": false
    },
    {
        "id": 3,
        "member": {
            "id": 3,
            "name": "onni",
            "email": "onni@gmail.com"
        },
        "book": 2,
        "is_accepted": true,
        "is_rejected": false,
        "is_returned": true
    },
    {
        "id": 4,
        "member": {
            "id": 3,
            "name": "onni",
            "email": "onni@gmail.com"
        },
        "book": 2,
        "is_accepted": true,
        "is_rejected": false,
        "is_returned": true
    },
    {
        "id": 5,
        "member": {
            "id": 3,
            "name": "onni",
            "email": "onni@gmail.com"
        },
        "book": 4,
        "is_accepted": true,
        "is_rejected": true,
        "is_returned": true
    },
    {
        "id": 6,
        "member": {
            "id": 3,
            "name": "onni",
            "email": "onni@gmail.com"
        },
        "book": 4,
        "is_accepted": false,
        "is_rejected": false,
        "is_returned": false
    },
    {
        "id": 7,
        "member": {
            "id": 3,
            "name": "onni",
            "email": "onni@gmail.com"
        },
        "book": 4,
        "is_accepted": false,
        "is_rejected": false,
        "is_returned": false
    },
    {
        "id": 8,
        "member": {
            "id": 3,
            "name": "onni",
            "email": "onni@gmail.com"
        },
        "book": 4,
        "is_accepted": false,
        "is_rejected": false,
        "is_returned": false
    },
    {
        "id": 9,
        "member": {
            "id": 3,
            "name": "onni",
            "email": "onni@gmail.com"
        },
        "book": 4,
        "is_accepted": false,
        "is_rejected": false,
        "is_returned": false
    },
    {
        "id": 10,
        "member": {
            "id": 3,
            "name": "onni",
            "email": "onni@gmail.com"
        },
        "book": 4,
        "is_accepted": false,
        "is_rejected": false,
        "is_returned": false
    }
    ]

#### 8. Create Loan Request(member)

    curl --location --request POST 'http://127.0.0.1:8000/loans/loan/' \
    --header 'Authorization: Token d9a59df3ebf8ec04145d1cf47c0c5c9874a4f8bf' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "book":4
    }'
    
#### Response
    {
        "id": 10,
        "member": 3,
        "book": 4,
        "is_accepted": false,
        "is_rejected": false,
        "is_returned": false
    }
    
#### 9. Update Load Request(only admin)

    curl --location --request PATCH 'http://127.0.0.1:8000/loans/loan/2/' \
    --header 'Authorization: Token fe46efb60cc0656528c7cbb7812d14ffac33742c' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "is_accepted": true,
        "is_rejected": true,
        "is_returned": true
    }'
    
#### Response
    {
        "id": 2,
        "member": 3,
        "book": 1,
        "is_accepted": true,
        "is_rejected": true,
        "is_returned": true
    }
    
    
