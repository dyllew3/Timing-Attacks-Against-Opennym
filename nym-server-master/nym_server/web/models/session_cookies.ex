defmodule NymServer.SessionCookies do
  use Ecto.Schema
  import Ecto.Changeset

  schema "session_cookies" do
    field :domain, :string
    field :cookies, :string
    belongs_to :nym, NymServer.Nym

    timestamps()
  end

  def changeset(session_cookies, params \\ %{}) do
    session_cookies
    |> cast(params, [:domain, :cookies, :nym_id])
    |> validate_required([:domain, :cookies, :nym_id])
  end
end
