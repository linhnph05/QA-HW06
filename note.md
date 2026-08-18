# Screenshot still needed from Terminal

The browser tools can capture the Newman HTML page, but the required pre-request console evidence is shown in a Terminal window. Please take this screenshot:

1. Open Terminal in the `hw06` repository.
2. Start the backend at `http://127.0.0.1:3000`.
3. Run:

   ```bash
   newman run collections/EShop-HW06.postman_collection.json \
     -e collections/local.postman_environment.json \
     -r cli
   ```

4. Capture a screenshot that clearly shows these repeated console lines and at least one request URL:

   ```text
   'X-Student-Id header:', '23127081'
   POST http://127.0.0.1:3000/...
   ```

5. Save it as `images/student-id-console.png`.

