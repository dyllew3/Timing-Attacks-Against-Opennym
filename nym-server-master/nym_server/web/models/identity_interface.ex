defmodule NymServer.IdentityInterface do
  use Ecto.Schema
  import Ecto.Changeset

  # Rating model structure
  schema "identity_interface" do
    field :domain, :string
    field :username, :string
    belongs_to :nym, NymServer.Nym
  end

  # Define changeset for making updates to existing model in DB
  def changeset(rating, params \\ %{}) do
    rating
    |> cast(params, [:domain, :username, :nym_id])
    |> validate_required([:domain, :username, :nym_id])
  end
end
