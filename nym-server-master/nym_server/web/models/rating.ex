defmodule NymServer.Rating do
  use Ecto.Schema
  import Ecto.Changeset

  # Rating model structure
  schema "ratings" do
    field :domain, :string
    field :item, :string
    field :score, :float
    field :num_votes, :integer
    belongs_to :nym, NymServer.Nym

    timestamps()
  end

  # Define changeset for making updates to existing model in DB
  def changeset(rating, params \\ %{}) do
    rating
    |> cast(params, [:domain, :item, :score, :num_votes, :nym_id])
    |> validate_required([:domain, :item, :score, :num_votes, :nym_id])
  end
end
