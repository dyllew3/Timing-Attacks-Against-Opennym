# NymServer

To start your Phoenix app:

  * Install dependencies with `mix deps.get`
  * Create and migrate your database with `mix ecto.create && mix ecto.migrate`
  * Install Node.js dependencies with `npm install`
  * Start Phoenix endpoint with `mix phoenix.server`

Now you can visit [`localhost:4000`](http://localhost:4000) from your browser.

Ready to run in production? Please [check our deployment guides](http://www.phoenixframework.org/docs/deployment).

## Learn more

  * Official website: http://www.phoenixframework.org/
  * Guides: http://phoenixframework.org/docs/overview
  * Docs: https://hexdocs.pm/phoenix
  * Mailing list: http://groups.google.com/group/phoenix-talk
  * Source: https://github.com/phoenixframework/phoenix

# TODO
* Get top cookies given nym id. Currently broken
* Add HTTP verb to rule responses
* Optional Timestamp to be included in request to get nyms, that checks if any nyms have changed since timestamp. Return no-change if there isnt.
* Same for requesting support list version, allow client to send current version in headers or as parameter and returned 304 - Not Modified
