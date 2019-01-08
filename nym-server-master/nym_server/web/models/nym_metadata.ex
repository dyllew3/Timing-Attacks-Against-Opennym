defmodule NymServer.NymMetadata do
  use Ecto.Schema
  import Ecto.Changeset

  schema "nym_metadata" do
    field :clustering_version, :float
    field :support_list_version, :float
  end

  def changeset(nym_metadata, params \\ %{}) do
    nym_metadata
    |> cast(params, [:clustering_version, :support_list_version])
    |> validate_required([:clustering_version, :support_list_version])
  end
end
