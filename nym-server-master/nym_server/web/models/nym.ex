defmodule NymServer.Nym do
  use Ecto.Schema
  import Ecto.Changeset

  @primary_key {:id, :id, autogenerate: false}
  @derive {Phoenix.Param, key: :id}

  schema "nyms" do
    field :top_ratings, {:array, :id}
    field :top_domains, {:array, :string}
    has_many :ratings, NymServer.Rating
    has_many :session_cookies, NymServer.SessionCookies
  end

  def changeset(nym, params \\ %{}) do
    nym
    |> cast(params, [:id, :top_ratings, :top_domains])
    |> validate_required([:id])
  end
end
