import pytest
from fastapi import status

# Helper to execute GraphQL queries/mutations

def execute_graphql(client, query: str, variables: dict = None):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    response = client.post('/graphql', json=payload)
    return response


def test_graphql_create_query_update_delete_book(client):
    # Create a new book
    create_mutation = '''
    mutation CreateBook($input: CreateBookInput!) {
      createBook(
        title: $input.title,
        subtitle: $input.subtitle,
        author: $input.author,
        pages: $input.pages
      ) {
        book { id title author pages }
      }
    }
    '''
    variables = {'input': {'title': 'GraphQL Test', 'subtitle': 'Sub', 'author': 'Tester', 'pages': 123}}
    response = execute_graphql(client, create_mutation, variables)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()['data']['createBook']['book']
    book_id = int(data['id'])
    assert data['title'] == 'GraphQL Test'

    # Query list
    list_query = '''
    query GetBooks($skip: Int, $limit: Int) {
      books(skip: $skip, limit: $limit) { id title }
    }
    '''
    response = execute_graphql(client, list_query, {'skip': 0, 'limit': 10})
    assert response.status_code == status.HTTP_200_OK
    books = response.json()['data']['books']
    assert any(int(b['id']) == book_id for b in books)

    # Update book
    update_mutation = '''
    mutation UpdateBook($id: Int!, $title: String!) {
      updateBook(id: $id, title: $title) { book { id title } }
    }
    '''
    response = execute_graphql(client, update_mutation, {'id': book_id, 'title': 'Updated'})
    assert response.status_code == status.HTTP_200_OK
    updated = response.json()['data']['updateBook']['book']
    assert updated['title'] == 'Updated'

    # Delete book
    delete_mutation = '''
    mutation DeleteBook($id: Int!) {
      deleteBook(id: $id) { ok }
    }
    '''
    response = execute_graphql(client, delete_mutation, {'id': book_id})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['data']['deleteBook']['ok'] is True

    # Confirm deletion
    query_single = '''
    query GetBook($id: Int!) {
      book(id: $id) { id title }
    }
    '''
    response = execute_graphql(client, query_single, {'id': book_id})
    assert response.json()['data']['book'] is None


def test_create_book_missing_required_field(client):
    # Missing required 'title'
    mutation = '''
    mutation {
      createBook(author: "No Title", pages: 10) { book { id title } }
    }
    '''
    response = execute_graphql(client, mutation)
    assert response.status_code == status.HTTP_400_BAD_REQUEST or 'errors' in response.json()


def test_create_book_invalid_type(client):
    # Invalid type for 'pages'
    mutation = '''
    mutation {
      createBook(title: "Invalid", author: "Test", pages: "NaN") { book { id pages } }
    }
    '''
    response = execute_graphql(client, mutation)
    assert response.status_code == status.HTTP_400_BAD_REQUEST or 'errors' in response.json()


def test_query_nonexistent_book_returns_null(client):
    query = '''
    query {
      book(id: 9999) { id title }
    }
    '''
    response = execute_graphql(client, query)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['data']['book'] is None

@pytest.mark.skip(reason="Subscription support not yet implemented in schema")
def test_book_created_subscription(client):
    # Placeholder for subscription test once 'bookCreated' subscription is implemented
    with client.websocket_connect('/graphql') as ws:
        # Initialize subscription
        ws.send_json({
            'type': 'start',
            'id': '1',
            'payload': {'query': 'subscription { bookCreated { id title } }'}
        })
        # Trigger an event via mutation
        mutation = '''
        mutation {
          createBook(title: "Sub Test", author: "Sub", pages: 5) { book { id title } }
        }
        '''
        client.post('/graphql', json={'query': mutation})
        # Expect data on websocket
        msg = ws.receive_json(timeout=5)
        assert msg['type'] == 'data'
        data = msg['payload']['data']['bookCreated']
        assert data['title'] == 'Sub Test'
