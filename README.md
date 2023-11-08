# Quote of the Day

Welcome to the Quote of the Day service. This service provides you with a random quote of the day and allows you to manage a collection of quotes, including adding, updating, deleting, and searching by author. This `README.md` file is designed to help you get started with using our service.

## Getting Started

To use our service, you can follow these steps:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/yourusername/infotrixs.git
   ```

2. **Create a Virtual Environment and Activate It**:

  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

3. **Install Dependencies**:

   ```bash
   cd quote-of-the-day
   python -m pip install -r requirements.txt
   ```

4. **Run the Service**:

   ```bash
   python app.py
   ```

   The service should be up and running at `http://127.0.0.1:5000`.

## API Endpoints

### Get a Random Quote of the Day

- **Endpoint**: `/quote-of-the-day`
- **Method**: GET
- **Description**: Retrieve a random quote of the day.

### Get All Quotes or Add a New Quote

- **Endpoint**: `/quotes`
- **Methods**: GET, POST
- **Description**:
  - GET: Retrieve a list of all quotes.
  - POST: Add a new quote.

### Update or Delete a Specific Quote

- **Endpoint**: `/quotes/{quoteId}`
- **Methods**: GET, PUT, DELETE
- **Description**:
  - GET: Retrieve a specific quote by its ID.
  - PUT: Update a specific quote with new content.
  - DELETE: Delete a specific quote.

### Search for Quotes by Author

- **Endpoint**: `/quotes/search?author={authorName}`
- **Method**: GET
- **Description**: Search for quotes by the name of the author.

## How to Add a Quote

You can add a new quote using a web browser, `curl`, or an API testing tool like Postman. Here's how:

- **Using a Web Browser**: Visit `http://127.0.0.1:5000/add-quote` in your web browser. You'll find a form to input the author and content of the quote.

- **Using `curl` (Command Line)**: Execute the following command, replacing `"Author Name"` and `"Your Quote"` with the actual author and content for your quote:

  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{
      "author": "Author Name",
      "content": "Your Quote"
  }' http://127.0.0.1:5000/quotes
  ```

- **Using Postman**: Create a new POST request with the request URL set to `http://127.0.0.1:5000/quotes`. In the request body, provide the quote data in JSON format.

## Contributing

Feel free to contribute to this project by submitting issues or pull requests. We welcome your feedback and ideas!

## License

This project is licensed under the MIT License.

Enjoy using our Quote of the Day service!