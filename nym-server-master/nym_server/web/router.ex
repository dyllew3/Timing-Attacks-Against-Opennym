defmodule NymServer.Router do
  use NymServer.Web, :router

  pipeline :browser do
    plug :accepts, ["html"]
    plug :fetch_session
    plug :fetch_flash
    plug :protect_from_forgery
    plug :put_secure_browser_headers
  end

  pipeline :api do
    plug :accepts, ["json"]
  end

  scope "/nym", NymServer do
    pipe_through :api

    # get "/version", NymController, :version_index
    resources "/", NymController, only: [:show, :index]
  end

  scope "/ratings", NymServer do
    pipe_through :api

    resources "/:nym_id/:domain", RatingController, only: [:show, :index]
    put "/update/", RatingController, :update
    put "/padding/", RatingController, :pointless_request
  end

  scope "/cookies", NymServer do
    pipe_through :api

    get "/:nym_id", SessionCookiesController, :index#, param: :domain
    get "/:nym_id/:domain", SessionCookiesController, :show
    get "/issued/:nym_id/:domain", SessionCookiesController, :show_issued
  end

  scope "/rules", NymServer do
    pipe_through :api

    get "/supported", RuleController, :supported_index
    get "/supported/version", RuleController, :supported_version_index
    get "/top/:nym_id", RuleController, :nym_rules_show
    get "/:domain", RuleController, :domain_rule_show
    get "/issued/:domain", RuleController, :rule_issued_show
  end

  scope "/identity", NymServer do
    pipe_through :api

    get "/:domain", IdentityInterfaceController, :domain_index
    get "/:domain/:timestamp", IdentityInterfaceController, :domain_index
    get "/nym/:domain/:nym_id", IdentityInterfaceController, :nym_index
    get "/nym/:domain/:nym_id/:timestamp", IdentityInterfaceController, :nym_index
    get "/map/:domain/:username", IdentityInterfaceController, :map_username
  end
end
