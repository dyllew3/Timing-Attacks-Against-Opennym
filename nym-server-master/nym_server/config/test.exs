use Mix.Config

# We don't run a server during test. If one is required,
# you can enable the server option below.
config :nym_server, NymServer.Endpoint,
  http: [port: 4001],
  server: false

# Print only warnings and errors during test
config :logger, level: :warn

# Configure your database
config :nym_server, NymServer.Repo,
  adapter: Ecto.Adapters.Postgres,
  username: "postgres",
  password: "opennym",
  database: "nym_server_test",
  hostname: "localhost",
  pool: Ecto.Adapters.SQL.Sandbox
