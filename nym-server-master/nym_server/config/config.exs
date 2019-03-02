# This file is responsible for configuring your application
# and its dependencies with the aid of the Mix.Config module.
#
# This configuration file is loaded before any dependency and
# is restricted to this project.
use Mix.Config

# General application configuration
config :nym_server,
  ecto_repos: [NymServer.Repo]

# Configures the endpoint
config :nym_server, NymServer.Endpoint,
  url: [host: "localhost"],
  secret_key_base: "5BuJ7YtEnVOo0Cv8EWC2F/WZDEpopTcPVGG8Lq6SvxR6cmfoeoggkUIJq0gnFccT",
  render_errors: [view: NymServer.ErrorView, accepts: ~w(html json)],
  pubsub: [name: NymServer.PubSub,
           adapter: Phoenix.PubSub.PG2]

# Configures Elixir's Logger
config :logger,
  backends: [ {LoggerFileBackend, :hutt}, :console],
  format: "$date $time $metadata[$level] $message\n",
  metadata: [:request_id]

config :logger, :hutt,
  format: "$date $time $metadata[$level] $message\n",
  path: "logs/info.log",
  level: :debug

# Import environment specific config. This must remain at the bottom
# of this file so it overrides the configuration defined above.
import_config "#{Mix.env}.exs"
